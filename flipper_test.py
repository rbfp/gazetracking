###1
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

# Replace with your Flipper Zero's serial port
SERIAL_PORT = '/dev/tty.usbmodemflip_Ouyidot1'  # Use 'COM3' on Windows
BAUD_RATE = 115200

# Command to send the IR remote
command = "ir tx NEC 0x17 0x44\n\n"

try:
    # Open serial connection
    with serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1) as flipper:
        print(f"Connected to {SERIAL_PORT}")

        # Send the IR command
        flipper.write(command.encode('utf-8'))
        print(f"Sent command: {command.strip()}")

        # Wait for a response
        time.sleep(2)

        # Read the response
        response = flipper.read_all().decode('utf-8')
        print("Response:")
        print(response)

except Exception as e:
    print(f"Error: {e}")
