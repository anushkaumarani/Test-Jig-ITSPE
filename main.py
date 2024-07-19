import time
import board
import busio
import adafruit_tca9548a
import adafruit_ina219
import digitalio
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
#i2c_new = busio.I2C(scl=board.GP19, sda = board.GP18)
tca = adafruit_tca9548a.TCA9548A(i2c)

ina1 = adafruit_ina219.INA219(tca[0])


led = digitalio.DigitalInOut(board.GP22)
red = digitalio.DigitalInOut(board.GP8)
green = digitalio.DigitalInOut(board.GP7)
amber = digitalio.DigitalInOut(board.GP6)
red.direction = digitalio.Direction.INPUT
green.direction = digitalio.Direction.INPUT
amber.direction = digitalio.Direction.INPUT
led.direction = digitalio.Direction.OUTPUT

csv_file_path = "/voltage_test.csv"

def write_to_csv(data, path):
    with open(path, "a") as f:
        f.write(data + "\n")

header = "ina1_voltage,vcheck,ina1_current,icheck,ina1_power,pcheck"
write_to_csv(header, csv_file_path)
led.value = True
while True:
    ina1_voltage = ina1.bus_voltage
    ina1_current = ina1.current
    ina1_power = ina1.power
    print(ina1_voltage, ina1_current, ina1_power)
    color = "None"
    vcheck = icheck = pcheck = "NA"
    if not red.value:
        color = "red"
    elif not green.value:
        color = "green"
    elif not amber.value:
        color = "amber"
    if color == "red":
        vcheck = "vpass" if 6.05 < ina1_voltage < 6.9 else "vfail"
        icheck = "ipass" if 0.330 < ina1_current < 0.370 else "ifail"
        pcheck = "ppass" if 1.996 < ina1_power < 2.553 else "pfail"
    elif color == "amber":
        vcheck = "vpass" if 6.05 < ina1_voltage < 6.9 else "vfail"
        icheck = "ipass" if 0.330 < ina1_current < 0.370 else "ifail"
        pcheck = "ppass" if 1.996 < ina1_power < 2.553 else "pfail"
    elif color == "green":
        vcheck = "vpass" if 6.05 < ina1_voltage < 6.9 else "vfail"
        icheck = "ipass" if 0.330 < ina1_current < 0.370 else "ifail"
        pcheck = "ppass" if 1.996 < ina1_power < 2.553 else "pfail"
    print(color)
    print(vcheck)
    print(icheck)
    print(pcheck)

    data_line = f"{ina1_voltage},{vcheck},{ina1_current},{icheck},{ina1_power},{pcheck}"
    write_to_csv(data_line, csv_file_path)

    #tca[7].active = False   //Example of disabling an input line (line no 8 in this case)

    time.sleep(1)
led.value = False
