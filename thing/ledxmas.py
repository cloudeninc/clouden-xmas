#!/usr/bin/env python
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt
import json

handler = None

# Custom MQTT message callback
def customCallback(client, userdata, message):
	#print("Received a new message: ")
	print(message.payload)
	#print("from topic: ")
	#print(message.topic)
	#print("--------------\n\n")
	try:
		msg = json.loads(message.payload)
		handler.handle_message(msg)
	except:
		pass

# Usage
usageInfo = """Usage:

Use certificate based mutual authentication:
python ledxmas.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

Use MQTT over WebSocket:
python ledxmas.py -e <endpoint> -r <rootCAFilePath> -w

Type "python ledxmas.py -h" for available options.
"""
# Help info
helpInfo = """-e, --endpoint
	Your AWS IoT custom endpoint
-r, --rootCA
	Root CA file path
-c, --cert
	Certificate file path
-k, --key
	Private key file path
-w, --websocket
	Use MQTT over WebSocket
-h, --help
	Help information


"""

# Read in command-line parameters
useWebsocket = False
host = ""
rootCAPath = ""
certificatePath = ""
privateKeyPath = ""
useGpio = False
useMidi = False
clientId = None
try:
	opts, args = getopt.getopt(sys.argv[1:], "hgmwe:i:k:c:r:", ["help", "endpoint=", "key=", "id=", "cert=","rootCA=", "websocket", "gpio", "midi"])
	if len(opts) == 0:
		raise getopt.GetoptError("No input parameters!")
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			print(helpInfo)
			exit(0)
		if opt in ("-e", "--endpoint"):
			host = arg
		if opt in ("-r", "--rootCA"):
			rootCAPath = arg
		if opt in ("-c", "--cert"):
			certificatePath = arg
		if opt in ("-k", "--key"):
			privateKeyPath = arg
		if opt in ("-w", "--websocket"):
			useWebsocket = True
		if opt in ("-g", "--gpio"):
			useGpio = True
		if opt in ("-m", "--midi"):
			useMidi = True
		if opt in ("-i", "--id"):
			clientId = arg
except getopt.GetoptError:
	print(usageInfo)
	exit(1)

# Missing configuration notification
missingConfiguration = False
if not host:
	print("Missing '-e' or '--endpoint'")
	missingConfiguration = True
if not rootCAPath:
	print("Missing '-r' or '--rootCA'")
	missingConfiguration = True
if not useWebsocket:
	if not certificatePath:
		print("Missing '-c' or '--cert'")
		missingConfiguration = True
	if not privateKeyPath:
		print("Missing '-k' or '--key'")
		missingConfiguration = True
if missingConfiguration:
	exit(2)

if not useMidi and not useGpio:
	print("Must specify --gpio or --midi")
	exit(2)

if not clientId:
	print("Must specify --id")
	exit(2)

if useMidi:
	import midi
	handler = midi
else:
	import gpio
	handler = gpio

# Configure logging
logger = logging.getLogger("AWSIoTPythonSDK.core")
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
	myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId, useWebsocket=True)
	myAWSIoTMQTTClient.configureEndpoint(host, 443)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
	myAWSIoTMQTTClient = AWSIoTMQTTClient(clientId)
	myAWSIoTMQTTClient.configureEndpoint(host, 8883)
	myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

handler.init()

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("ledxmas", 1, customCallback)
time.sleep(2)

# Publish to the same topic in a loop forever
#loopCount = 0
while True:
	#myAWSIoTMQTTClient.publish("ledxmas", "New Message " + str(loopCount), 1)
	#loopCount += 1
	time.sleep(0.1)
	handler.tick()
