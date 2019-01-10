#!/usr/bin/sudo python3

import pyshark
import sys
import os.path
from payload import Payload
from NN import NN
import pprint
from TrainingSample import TrainingSample
import random
import OutputMapper

def man():
	print("Usage: %s <NN Weights Path> Protocol N-packets")

if len(sys.argv) < 3:
	man()
	sys.exit(1)

weightsPath = sys.argv[1]
protocol = sys.argv[2]

if protocol == 'SSH':
	port = 22
elif protocol == 'FTP':
	port = 21
elif protocol == 'HTTP':
	port = 80
else:
	assert(False)

if len(sys.argv) > 3:
	iterations = int(sys.argv[3])
else:
	iterations = 10


interface = 'enp3s0'
filter = 'tcp port %d' % port

cap = pyshark.LiveCapture(interface = interface, bpf_filter = filter)
nn = NN(Payload.vectorSize(), OutputMapper.vectorSize)

nn.load(weightsPath)

for i in range(iterations):
	try:
		cap.sniff(packet_count = 1)
		packet = cap.next()
		payload = Payload.fromPySharkCapture(packet)
		res = nn.predict(payload.toVector())

		output = OutputMapper.fromVector(res)
		for protocolRes in output:
			print("%s: %f, " % protocolRes, end = '')
		print()
	except KeyboardInterrupt:
		break
	except Exception(ex):
		print("Error has ocurred: " + ex)
		sys.stdout.flush()
		continue
	
	i += 1
	sys.stdout.flush()

sys.exit(0)
