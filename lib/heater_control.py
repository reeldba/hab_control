# -------------------------------------------------------------------------
# Heater Control.This is a stub for the code that will transmit RF signals
# to the remote heater unit 
# -------------------------------------------------------------------------
def heater_control(heater_config, desired_state):
    """
    """
    import sys
    from datetime import datetime

    # step 1 get the current state of the file
    ts=datetime.datetime.utcnow()	

    try:
        with open(heater_config.get('state_file'), "r") as heater_state_file:
            recorded_state=heater_state_file.read()

    except IOError as er:
        sys.stderr.write("Error reading from state file %s: %s",
                heater_config.get('state_file'), str(er)
        sys.exit(1)

    if desired_state == 1:
        if recorded_state == 'ON':
            print "Heater state remains on"
        else:
            recorded_state = 'ON'
            # call code send here
            print "Turning Heater On."

    if desired_state == 0:
        if recorded_state == 'ON':
            print "Turning Heater off."
            recorded_state = 'OFF'
            # call code send here
        else:
            print "Heater state remains off"

    try:
        with open(heater_config.get('state_file'), "w") as heater_state_file:
            recorded_state=heater_state_file.write(recorded_state)
            heater_state_file.close()

    except IOError as er:
        sys.stderr.write("Error reading from state file %s: %s",
                heater_config.get('state_file'), str(er)
        sys.exit(1)
