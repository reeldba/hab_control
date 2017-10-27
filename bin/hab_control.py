#!/usr/bin/env python
"""
"""


def main():
    """
    """
    import sys
    import Adafruit_DHT
    from get_config_file import get_config_json

    cfg = get_config_json(sys.argv[1])
    SENSOR = cfg['hab_control'].get('sensor')
    SENSOR_PIN = cfg['hab_control'].get('sensor_pin')
    TARGET_TEMP = cfg['hab_control'].get('target_temp')
    LOWER_CONTROL_TEMP = cfg['hab_control'].get('lower_control_temp')
    LOWER_ALERT_TEMP = cfg['hab_control'].get('lower_alert_temp')
    UPPER_ALERT_TEMP = cfg['hab_control'].get('upper_alert_temp')
    UPPER_CONTROL_TEMP = cfg['hab_control'].get('upper_control_temp')

    humidity,temperature = Adafruit_DHT.read_retry(SENSOR,SENSOR_PIN)
    
    print "relative humidity={0:6.2f}%, temperature={1:6.2f} C".format(humidity, temperature)

    if temperature > UPPER_ALERT_TEMP:
        print "temp is {0:6.2} C above target and {1:6.2} C above upper limit".format(temperature-TARGET_TEMP,temperature-UPPER_ALERT_TEMP)

    if temperature > UPPER_CONTROL_TEMP and temperature <= UPPER_ALERT_TEMP:
        print "temp above target"

    if temperature >= TARGET_TEMP and temperature <= UPPER_CONTROL_TEMP:
        print "temp nominal, no heaters are on."

    if temperature < TARGET_TEMP and temperature >= LOWER_CONTROL_TEMP:
        print "its a little chilly, turn on the least powerful heater"

    if temperature < LOWER_CONTROL_TEMP and temperature > LOWER_ALERT_TEMP:
        print "bring on the more powerful heater"

    if temperature <= LOWER_ALERT_TEMP:
        print "all heaters are on.  heaters are not keeping up"



if __name__ == "__main__":
    main()
