#Bovenaan je code zet je deze klasse
#begin klasse:
class ds18x20_mock:
    __current_temp = 19
    __relais = None
    
    def __init__(self, relais):
        self.__relais = relais
    
    def convert_temp(self):
        if self.__relais.value() == 1:
            self.__current_temp = self.__current_temp + 0.001
        else:
            self.__current_temp = self.__current_temp - 0.001
        
    def read_temp(self, rom):
        return self.__current_temp

#einde klasse

ds_sensor = ds18x20_mock(relais)