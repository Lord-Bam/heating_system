import time

class Hardware_service:
    def __init__(self, controller, hardware_input, hardware_output):
        self.__controller = controller
        self.__hardware_input = hardware_input
        self.__hardware_output = hardware_output
        self.__timer = time.ticks_ms() - 5000
        self.__previous_target_temperature = 0

    #method used to get input from hardware.
    def get_input(self):
        
        #The potmeter cannot not change "state" when the target temperture gets changed by the webserver, buttons or rotary encoder.
        #To prevent the potmeter from overwriting the temperature a temporary variable "__previous_target_temperature" is used.
        #Use a local variable to prevent potmeter from overwriting the temperature set by the webserver
        if self.__hardware_input.get_room_temperature_target() != self.__previous_target_temperature:
            self.__previous_target_temperature = self.__hardware_input.get_room_temperature_target()
            self.__controller.set_target_temperature(self.__previous_target_temperature)
        
        if self.__hardware_input.get_on_off_button_pressed() == 1:
            print("button pressed")
            self.__controller.toggle_on_off()
            
        if self.__hardware_input.get_temp_down_button_pressed() == 1:
            print("button pressed")
            self.__controller.temp_down()
            
        if self.__hardware_input.get_temp_up_button_pressed() == 1:
            print("button pressed")
            self.__controller.temp_up()
            
        #The rotary encoder has a direction it is turned.
        #the direction is saved in the rotary encoder as a string and used in this method
        if self.__hardware_input.get_rot_encoder_direction() != "":
            print("rot encoder", self.__hardware_input.get_rot_encoder_direction())
            
            if self.__hardware_input.get_rot_encoder_direction() == "left":
                self.__controller.temp_down()
            if self.__hardware_input.get_rot_encoder_direction() == "right":
                self.__controller.temp_up()
            
            self.__hardware_input.reset_rot_encoder()
        
        #A timer limits the rate the temperature sensor is read. 
        if self.__timer + 5000 < time.ticks_ms():
            self.__timer = time.ticks_ms()
            print("reading")
            try:
                current_temperature = self.__hardware_input.get_room_temperature()
                self.__controller.set_current_temperature(current_temperature)
            except Exception as e:
                import sys
                sys.print_exception(e)
            
        
        
    #Write output to the OSD. The lines themself are fetched in the controller
    def write_output(self):
        lines = self.__controller.get_osd_lines()  
        self.__hardware_output.write_to_display(lines)
        
    #Switch on the relais if heating is required.
    def set_burner(self):
        if self.__controller.heating_required() == 1:
            self.__hardware_output.set_relais_state(1)
        else:
            self.__hardware_output.set_relais_state(0)
        
    #Return state of the relais
    def get_burner(self):
        return self.__hardware_output.get_relais_state()
    
    #Hardware service main function
    def run(self):
        self.get_input()
        self.set_burner()
        self.write_output()
        
    
        
