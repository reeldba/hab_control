#!/usr/bin/env python
"""
"""

import sys
import os
import stat
import fcntl
import gpiozero
import RPi.GPIO as GPIO
import datetime
import Adafruit_DHT
import logging
import time
import json


# -------------------------------------------------------------------------
# MAIN LINE OF CODE STARTS HERE
# -------------------------------------------------------------------------

# Step 1 - record the temperature and humidity
humidity,temperature = Adafruit_DHT.read_retry(SENSOR,SENSOR_PIN)

# Step 2 - Decide what to do based on the readings from the Sensor
if humidity is None or temperature is None:
	# couldn't get a reading on one or both of the measures
	record_observation(field1=temperature,\
		field2=humidity, \
		field3="failed to get a reading")

else:
	record_observation(field1=temperature, field2=humidity, field3="OK")
	if temperature < TARGET_TEMPERATURE:
		if temperature < LOWER_CONTROL_LIMIT:
			print("temperature {0:0.1f} lower than lower control limit of {1:0.1f}".format(temperature, LOWER_CONTROL_LIMIT))
			rc=HeaterControl(1)
			if temperature < LOWER_ALERT_LIMIT:
				# alert someone
				print("temperature {0:0.1f} lower than lower alert limit of {1:0.1f}".format(temperature, LOWER_ALERT_LIMIT))
				rc=HeaterControl(1)
		else:
			print("temperature {0:0.1f} lower than target {1:0.1f} but higher than lower control ofof {2:0.1f}".format(temperature, TARGET_TEMPERATURE, LOWER_CONTROL_LIMIT))
			rc=HeaterControl(1)


	elif temperature > TARGET_TEMPERATURE:
		if temperature > UPPER_CONTROL_LIMIT:
			print("temperature {0:0.1f} greater than upper control limit {1:0.1f}".format(temperature, UPPER_CONTROL_LIMIT))
			rc=HeaterControl(0)
			if temperature > UPPER_ALERT_LIMIT:
				print("temperature {0:0.1f} greater than upper alert limit {1:0.1f}".format(temperature, UPPER_ALERT_LIMIT))
				# alert someone
	else:
		# must have equaled it
		print("temperature {0:0.1f} at target {1:0.1f}".format(temperature, TARGET_TEMPERATURE ))
		print "="

# =========================================================================
# clean up
# =========================================================================

# =========================================================================
#
# =========================================================================

# vim: set number on:ts=4
