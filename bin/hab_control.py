#!/usr/bin/env python
"""
"""

def read_sensor(sensor, sensor_pin):
    """
    sample the temp.  at some point, improve this to toss out 
    invalid readings (like 3000% RH and -10 C)

    Arguments
    Sensor  integer constant that tells the DHT lib what kind of sensor
    sensor_pin  which pin is the sensor wired to on the rPi

    Returns
    list    humidity, temperature

    """

    import Adafruit_DHT

    LOGGER.debug('howdy')

    try:
        humidity,temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

    except Exception as e:
        print str(e)

    return humidity, temperature


def setup_logging(log_file_name, log_level):
    """
    set up logging
    """
    import logging
    from logging.handlers import RotatingFileHandler
    
    logger = logging.getLogger()
    logger.setLevel(log_level)
    handler = logging.handlers.RotatingFileHandler(log_file_name,
            maxBytes = 1024*1024*32, 
            backupCount=5)
    formatter = logging.Formatter(
            "[%(filename)s[%(lineno)s] %(funcName)s()] %(asctime)s %(levelname)s %(message)s", "%Y-%m-%d %H:%M:%S")
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    console=logging.StreamHandler()
    console.setLevel(log_level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


def main():
    """
    """
    import sys
    import logging
    from get_config_file import get_config_json
    #from heater_control import heater_control

    global LOGGER

    cfg = get_config_json(sys.argv[1])

    LOGGER=setup_logging(cfg['hab_control'].get('log_file'), logging.DEBUG)

    LOGGER.info('Startup')

    SENSOR = cfg['hab_control'].get('sensor')
    SENSOR_PIN = cfg['hab_control'].get('sensor_pin')
    TARGET_TEMP = cfg['hab_control'].get('target_temp')
    LOWER_CONTROL_TEMP = cfg['hab_control'].get('lower_control_temp')
    LOWER_ALERT_TEMP = cfg['hab_control'].get('lower_alert_temp')
    UPPER_ALERT_TEMP = cfg['hab_control'].get('upper_alert_temp')
    UPPER_CONTROL_TEMP = cfg['hab_control'].get('upper_control_temp')

    remotes_cfg = get_config_json(cfg['hab_control'].get('remotes_cfg'))

    heater_list = sorted(remotes_cfg['remotes'], key=lambda k: k['watts'])

    humidity,temperature = read_sensor(SENSOR, SENSOR_PIN)
    
    LOGGER.debug("RH=%6.2f%%, T=%6.2fC",humidity, temperature)
    #print "relative humidity={0:6.2f}%, temperature={1:6.2f} C".format(humidity, temperature)

    if temperature > UPPER_ALERT_TEMP:
        LOGGER.debug("T exceeds %6.2fC upper alert limit", UPPER_ALERT_TEMP)
        #print "temp is {0:6.2} C above target and {1:6.2} C above upper limit".format(temperature-TARGET_TEMP,temperature-UPPER_ALERT_TEMP)

    if temperature > UPPER_CONTROL_TEMP and temperature <= UPPER_ALERT_TEMP:
        LOGGER.debug("T above %6.2fC uppert alert limit", UPPER_CONTROL_TEMP)

    if temperature >= TARGET_TEMP and temperature <= UPPER_CONTROL_TEMP:
        LOGGER.debug("T nominal. Heaters off")
        LOGGER.debug("Disable %s". heater_list[0].get('label'))

    if temperature < TARGET_TEMP and temperature >= LOWER_CONTROL_TEMP:
        LOGGER.debug("T below target. Enable lowest power heat")
        LOGGER.debug("Enable %s". heater_list[0].get('label'))
        LOGGER.debug("Disable %s". heater_list[1].get('label'))

    if temperature < LOWER_CONTROL_TEMP and temperature > LOWER_ALERT_TEMP:
        LOGGER.debug("T below target. Enable all heaters")
        LOGGER.debug("Enable %s". heater_list[0].get('label'))
        LOGGER.debug("Enable %s". heater_list[1].get('label'))

    if temperature <= LOWER_ALERT_TEMP:
        LOGGER.debug("T below lower alert. heaters not keeping up")


if __name__ == "__main__":
    import sys
    main()
    sys.exit(0)
