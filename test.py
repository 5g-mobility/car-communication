# import obdEmulator as obd

# connection = obdEmulator.OBD()
# connection.query(obdEmulator.commands.RPM)


# connection.close()

import argparse
# import obd
import obdEmulator as obd
import time

# a callback that prints every new value to the console
def new_rpm(r):
    # print(r.value)
    print(f' Na callback: {r}')

def main(mode):
    if mode == 0:
        connection = obd.Async()
    elif mode == 1:
        connection = obd.Async("/dev/tty.OBDLinkMX68078-STN-SPP")

    connection.watch(obd.commands.RPM, callback=new_rpm)
    connection.start()

    # the callback will now be fired upon receipt of new values

    time.sleep(10)
    connection.stop()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mode', help='Select either 0 (emulator mode) or 1 (vehicle mode)', default=0,type=int, choices=[0, 1])
    args = parser.parse_args()
    main(args.mode)