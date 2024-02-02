import smbus
import time

# Define I2C bus number (typically 1 for Raspberry Pi)
bus = smbus.SMBus(1)

# Define HMC5983 address
HMC5983_ADDR = 0x1E

def initialize_hmc5983():
    # Configure HMC5983 for continuous measurement mode
    bus.write_byte_data(HMC5983_ADDR, 0x00, 0x70)  # Configuration Register A
    bus.write_byte_data(HMC5983_ADDR, 0x01, 0xE0)  # Configuration Register B
    bus.write_byte_data(HMC5983_ADDR, 0x02, 0x00)  # Continuous mode 
    time.sleep(0.1)  # Delay for stability

def read_hmc5983():
    # Read 6 bytes of data from HMC5983
    data = bus.read_i2c_block_data(HMC5983_ADDR, 0x03, 6)
    print(data)

    # Convert the data from two's complement to signed integers
    x = twos_complement((data[0] << 8) | data[1])
    y = twos_complement((data[2] << 8) | data[3])
    z = twos_complement((data[4] << 8) | data[5])

    return x, y, z

def twos_complement(val):
    # Convert a 16-bit two's complement value to a signed integer
    if val & (1 << 15):
        val = val - (1 << 16)
    return val

if __name__ == "__main__":
    try:
        initialize_hmc5983()
        while True:
            try:
                x, y, z = read_hmc5983()
                print(f"X: {x}, Y: {y}, Z: {z}")
                time.sleep(1)  # Delay for stability
            except Exception as e:
                print(e)

    except KeyboardInterrupt:
        pass

