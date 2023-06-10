from serial import Serial
from time import sleep

arduino = Serial(port="/dev/tty.usbmodem14201", baudrate=115200, timeout=1)


def write(data):
    # check if previous data has been sent
    # sentSoFar = arduino.readline()
    # print(f"begin write {sentSoFar}")

    # if not "\\n" in str(sentSoFar) and not not sentSoFar:
    #     print("Not finished writing")
    #     return

    arduino.write(bytes(data, "utf-8"))
    print(f"wrote {data}")
    sleep(0.05)
    response = arduino.readline().decode()
    print(response)
    return response
