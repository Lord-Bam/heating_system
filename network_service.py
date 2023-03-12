import network
import usocket as socket
import json
import _thread as thread

class Network_service:
  
    def __init__(self, controller, network_name, password):
        #setup the network interface.
        self.__sta_if = network.WLAN(network.STA_IF)
        if not self.__sta_if.isconnected():
            print('connecting to network...')
            self.__sta_if.active(True)
            self.__sta_if.connect(network_name, password)
            while not self.__sta_if.isconnected():
                pass
    
        print('network config:', self.__sta_if.ifconfig()[0])

        #create websocket:
        self.__s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.__s.bind(('', 80))
        self.__s.listen(5)
        
        self.__controller = controller
        #write the ip to the controller so it can be saved in the model.
        self.__controller.set_ip(self.__sta_if.ifconfig()[0])

    def web_service(self):
        while True:
            #Listen on the socket.
            conn, addr = self.__s.accept()
            #print('Got a connection from %s' % str(addr))
            request = conn.recv(1024)
            print(request)
            
            #Decode and split the request to get the HTTP method.
            request = str(request.decode("utf-8"))
            request = request.split("\r\n")
            request_type = (request[0].split(" ")[0])
            
            
            #curl 192.168.0.169
            if request_type == "GET":
                payload = self.__controller.get_webservice_lines()
            
            
            if request_type == "POST":
                try:
                    #get the json out of the request.
                    body_dict = json.loads(request.pop())
                    
                    #Switch on_off
                    if "toggle_on_off" in body_dict:
                        if body_dict["toggle_on_off"] == "true":
                            self.__controller.toggle_on_off()
                    
                    #Set temperature
                    if "target_temp" in body_dict:
                        #Increase, decrease temperature by 1
                        if body_dict["target_temp"] == "up":
                            self.__controller.temp_up()
                        elif body_dict["target_temp"] == "down":
                            self.__controller.temp_down()
                        #Set the temperature to a value.
                        else:                        
                            self.__controller.set_target_temperature(body_dict["target_temp"])
                    
                    #returning the current state of the model          
                    payload = self.__controller.get_webservice_lines()
                
                    print(json.dumps(payload))
                except:
                    payload = {}
                    payload["POST"] = "crap something went wrong"
            
            #Sending response.
            conn.send('HTTP/1.1 200 OK\r\n')
            conn.send('Content-Type: application/json\r\n')
            conn.send('Connection: close\r\n')
            conn.send('\n')
            conn.send(json.dumps(payload))
            conn.close()
            
            

