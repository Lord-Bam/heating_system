import machine
import time

pot = machine.ADC(machine.Pin(2))
pot.width(machine.ADC.WIDTH_9BIT)
pot.atten(pot.ATTN_11DB)
smallest = pot.read() + 1
biggest = pot.read() - 1

for x in range(5):
    smallest = pot.read() + 1
    biggest = pot.read() - 1
    for x in range(100000):
      
        value = pot.read()
        
        if value < smallest:
            smallest = value
        
        if value > biggest:
            biggest = value
            

    print("biggest", biggest)
    print("smallest", smallest)
    print(biggest - smallest)
    print("")
print("done")
