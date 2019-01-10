#!/usr/bin/env python3

from operator import itemgetter

__protocols = ['SSH', 'HTTP', 'FTP']
vectorSize = 4

assert(len(__protocols) <= vectorSize)

def getProtocolId(protocolName):
	found = False
	for index, protocol in enumerate(__protocols):
		if protocol == protocolName:
			return index
	

def getProtocolName(protocolId):
	if protocolId >= len(__protocols):
		return 'UNKNOWN'
	
	return __protocols[protocolId]


def toVector(protocolName):
	outputVector = [0.] * vectorSize

	protocolId = getProtocolId(protocolName)
	if protocolId is None:
		raise ValueError("Unsupported traffic type (%s)" % self.trafficType)

	outputVector[protocolId] = 1.
	return outputVector


def fromVector(vector):
	indexedVector = list(enumerate(vector[0]))
	sorted(indexedVector, key = itemgetter(1), reverse = True)

	namedVector = []
	for val in indexedVector:
		protocolName = getProtocolName(val[0])
		namedVector.append((protocolName, val[1]))

	return namedVector
