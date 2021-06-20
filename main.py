import argparse
import obd
import time
import obd_emulator

# a callback that prints every new value to the console
def new_rpm(r):
    print(r.value)

def main(mode):
    # turn on debug mode
    obd.logger.setLevel(obd.logging.DEBUG)
    if mode == 0:
        connection = obd_emulator.Async()
        connection.start_monitoring()           # start thread with response generator
    elif mode == 1:
        connection = obd.OBD("/dev/tty.OBDLinkMX68078-STN-SPP")

    connection.watch(obd_emulator.commands.RPM, callback=new_rpm)
    connection.watch(obd_emulator.commands.SPEED, callback=new_rpm)
    connection.watch(obd_emulator.commands.RUN_TIME, callback=new_rpm)
    connection.watch(obd_emulator.commands.AMBIENT_AIR_TEMP, callback=new_rpm)
    connection.watch(obd_emulator.commands.LIGHT_SENSOR, callback=new_rpm)
    connection.watch(obd_emulator.commands.FOG_LIGHTS, callback=new_rpm)
    connection.watch(obd_emulator.commands.RAIN_SENSOR, callback=new_rpm)
    connection.watch(obd_emulator.commands.CO2_EMISSIONS, callback=new_rpm)
    
    connection.start()

    # the callback will now be fired upon receipt of new values

    time.sleep(120)
    connection.stop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mode', help='Select either 0 (emulator mode) or 1 (vehicle mode, need to change OBD Commands accordingly with vehicle)', default=0,type=int, choices=[0, 1])
    args = parser.parse_args()
    main(args.mode)