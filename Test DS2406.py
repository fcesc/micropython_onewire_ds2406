import machine
from machine import Pin, Timer
import onewire


ONE_WIRE_PIN = 21
p_ow = Pin(ONE_WIRE_PIN, Pin.OUT)
ow = onewire.OneWire(p_ow)


# Change the PIO_A output state.
def setPIO_A( dev, on ):
    ow.select_rom(dev)
    ow.writebyte(0x55)
    ow.writebyte(0x07)
    ow.writebyte(0)
    # 0x1F: GPIO_A -> Transistor On
    # 0x3F: GPIO_A -> Transistor Off
    if on:
        ow.writebyte(0x1F)
    else:
        ow.writebyte(0x3F)
    ow.readbyte()
    ow.readbyte()



# Demo loop.
def change_state_loop(t):
    global b
    if b:
        setPIO_A(devs[0], True)
    else:
        setPIO_A(devs[0], False)
    print(b)
    b = not b


#######################################

ow.reset()

global devs    
devs = ow.scan()

if len(devs)>0:
    global b
    b = True
    
    # Forever.
    timer = Timer(-1)
    timer.init(period=750, callback=change_state_loop)
else:
    print('No device found!')




