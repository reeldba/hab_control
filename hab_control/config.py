#
sensor_id = 22
sensor_pin = 23
log_file = "hab_control.log"

# Hedgie's comfort zone is 72-82F (22.2-27.8C)
# 75
target_temp = 23.9              
# 73.5
lower_control_temp = 23.1       
# 72
lower_alert_temp = 22.2         
# 74.5 
upper_control_temp = 23.6       
# 82
upper_alert_temp = 27.7         

codesend = "/home/pi/rfoutlet/codesend"

remotes =  [{
		"remote_id": "0321-4",
		"on": "1119539",
		"on-pulse": "184",
		"off": "1119548",
		"off-pulse": "184",
		"state_file" : "0321-4.state",
		"watts" : 10,
		"label" : "Infrared Lamp"
	}, {
		"remote_id": "0321-5",
		"on": "1119683",
		"on-pulse": "184",
		"off": "1119692",
		"off-pulse": "184",
		"state_file" : "0321-5.state",
		"watts" : 2,
		"label" : "Heating Pad"
	}]

thinkspeak = {
		"read_key": "GQ2QWJ82ZDJEPFQV",
		"write_key": "Y52EA5PMQAZL7L03",
		"channel_id": "204433",
		"update_url": "https://api.thingspeak.com/update.json"
	}

logsetup = {
    "maxbytes" : 33554432, 
    "backupCount" : 5,
    "format" : { 
        "format_string" : "[%(filename)s[%(lineno)s] %(funcName)s()] %(asctime)s %(levelname)s %(message)s", 
        "time_string" : "%Y-%m-%d %H:%M:%S"
    }
}
