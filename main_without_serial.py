import machine
import heating_system
import hardware_driver
import time
import _thread as thread
import network_service
import hardware_service
import controller
#The wifi password.
password = ""
network = ""

#create model
hysteresis = 1
heating = heating_system.Heating_system(hysteresis)

#create controller
controller = controller.Controller(heating)

#create hardware service and drivers
hardware_input = hardware_driver.Hardware_input_driver(4, 36, 5, 18, 19, 2, 15)
hardware_output = hardware_driver.Hardware_output_driver(23, 21, 22)   
hardware_service = hardware_service.Hardware_service(controller, hardware_input, hardware_output)
 
#Create networking service.
network_service = network_service.Network_service(controller, network, password)
#Since the network service waits for input it is started in a thread
thread.start_new_thread(network_service.web_service, ())



while True:
    #run hardware service
    hardware_service.run()


    
    
    
    
        
    
