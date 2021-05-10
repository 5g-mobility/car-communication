import traci
import time
import traci.constants as tc
from obd_emulator import response_generator
import random

from obu import OBU

SUMO_BINARY = "sumo"
SUMO_CMD = [SUMO_BINARY, "-c", "sumo/osm.sumocfg"]

emulator_car_map = {}

def main():

    last_port = 8000
    
    while True:
        # just a variable to verify the max cars that the simulation has
        max_cars = 0

        # initialize response generator
        generator = response_generator.ResponseGenerator()

        traci.start(SUMO_CMD, port=9000)

        while traci.simulation.getMinExpectedNumber() > 0:
            
            list_current_step_cars = traci.vehicle.getIDList()

            if len(list_current_step_cars) > max_cars:
                max_cars = len(list_current_step_cars)
                print(f'Currently, there are {max_cars} car(s) sending information to backend infrastructure.')

            for veh_id in list_current_step_cars:

                position = traci.vehicle.getPosition(veh_id)
                position = traci.simulation.convertGeo(position[0], position[1])
                position = (position[1], position[0])
                speed = traci.vehicle.getSpeed(veh_id)

                if speed > 90:
                    if random.random() <= 0.9955:
                        speed -= ((speed-90) + random.randint(2, 15))
                        
                co2_emissions = traci.vehicle.getCO2Emission(veh_id)

                # verify if its the first time that the car pops on the net
                if not veh_id in emulator_car_map:
                    """ if the car appears on the network for the first time
                        add it to the map
                    """

                    emulator_car_map[veh_id] = OBU(veh_id, generator, port=last_port)
                    emulator_car_map[veh_id].connect2OBD2(position, speed, co2_emissions)
                    last_port+=1
                    if last_port > 8005:
                        last_port = 8000
                    
                else:
                    """ if the car was already initialized
                        just update it
                    """
                    emulator_car_map[veh_id].obd2.update(position, speed, co2_emissions)

                # send information of the vehicle to the RSU
                emulator_car_map[veh_id].forward_info_2_RSU()
                #print(f'Car with id {veh_id} sent his data to RSU')                

            traci.simulationStep()

            # simulate the delay of 1 second
            # cars should send data each second
            time.sleep(1)

        traci.close()

        print(f'Max of cars sending data to the backend infrastructure was {max_cars}.')

        # close sockets
        for obu in emulator_car_map.values():
            obu.close()

if __name__ == "__main__":
    main()