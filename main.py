import machine
import heating_system
import hardware_driver
import time
import _thread as thread
import network_service
import hardware_service
import controller
from machine import UART

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


led = machine.Pin(2, machine.Pin.OUT)
led.value(1)
uart = UART(1, baudrate=115200, tx=1, rx=3)
previous_target_temp = controller.get_target_temperature()
previous_current_temp = controller.get_current_temperature()

while True:
    #run hardware service
    hardware_service.run()
    print("loop")
    target_temp = controller.get_target_temperature()
    state =  controller.get_heating_system_state()
    
    data = uart.any()
    if data:
        data = uart.read()
        if data == b'toggle_on_off\n':
            controller.toggle_on_off()
            data = controller.get_heating_system_state()
            data = "state-" + str(data) + "\n"
            uart.write(bytes(data, 'UTF-8'))
            led.value(1)
        else:
            uart.write(data)
            led.value(0)
    
    if previous_target_temp != controller.get_target_temperature():
        previous_target_temp = controller.get_target_temperature()
        data = "target_temp-" + str(target_temp) + "\n"
        uart.write(bytes(data, 'UTF-8'))

    if previous_current_temp != controller.get_current_temperature():
        previous_current_temp = controller.get_current_temperature()
        data = "current_temp-" + str(controller.get_current_temperature()) + "\n"
        uart.write(bytes(data, 'UTF-8'))
    
    
    
        
    
