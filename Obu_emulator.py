import traci
import time
import traci.constants as tc

import obd_emulator

SUMO_BINARY = "sumo"
SUMO_CMD = [SUMO_BINARY, "-c", "sumo-exp/osm.sumocfg"]

obd2EmulatorMap = {}

class Vehicle:
    def __init__(self, position, speed, co2Emissions):
        self.obdEmulator = obd_emulator.OBDEmulator()
        self.position = position
        self.speed = speed
        self.co2Emissions = co2Emissions
        self.update_emu()
        


    def update(self, position, speed, co2Emissions ):
        self.position = position
        self.speed = speed
        self.co2Emissions = co2Emissions

        self.update_emu()

    def update_emu(self):

        # Todo : aleterar a localização para geo coords
        self.obdEmulator.update_location(self.position)
        self.air_temperature = self.obdEmulator.query(obd_emulator.commands.AMBIENT_AIR_TEMP).value
        self.light_sensor = self.obdEmulator.query(obd_emulator.commands.LIGHT_SENSOR).value
        self.rain_sensor = self.obdEmulator.query(obd_emulator.commands.RAIN_SENSOR).value
        self.fog_light = self.obdEmulator.query(obd_emulator.commands.FOG_LIGHTS).value

    def __str__(self):
        return f"Vehicle({self.position}): speed -> {self.speed} m/s \n\t\tCO2 emissions -> {self.co2Emissions} mg/s" + \
        f"\n\t\tAir Temperature -> {self.air_temperature} ºC" + \
        f"\n\t\tDay -> {self.light_sensor}" + \
        f"\n\t\tRain -> {self.rain_sensor}" + \
        f"\n\t\tFog -> {self.fog_light}"


def main():
    traci.start(SUMO_CMD, port=8000)

    while traci.simulation.getMinExpectedNumber() > 0:
        
            for veh_id in traci.vehicle.getIDList():

                position = traci.vehicle.getPosition(veh_id)
                position = traci.simulation.convertGeo(position[0], position[1])
                position = (position[1], position[0])
                speed = traci.vehicle.getSpeed(veh_id)
                co2_emissions = traci.vehicle.getCO2Emission(veh_id)

                # verify if its the first time that the car pops on the net
                if not veh_id in obd2EmulatorMap:
                    """ if the car appears on the network for the first time
                        add it to the map
                    """
                    obd2EmulatorMap[veh_id] = Vehicle(position, speed, co2_emissions)
                else:
                    """ if the car was already initialized
                        just update it
                    """
                    obd2EmulatorMap[veh_id].update(position , speed, co2_emissions)

                print(obd2EmulatorMap[veh_id])

                time.sleep(0.5)

            traci.simulationStep()

            # print(traci.vehicle.getSubscriptionResults("vehID"))

    traci.close()

if __name__ == "__main__":
    main()