import machine
import sh1106
import ds18x20
import onewire
import time
#from machine import I2C

#https://github.com/gurgleapps/rotary-encoder
class Rotary:
    
    def __init__(self,s1, s2):
        #Set pins of rotary encoder. The push button is not used.
        self.__s1_pin = machine.Pin(s1, machine.Pin.IN, machine.Pin.PULL_UP)
        self.__s2_pin = machine.Pin(s2, machine.Pin.IN, machine.Pin.PULL_UP)
        #Create interrupts for the changing of the pin.
        self.__s1_pin.irq(handler=self.rotaryChange, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        self.__s2_pin.irq(handler=self.rotaryChange, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING)
        #Save the start state of the encoder.
        #A bitshift is used to save the 2 values of the pin in binary
        self.__last_status = (self.__s1_pin.value() << 1 | self.__s2_pin.value())
        #Variable used to save the last rotation diraction
        self.__rot_encoder_direction = ""

    #When an interrupt is thrown the following method is called.
    def rotaryChange(self, pin):
        
        #Save the current state of the rotary controller.
        new_status = (self.__s1_pin.value() << 1 | self.__s2_pin.value())
        rotation_result = (self.__last_status << 2) | new_status
        
        #only write when there is a change.
        if new_status != self.__last_status:
            self.__last_status = new_status
            
            #11 is the start state, 10 is right
            if rotation_result == 0b1110:
                self.__rot_encoder_direction = "right"
            
            #11 is the start state, 01 is left
            elif rotation_result == 0b1101:
                self.__rot_encoder_direction = "left"
            
            #reset the encoder to the starting position.
            else:
                rotation_result = (self.__s1_pin.value() << 1 | self.__s2_pin.value())
    
    #reset the location direction to "center".
    def reset_rot_encoder(self):
        self.__rot_encoder_direction = ""
        
    #return the last rotation direction.
    def get_rot_encoder_direction(self):
        return self.__rot_encoder_direction

        



class Hardware_input_driver:

    def __init__(self, temp_pin, pot_pin, on_off_pin, temp_down_pin, temp_up_pin, rotary_s1, rotary_s2):
        
        #setup temperature sensor
        ds_pin = machine.Pin(temp_pin)
        self.__ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
        roms = self.__ds_sensor.scan()
        print("Found DS devices: ", roms)
        self.__rom = roms[0]
        
        #create pot sensor.
        self.__pot = machine.ADC(machine.Pin(pot_pin))
        self.__pot.atten(self.__pot.ATTN_11DB)
        self.__pot.width(machine.ADC.WIDTH_12BIT)
        machine.ADC.WIDTH_9BIT
        #on off button
        self.__on_off_button = machine.Pin(on_off_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.__previous_on_off_button = self.__on_off_button.value()
        
        self.__temp_down_button = machine.Pin(temp_down_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.__previous_temp_down_button = self.__temp_down_button.value()
        
        self.__temp_up_button = machine.Pin(temp_up_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self.__previous_temp_up_button = self.__temp_up_button.value()
        
        #create rotary encoder
        self.__rot_encoder = Rotary(2, 15)
        
    def get_room_temperature(self):
        self.__ds_sensor.convert_temp()
        temperature = round(self.__ds_sensor.read_temp(self.__rom), 1)
        return(temperature)
        
    def get_room_temperature_target(self):
        
        #Get average of multiple measurements to get a more acurate reading.
        #Also added a decoupling capacitor!!
        total = 0
        for x in range(1000):
            total = total + self.__pot.read()
        total = total // 1000
        temperature_setting = round(total/4095*10 + 15)
        return(temperature_setting)
    
    def get_on_off_button_pressed(self):
        #return_value is needed since return in the if will circomvent the sleep!
        return_value = 0
        if self.__previous_on_off_button != self.__on_off_button.value():
            self.__previous_on_off_button = self.__on_off_button.value()
            if self.__on_off_button.value() == 0:
                return_value = 1
        
            time.sleep(0.1)
        return return_value
    
    def get_temp_down_button_pressed(self):
        #return_value is needed since return in the if will circomvent the sleep!
        return_value = 0
        if self.__previous_temp_down_button != self.__temp_down_button.value():
            self.__previous_temp_down_button = self.__temp_down_button.value()
            if self.__temp_down_button.value() == 0:
                return_value = 1
        
            time.sleep(0.1)
        return return_value
    
    def get_temp_up_button_pressed(self):
        #return_value is needed since return in the if will circomvent the sleep!
        return_value = 0
        if self.__previous_temp_up_button != self.__temp_up_button.value():
            self.__previous_temp_up_button = self.__temp_up_button.value()
            if self.__temp_up_button.value() == 0:
                return_value = 1
        
            time.sleep(0.1)
        return return_value

    def get_rot_encoder_direction(self):
        return_value = self.__rot_encoder.get_rot_encoder_direction()
        return return_value
    
    def reset_rot_encoder(self):
        self.__rot_encoder.reset_rot_encoder()
   


class Hardware_output_driver():
    
    def __init__(self, scl_pin, sda_pin, relais_pin):
        #create display
        i2c = machine.I2C(scl=machine.Pin(scl_pin), sda=machine.Pin(sda_pin), freq=400000)
        self.__display = sh1106.SH1106_I2C(128, 64, i2c, machine.Pin(16), 0x3C, rotate=180)
        self.__display.sleep(False)
        #initialize display lines
        self.__display_line = []
        for x in range(5):
            self.__display_line.append("")
        
        #relais
        self.__relais = machine.Pin(relais_pin, machine.Pin.OUT)
        self.__relais.value(0)  
        
        
    def write_to_display(self, lines):
        
        #only write if lines where changed.
        if self.__display_line != lines:
            self.__display_line = lines
            self.__display.fill(0)
            for x in range(5):
                self.__display.text(self.__display_line[x], 0, x * 10, 1)           
            self.__display.show()  
        
        
    def get_relais_state(self):
        return self.__relais.value()
    
    def set_relais_state(self, x):
        #Only write if there is a change in the relais state.
        if self.__relais.value() != x:
            self.__relais.value(x)
            return self.__relais.value()
    
        
    
