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

    payload={'api_key': thinkspeak.get('write_key')}
    payload.update(measures)

    logging.debug('updating thinkspeak with %s', payload)

    try:
        request=requests.post(
                thinkspeak.get('update_url'),
                data=payload
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


def heater_control(heater, command):
    """
    """
    import config
    import subprocess

    logging.info('heater %s to %s',heater.get('label'), command)

    subprocess.call([config.codesend, heater.get(command), "-l", heater.get("{0}-pulse".format(command))])

    
def main():
    """
    """
    import sys
    import logging
    import subprocess
    import config 

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

    humidity,temperature = read_sensor(SENSOR, SENSOR_PIN)
    
    logging.info("Reading is RH=%6.2f%%, T=%6.2fC",humidity, temperature)

    if temperature > UPPER_ALERT_TEMP:
        logging.warn("temp %6.2fC exceeds alert limit %6.2fC", temperature, UPPER_ALERT_TEMP)
        heater_list[0]['state']=0
        heater_list[1]['state']=0
        heater_control(heater_list[0],'off')
        heater_control(heater_list[1],'off')

    if temperature > UPPER_CONTROL_TEMP and temperature <= UPPER_ALERT_TEMP:
        logging.info("temp %6.2fC exceeds upper control limit %6.2fC", temperature, UPPER_CONTROL_TEMP)
        heater_list[0]['state']=0
        heater_list[1]['state']=0
        heater_control(heater_list[0],'off')
        heater_control(heater_list[1],'off')

    if temperature >= TARGET_TEMP and temperature <= UPPER_CONTROL_TEMP:
        logging.info("temp %6.2fC in comfort range. all heaters off",temperature)
        logging.debug("Disable %s", heater_list[0].get('label'))
        heater_list[0]['state']=0
        heater_list[1]['state']=0
        heater_control(heater_list[0],'off')
        heater_control(heater_list[1],'off')

    if temperature < TARGET_TEMP and temperature >= LOWER_CONTROL_TEMP:
        logging.info("temp %6.2fC below target %6.2fC. Enable lowest power heat", temperature, TARGET_TEMP)
        logging.debug("Enable %s", heater_list[0].get('label'))
        logging.debug("Disable %s", heater_list[1].get('label'))
        heater_list[0]['state']=1
        heater_list[1]['state']=0
        heater_control(heater_list[0],'on')
        heater_control(heater_list[1],'off')

    if temperature < LOWER_CONTROL_TEMP and temperature > LOWER_ALERT_TEMP:
        logging.info('temp %6.2fC below %6.2fC, enable all heaters.',temperature, LOWER_CONTROL_TEMP)
        logging.debug("T below target. Enable all heaters")
        logging.debug("Enable %s", heater_list[0].get('label'))
        logging.debug("Enable %s", heater_list[1].get('label'))
        heater_list[0]['state']=1
        heater_list[1]['state']=1
        heater_control(heater_list[0],'on')
        heater_control(heater_list[1],'on')


    # we need to send the turn on pulse because the 
    # system could start with the hab below temp.
    if temperature <= LOWER_ALERT_TEMP:
        logging.info('%6.2fC below lower alert limit %6.2fC, heaters not keeping up.',temperature, LOWER_ALERT_TEMP)
        logging.warning("T below lower alert. heaters not keeping up")
        heater_list[0]['state']=1
        heater_list[1]['state']=1
        heater_control(heater_list[0],'on')
        heater_control(heater_list[1],'on')

    update_thinkspeak({'field2': '{0:5.2f}'.format(humidity), 'field1':'{0:5.2f}'.format(temperature), 
        'field3' : heater_list[0]['state'],
        'field4' : heater_list[1]['state']})

if __name__ == "__main__":
    import sys
    import traceback
    try:
        main()
        sys.exit(0)
    except Exception , e:
        traceback.print_exc(file=sys.stdout)
        raise e
        sys.exit(-1)
