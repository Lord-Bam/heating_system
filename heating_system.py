class Heating_system:
    __current_temp = 0
    __target_temp = 0
    #Boolean to store if heating is on.
    __heating_system_state = False
    #Boolean to store if burner/relais is on.
    __burner_state = False
    __hysteresis_value = 0
    __network_ip = ""
    
    
    def __init__(self, hysteresis):
        self.__hysteresis_value = hysteresis
        pass
    
    
    def get_current_temp(self):
        return self.__current_temp
    
    def set_current_temp(self, temp):
        self.__current_temp = temp
        
        
    def get_target_temp(self):
        return self.__target_temp
    
    def set_target_temp(self, temp):
        self.__target_temp = temp
        
        
    def get_heating_system_state(self):
        return self.__heating_system_state
    
    def set_heating_system_state(self, state):
        self.__heating_system_state = state
    
    
    def get_burner_state(self):
        return self.__burner_state
    
    def set_burner_state(self, state):
        self.__burner_state = state
        
        
    def get_hysteresis_value(self):
        return self.__hysteresis_value
    
    def set_hysteresis_value(self, hysteresis_value):
        self.__hysteresis_value = hysteresis_value
        
    def get_ip(self):
        return self.__network_ip
    
    def set_ip(self, ip):
        self.__network_ip = ip
        
    
    #Function to check if heating is required. 
    def heating_required(self):
        #Set target temperature depending on the state of the burner and the hysteresis_value
        if self.__burner_state == 1:
            hysteresis_target = self.__target_temp + self.__hysteresis_value
        else:
            hysteresis_target = self.__target_temp - self.__hysteresis_value
    
        #If the heating is on, set a burner state
        if self.__heating_system_state == 1:
            #check if target temp is reached
            if self.__current_temp < hysteresis_target:
                self.set_burner_state(True)
                return True
            else:
                self.set_burner_state(False)
                return False
        #heating is off.
        else:
            self.set_burner_state(False)
            return False
            
    