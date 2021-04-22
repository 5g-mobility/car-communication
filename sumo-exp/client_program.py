import traci
import time
import traci.constants as tc

import obd_emulator

SUMO_BINARY = "sumo"
SUMO_CMD = [SUMO_BINARY, "-c", "osm.sumocfg"]

obd2EmulatorMap = {}

class Vehicle:
    def __init__(self, position, speed, co2Emissions):
        self.obdEmulator = obd_emulator.OBDEmulator()
        self.position = position
        self.speed = speed
        self.co2Emissions = co2Emissions
        
        # TODO initialize the rest of the params


    def update(self, position, speed, co2Emissions):
        self.position = position
        self.speed = speed
        self.co2Emissions = co2Emissions

        # TODO update the rest of the params


    def get_light_sensor():
        return self.obdEmulator.query(commands.LIGHT_SENSOR)


def main():
    traci.start(SUMO_CMD, port=8000)

    while traci.simulation.getMinExpectedNumber() > 0:
        
            for veh_id in traci.vehicle.getIDList():

                position = traci.vehicle.getPosition(veh_id)
                speed = traci.vehicle.getSpeed(veh_id)
                co2Emissions = traci.vehicle.getCO2Emission(veh_id)

                # verify if its the first time that the car pops on the net
                if not veh_id in obd2EmulatorMap:
                    """ if the car appears on the network for the first time
                        add it to the map
                    """
                    obd2EmulatorMap[veh_id] = Vehicle(position, speed, co2Emissions)
                else:
                    """ if the car was already initialized
                        just update it
                    """
                    obd2EmulatorMap[veh_id].update(coord, vel, emissions)
                # se nao estiver criar instancia obd2
                # obdEmu = Obd(a    faf, adad)

                # position = traci.simulation.convertGeo(x, y)
                print("vehicle_id ", veh_id, ": ", position, " ",  traci.vehicle.getCO2Emission(veh_id))
                # print(f"Antes do sleep:{traci.simulation.getTime()}")
            traci.simulationStep(1)

            # print(traci.vehicle.getSubscriptionResults("vehID"))

    traci.close()

if __name__ == "__main__":
    main()