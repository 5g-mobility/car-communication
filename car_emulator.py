from enum import Enum

"""
Enumerate with commands available
"""
class commands(Enum):
    RPM = 12
    SPEED = 13
    RUN_TIME = 31
    AMBIANT_AIR_TEMP = 70


"""
Class with the main functionalities
"""
class OBD:

    def __init__(self):
        print('Conexão com dispositivo mágico efetuado com sucesso! Pronto para emular')

    def query(self, command):
        print('efetuando query')
        pass



if __name__ == '__main__':
    connection = OBD()
    connection.query(commands.RPM)
