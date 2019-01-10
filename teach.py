#!/usr/bin/env python3

import pyshark
import sys
import os.path
from payload import Payload
from NN import NN
import pprint
import TrainingSample
import random
import OutputMapper

def man():
	print("Usage: %s <NN Weights Path> [Type(SSH, HTTP, FTP) DumpPath] ..." % sys.argv[0])

if len(sys.argv) < 3:
	man()
	sys.exit(1)

weightsPath = sys.argv[1]

sourceFiles = {}
for i in range(2, len(sys.argv), 2):
	currentType = sys.argv[i]
	currentPath = sys.argv[i + 1]

	if os.path.isfile(currentPath) == False:
		print("[%s] does not exist. Skipping." % currentPath)
		continue
	
	if currentType in sourceFiles:
		print("U [%s:%s]" % (currentType, currentPath))
		sourceFiles[currentType].append(currentPath)
	else:
		print("I [%s:%s]" % (currentType, currentPath))
		sourceFiles[currentType] = [currentPath]

if len(sourceFiles) == 0:
	print("No files were added. Exiting.")
	sys.exit(1)


nn = NN(Payload.vectorSize(), OutputMapper.vectorSize)

if os.path.isfile(weightsPath):
	nn.load(weightsPath)

samples = TrainingSample.TrainingSampleBatch()
for trafficType in sourceFiles.keys():
	for filePath in sourceFiles[trafficType]:
		cap = pyshark.FileCapture(filePath)
		for packet in cap:
			try:
				sample = TrainingSample.TrainingSample(
					Payload.fromPySharkCapture(packet),
					trafficType
				)
				samples.add(sample)
			except AttributeError as ae:
				print(ae)

samples.shuffle()
vectors = samples.toVectors()

nn.train(vectors[0], vectors[1])
nn.save(weightsPath)


sys.exit(0)

