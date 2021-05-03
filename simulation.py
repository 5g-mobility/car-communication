import traci
import time
import traci.constants as tc

from obu import OBU

SUMO_BINARY = "sumo"
SUMO_CMD = [SUMO_BINARY, "-c", "sumo-exp/osm.sumocfg"]

emulator_car_map = {}

def main():
    traci.start(SUMO_CMD, port=9000)

    while traci.simulation.getMinExpectedNumber() > 0:
        
            for veh_id in traci.vehicle.getIDList():

                position = traci.vehicle.getPosition(veh_id)
                position = traci.simulation.convertGeo(position[0], position[1])
                position = (position[1], position[0])
                speed = traci.vehicle.getSpeed(veh_id)
                co2_emissions = traci.vehicle.getCO2Emission(veh_id)

                # verify if its the first time that the car pops on the net
                if not veh_id in emulator_car_map:
                    """ if the car appears on the network for the first time
                        add it to the map
                    """
                    emulator_car_map[veh_id] = OBU(veh_id)
                    emulator_car_map[veh_id].connect2OBD2(position, speed, co2_emissions)
                else:
                    """ if the car was already initialized
                        just update it
                    """
                    emulator_car_map[veh_id].obd2.update(position , speed, co2_emissions)

                # print(emulator_car_map[veh_id])

                # send information of the vehicle to the RSU
                emulator_car_map[veh_id].forward_info_2_RSU()
                print(f'Car with id {veh_id} sent his data to RSU')
                
                # for not be blocked by the api
                time.sleep(1.1)

            traci.simulationStep()

            # print(traci.vehicle.getSubscriptionResults("vehID"))

    traci.close()

    # TODO para aumentar um nível de realismo podia-se criar várias RSU e os carros iam
    # ligando-se mediante a sua localização

    # TODO fazer lógica para que os carros que já chegaram ao destino possam terminar as suas ligações ao RSU
    # fechar as sockets
    for obu in emulator_car_map.values():
        obu.close()

if __name__ == "__main__":
    main()