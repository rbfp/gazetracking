#NEC A: 0x17 C: 0x44
#ir tx NEC 0x17 0x44

###2
#NEC A: 0x17 C: 0x43
#ir tx NEC 0x17 0x43

##3
#NEC A: 0x17 C: 0x07
#ir tx NEC 0x17 0x07

import serial
import time

SERIAL_PORT = '/dev/cu.usbmodemflip_Ouyidot1'  # Replace with your serial port
BAUD_RATE = 115200
COMMAND = "ir tx NEC 0x17 0x07\r"

try:
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as flipper:
        print(f"Connected to {SERIAL_PORT}")
        flipper.write(COMMAND.encode('utf-8'))
        print(f"Sent command: {COMMAND.strip()}")
        time.sleep(1)
        response = flipper.read_all().decode('utf-8')
        print(f"Response: {response}")
except Exception as e:
    print(f"Error: {e}")