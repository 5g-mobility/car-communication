import traci
import time
import traci.constants as tc

import obd_emulator

SUMO_BINARY = "sumo"
SUMO_CMD = [SUMO_BINARY, "-c", "./sumo-exp/osm.sumocfg"]

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

        x, y = self.position
        # Todo : aleterar a localização para geo coords
        x2, y2 = traci.simulation.convertGeo(x, y)

        self.position = y2, x2

        print(self.position)

        self.obdEmulator.update_location(self.position)
        self.air_temperature = self.obdEmulator.query(obd_emulator.commands.AMBIENT_AIR_TEMP).value
        self.light_sensor = self.obdEmulator.query(obd_emulator.commands.LIGHT_SENSOR).value
        self.rain_sensor = self.obdEmulator.query(obd_emulator.commands.RAIN_SENSOR).value
        self.fog_light = self.obdEmulator.query(obd_emulator.commands.FOG_LIGHTS).value

    def __str__(self) -> str:
        return super().__str__()


def main():
    traci.start(SUMO_CMD, port=8000)

    while traci.simulation.getMinExpectedNumber() > 0:
        
            for veh_id in traci.vehicle.getIDList():

                position = traci.vehicle.getPosition(veh_id)
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
                # se nao estiver criar instancia obd2
                # obdEmu = Obd(a    faf, adad)

                # position = traci.simulation.convertGeo(x, y)
                print(obd2EmulatorMap["veh0"])

                time.sleep(2)
                # print(f"Antes do sleep:{traci.simulation.getTime()}")
            traci.simulationStep()

            # print(traci.vehicle.getSubscriptionResults("vehID"))

    traci.close()




if __name__ == "__main__":
    main()