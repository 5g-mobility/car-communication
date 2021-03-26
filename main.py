import argparse
import obd

def main(mode):
    print(mode)
     

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--mode', help='Select either "emulator" mode or "vehicle" mode', default="emulator")
    args = parser.parse_args()
    main(args.mode)