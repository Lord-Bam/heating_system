class Controller:
    __heating = None
    
    def __init__(self, heating):
        self.__heating = heating
        #the temperature sensor add delay which impacts reading of the button.
        #easiest fix is to start it as a child process.
        self.__heating.set_hysteresis_value(1)
    
    #__current_temperature = hardware_input.get_room_temperature()    
    
    def get_current_temperature(self):
        return self.__heating.get_current_temp()
    
    def set_current_temperature(self, temp):
        self.__heating.set_current_temp(temp)
        return self.__heating.get_current_temp()
    
    
    def get_target_temperature(self):
        return self.__heating.get_target_temp()
    
    def set_target_temperature(self, temp):
        print(f"setting target temperature {temp}")
        self.__heating.set_target_temp(temp)
        return self.__heating.get_target_temp()
    
    def toggle_on_off(self):
        self.__heating.set_heating_system_state(not self.__heating.get_heating_system_state())
        
    def temp_down(self):
        if self.__heating.get_target_temp() > 15:
            self.__heating.set_target_temp(self.__heating.get_target_temp() - 1)
    
    def temp_up(self):
        if self.__heating.get_target_temp() < 25:
            self.__heating.set_target_temp(self.__heating.get_target_temp() + 1)

    def get_heating_system_state(self):
        if self.__heating.get_heating_system_state() == 1:
            return "on"
        else:
            return "off"
        
    def set_ip(self, ip):
        self.__heating.set_ip(ip)
        
    def get_ip(self):
        self.__heating.get_ip()
           
    
    def get_osd_lines(self):
        #write to display
        lines = []
        lines.append(f"heating on: {self.__heating.get_heating_system_state()}")
        lines.append(f"current: {self.__heating.get_current_temp()}")
        lines.append(f"target: {self.__heating.get_target_temp()}")
        lines.append(f"burner: {self.__heating.get_burner_state()}")
        lines.append(self.__heating.get_ip())
        return lines
    
    def get_webservice_lines(self):
        
        lines = {}
        lines["heating_on"] = self.__heating.get_heating_system_state()
        lines["temp"] = self.__heating.get_current_temp()
        lines["target"] = self.__heating.get_target_temp()
        lines["burner"] = self.__heating.get_burner_state()
        return lines
    
    def heating_required(self):
        return(self.__heating.heating_required())
            