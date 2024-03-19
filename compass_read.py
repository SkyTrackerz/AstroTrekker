import smbus
import time
import math

# Docs: https://www.farnell.com/datasheets/1509871.pdf?_ga=2.219060057.1318745487.1555987311-293789508.1555987311

# Define I2C bus number (typically 1 for Raspberry Pi)
bus = smbus.SMBus(1)

# Define HMC5983 address
HMC5983_ADDR = 0x1E


def initialize_hmc5983(temperature_compensation=True, samples_avgd_per_output=8, data_rate_hz=15):
    # Ensure that samples_avgd_per_output is one of the allowed values

    # Create a mapping of the sample averages to their respective binary codes
    samples_to_bin = {1: 0b00, 2: 0b01, 4: 0b10, 8: 0b11}
    data_rate_to_bin = {
        0.75: 0b000,
        1.5: 0b001,
        3: 0b010,
        7.5: 0b011,
        15: 0b100,  # Default
        30: 0b101,
        75: 0b110,
        220: 0b111
    }
    assert samples_avgd_per_output in samples_to_bin, "Invalid number of samples averaged per output"
    assert data_rate_hz in data_rate_to_bin, "Invalid data output rate"

    #data_rate_to_bin = {: 0b00, 2: 0b01, 4: 0b10, 8: 0b11}
    reg_a_config = samples_to_bin[samples_avgd_per_output] << 5
    reg_a_config |= data_rate_to_bin[data_rate_hz] << 2
    if temperature_compensation:
        reg_a_config |= 0x80

    print(f"Samples averaged per output (binary): {format(samples_to_bin[samples_avgd_per_output], '02b')}")
    print(f"Data output rate (binary): {format(data_rate_to_bin[data_rate_hz], '03b')}")
    print(f"Temperature compensation bit (binary): {'1' if temperature_compensation else '0'}")
    print(f"reg_a_config in binary: {format(reg_a_config, '08b')}")

    # Configure HMC5983 for continuous measurement mode
    bus.write_byte_data(HMC5983_ADDR, 0x00, reg_a_config)  # Configuration Register A
    bus.write_byte_data(HMC5983_ADDR, 0x01, 0xE0)  # Configuration Register B
    bus.write_byte_data(HMC5983_ADDR, 0x02, 0x00)  # Continuous mode 

    time.sleep(0.1)  # Delay for stability

def read_hmc5983():
    # Read 6 bytes of data from HMC5983
    data = bus.read_i2c_block_data(HMC5983_ADDR, 0x03, 6)
    print(data)

    # Display the binary representation of the first two bytes for x
    print(f"X MSB in binary: {format(data[0], '08b')}")
    print(f"X LSB in binary: {format(data[1], '08b')}")
    print(f"Y MSB in binary: {format(data[4], '08b')}")
    print(f"Y LSB in binary: {format(data[5], '08b')}")
    # Print the binary representation of the combined MSB and LSB for X before two's complement conversion
    print(f"Combined X in binary before two's complement: {format((data[0] << 8) | data[1], '016b')}")

    # Convert the data from two's complement to signed integers
    hx = (data[0] << 8) | data[1]
    hz = (data[2] << 8) | data[3]
    hy = (data[4] << 8) | data[5]

    if hx > 0x07FF:
        hx = 0xFFFF - hx
    if hz > 0x07FF:
        hz = 0xFFFF - hz
    if hy > 0x07FF: 
        hy = 0xFFFF - hy
    #x = twos_complement((data[0] << 8) | data[1])
    #x = (data[0] << 8) | data[1]
    #z = twos_complement((data[2] << 8) | data[3])
    #z = (data[2] << 8) | data[3]
    #y = twos_complement((data[4] << 8) | data[5])
    #y = (data[4] << 8) | data[5]
    H = 0

    if hy == 0 and hx > 0:
        H = 180.0
    if hy == 0 and hx <= 0:
        H = 0.0
    if hy > 0:
        H = 90 - math.atan(hx/hy) * 180 / math.pi
    if hy < 0:
        H = 270 - math.atan(hx/hy) * 180 / math.pi
    print(f'H: {H}')
    return hx, hy, hz

def twos_complement(val):
    # If the MSB (16th bit) is set, the number is negative.
    if val & (1 << 15):
        # Convert from two's complement to a negative integer
        val = val - (1 << 16)
    return val

def calculate_heading(magRawX, magRawY):
    return 180 * math.atan2(magRawY, magRawX)/math.pi


# Test cases for twos_complement function
def test_twos_complement():
    # Test with a positive number that doesn't change
    assert twos_complement(0x0001) == 1, "Test with 1 failed"
    # Test with the maximum positive value before overflow
    assert twos_complement(0x7FFF) == 32767, "Test with 32767 failed"
    # Test with a negative number, -1 in two's complement
    assert twos_complement(0xFFFF) == -1, "Test with -1 failed"
    # Test with the most negative number in two's complement
    assert twos_complement(0x8000) == -32768, "Test with -32768 failed"
    # Test with a mid-range negative number
    assert twos_complement(0xFFFE) == -2, "Test with -2 failed"
    print("All two's complement tests passed!")

def test_calculate_heading():
    # Test case 1: Heading due East
    assert calculate_heading(1, 0) == 0, "Test case 1 failed: Heading due East should be 0 degrees."

    # Test case 2: Heading due North
    assert calculate_heading(0, 1) == 90, "Test case 2 failed: Heading due North should be 90 degrees."

    # Test case 3: Heading due West
    assert calculate_heading(-1, 0) == 180 or calculate_heading(-1, 0) == -180, "Test case 3 failed: Heading due West should be 180 or -180 degrees."

    # Test case 4: Heading due South
    assert calculate_heading(0, -1) == -90, "Test case 4 failed: Heading due South should be -90 degrees."

    # Test case 5: Northeast diagonal
    expected_heading_NE = 45
    assert abs(calculate_heading(1, 1) - expected_heading_NE) < 1e-6, "Test case 5 failed: Northeast diagonal should be 45 degrees."

    # Test case 6: Southwest diagonal
    expected_heading_SW = -135
    assert abs(calculate_heading(-1, -1) - expected_heading_SW) < 1e-6, "Test case 6 failed: Southwest diagonal should be -135 degrees."

    print("All heading test cases passed!")

if __name__ == "__main__":
    test_twos_complement()
    test_calculate_heading()
    time.sleep(3)
    try:
        initialize_hmc5983()
        while True:
            try:
                x, y, z = read_hmc5983()
                print(f"X: {x}, Y: {y}, Z: {z}")
                print(f'Calculated XY heading: {calculate_heading(x, y)}')
                print(f'Calculated YZ heading: {calculate_heading(y, z)}')
                print(f'Calculated XZ heading: {calculate_heading(x, z)}')
            except Exception as e:
                print(e)
            time.sleep(2)  # Delay for stability

    except KeyboardInterrupt:
        pass

