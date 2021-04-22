import traci
import traci.constants as tc
import time


PORT = 8000
# correr o sumo: sumo -c osm.sumocfg --remote-port 8000

def main():

    traci.init(PORT)
    while traci.simulation.getMinExpectedNumber() > 0:
       
        for veh_id in traci.vehicle.getIDList():
            x, y = traci.vehicle.getPosition(veh_id)
            position = traci.simulation.convertGeo(x, y)
            print("vehicle_id ", veh_id, ": ", position, " ",  traci.vehicle.getCO2Emission(veh_id))

            time.sleep(2)
        traci.simulationStep()

        # print(traci.vehicle.getSubscriptionResults("vehID"))
    time.sleep(5)
    #traci.close()




if __name__ == "__main__":
    main()