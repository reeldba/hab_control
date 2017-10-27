def record_observation(field1,field2,field3):
    """
    """
    import requests

    # lets use a common timestamp
    ts=datetime.datetime.utcnow()

    # first thing, lets write the data to the local disk
    try:
            with open("habitat.dat","a") as datafile:
                    datafile.write("{0},{1:0.1f},{2:0.1f},{3:s}\n".format(ts,field1,field2,field3))
    except IOError as er:
            sys.stderr.write("Error writing data {0}".format(er.strerror))

    # next, lets put the data on Thing Speak so we can have a web service
    # watch out for it.	
    try:
            r = requests.post(config['cfg']['thingspeak_update_url'],data={'api_key':config['cfg']['thingspeak_write_key'],'field1':field1,'field2':field2}) 
    except Exception as er:
            sys.stderr.write("Error posting to thingspeak {0}".format(er.strerror))

    # finally, put the readings to the screen
    print("{0}, Temp={1:0.1f}*C, Relative Humidity={2:0.1f}%, {3}".format(ts,field1,field2,field3))

