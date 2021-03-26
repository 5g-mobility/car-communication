import obdEmulator

connection = obdEmulator.OBD()
connection.query(obdEmulator.commands.RPM)


connection.close()