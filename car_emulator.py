from enum import Enum

"""
Enumerate with commands available
"""
class commands(Enum):
    RPM = 1
    SPEED = 2

"""
Class with the main functionalities
"""
class OBD:

    def __init__(self):
        print('Conexão com dispositivo mágico efetuado com sucesso! Pronto para emular')
        print(repr(commands.RPM))



if __name__ == '__main__':
    emulator = OBD()
