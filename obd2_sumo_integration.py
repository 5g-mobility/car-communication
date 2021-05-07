import obd_emulator

class OBD2:
    def __init__(self, generator, position, speed, co2Emissions):
        self.obdEmulator = obd_emulator.OBDEmulator(generator)
        self.position = position
        self.speed = speed
        self.co2Emissions = co2Emissions
        self.update_emu()

    @property
    def get_position(self):
        return self.position

    @property
    def get_speed(self):
        return self.speed

    @property
    def get_co2_emissions(self):
        return self.co2Emissions

    @property
    def get_air_temperature(self):
        return self.air_temperature
    
    @property
    def get_light_sensor(self):
        return self.light_sensor

    @property
    def get_rain_sensor(self):
        return self.rain_sensor

    @property
    def get_fog_light_sensor(self):
        return self.fog_light

    def update(self, position, speed, co2Emissions ):
        self.position = position
        self.speed = speed
        self.co2Emissions = co2Emissions

        self.update_emu()

    def update_emu(self):
        # update the location and params of the obd2 device using the api
        self.obdEmulator.update_location(self.position)
        self.air_temperature = self.obdEmulator.query(obd_emulator.commands.AMBIENT_AIR_TEMP).value
        self.light_sensor = self.obdEmulator.query(obd_emulator.commands.LIGHT_SENSOR).value
        self.rain_sensor = self.obdEmulator.query(obd_emulator.commands.RAIN_SENSOR).value
        self.fog_light = self.obdEmulator.query(obd_emulator.commands.FOG_LIGHTS).value

    def __str__(self):
        return f"OBD2 measures({self.position}): speed -> {self.speed} m/s \n\t\tCO2 emissions -> {self.co2Emissions} mg/s" + \
        f"\n\t\tAir Temperature -> {self.air_temperature} ºC" + \
        f"\n\t\tDay -> {self.light_sensor}" + \
        f"\n\t\tRain -> {self.rain_sensor}" + \
        f"\n\t\tFog -> {self.fog_light}"