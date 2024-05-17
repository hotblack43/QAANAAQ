import serial

# Open serial port
ser = serial.serial_for_url('/dev/ttyUSB0', baudrate=4800)

try:
    while True:
        # Read a line from serial port
        line = ser.readline().decode().strip()
        
        # Print the received GPS data
        print(line)

finally:
    # Close the serial port
    ser.close()

