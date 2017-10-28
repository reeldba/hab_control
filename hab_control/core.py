#!/usr/bin/env python
"""
"""

import logging
import logging.config

logging.config.fileConfig('logging.conf')
logging.getLogger('root')


def update_thinkspeak(measures):
    """
    """
    import requests
    from config import thinkspeak

    try:
        request=requests.post(
                thinkspeak.get('update_url'),
                data={
                    'api_key': thinkspeak.get('write_key'),
                    'field1' : measures.get('temperature'),
                    'field2' : measures.get('humidity'),
                    'field3' : measures.get('message')
                    }
                )
    except Exception as err:
        sys.stderr.write("Error posting to thinkspeak. {0}".format(err.strerror))



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
    import time

    logging.debug('reading Adafruit_DHT sensor')

    attempt=0
    while attempt < 9:
        logging.debug('attempt %d',attempt)
        try:
            humidity,temperature = Adafruit_DHT.read_retry(sensor, sensor_pin)

            # attempt to validate the readings
            if (humidity > 0 and humidity < 100) and (temperature > 0 and temperature < 100 ):
                break

        except Exception as e:
            print str(e)

        attempt = attempt + 1
        time.sleep(1)
        

    return humidity, temperature


def setup_logging(log_file_name, log_level):
    """
    set up logging
    """
    import logging
    from config import logsetup
    from logging.handlers import RotatingFileHandler
    
    logger = logging.getLogger()
    logger.setLevel(log_level)
    handler = logging.handlers.RotatingFileHandler(log_file_name,
            maxBytes=logsetup.get('maxbytes'),
            backupCount=logsetup.get('backupCount')
            )
    formatter = logging.Formatter(logsetup.get('format').get('format_string'),
            logsetup.get('format').get('time_string')
            )
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
    import subprocess
    import config 

    #from heater_control import heater_control

    global logging

    #thinkspeak_file=cfg['hab_control'].get('thinkspeak')
    #thinkspeak_cfg = get_config_json(thinkspeak_file)

    #logging=setup_logging(config.log_file, logging.DEBUG)

    logging.info('Startup')

    SENSOR = config.sensor_id
    SENSOR_PIN = config.sensor_pin
    TARGET_TEMP = config.target_temp
    LOWER_CONTROL_TEMP = config.lower_control_temp
    LOWER_ALERT_TEMP = config.lower_alert_temp
    UPPER_ALERT_TEMP = config.upper_alert_temp
    UPPER_CONTROL_TEMP = config.upper_control_temp

    remotes = config.remotes

    heater_list = sorted(remotes, key=lambda k: k['watts'])

    logging.info(heater_list[0].get('label'))

    humidity,temperature = read_sensor(SENSOR, SENSOR_PIN)
    
    logging.debug("RH=%6.2f%%, T=%6.2fC",humidity, temperature)

    if temperature > UPPER_ALERT_TEMP:
        logging.critical("T exceeds %6.2fC upper alert limit", UPPER_ALERT_TEMP)
        subprocess.call([config.codesend, heater_list[0].get('off'), "-l", heater_list[0].get('off-pulse')])
        subprocess.call([config.codesend, heater_list[1].get('off'), "-l", heater_list[1].get('off-pulse')])

    if temperature > UPPER_CONTROL_TEMP and temperature <= UPPER_ALERT_TEMP:
        logging.debug("T above %6.2fC uppert alert limit", UPPER_CONTROL_TEMP)
        subprocess.call([config.codesend, heater_list[0].get('off'), "-l", heater_list[0].get('off-pulse')])
        subprocess.call([config.codesend, heater_list[1].get('off'), "-l", heater_list[1].get('off-pulse')])

    if temperature >= TARGET_TEMP and temperature <= UPPER_CONTROL_TEMP:
        logging.debug("T nominal. Heaters off")
        logging.debug("Disable %s". heater_list[0].get('label'))
        subprocess.call([config.codesend, heater_list[0].get('off'), "-l", heater_list[0].get('off-pulse')])
        subprocess.call([config.codesend, heater_list[1].get('off'), "-l", heater_list[1].get('off-pulse')])

    if temperature < TARGET_TEMP and temperature >= LOWER_CONTROL_TEMP:
        logging.debug("T below target. Enable lowest power heat")
        logging.debug("Enable %s". heater_list[0].get('label'))
        logging.debug("Disable %s". heater_list[1].get('label'))
        subprocess.call([config.codesend, heater_list[0].get('on'), "-l", heater_list[0].get('on-pulse')])
        subprocess.call([config.codesend, heater_list[1].get('off'), "-l", heater_list[1].get('off-pulse')])

    if temperature < LOWER_CONTROL_TEMP and temperature > LOWER_ALERT_TEMP:
        logging.debug("T below target. Enable all heaters")
        logging.debug("Enable %s". heater_list[0].get('label'))
        logging.debug("Enable %s". heater_list[1].get('label'))
        subprocess.call([config.codesend, heater_list[0].get('on'), "-l", heater_list[0].get('on-pulse')])
        subprocess.call([config.codesend, heater_list[1].get('on'), "-l", heater_list[1].get('on-pulse')])


    if temperature <= LOWER_ALERT_TEMP:
        logging.debug("T below lower alert. heaters not keeping up")

    update_thinkspeak({'humidity':humidity, 'temperature':temperature, 'message':'update'})

if __name__ == "__main__":
    import sys
    try:
        main()
        sys.exit(0)
    except Exception as e:
        raise e
