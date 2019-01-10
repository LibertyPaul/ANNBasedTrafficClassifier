#!/usr/bin/env python3

from payload import Payload
import OutputMapper
import random


class TrainingSample():
	def __init__(self, payload, trafficType):
		assert(isinstance(payload, Payload))
		assert(isinstance(trafficType, str))

		self.__payload = payload
		self.__trafficType = trafficType

		self.toVectors()

	
	def toVectors(self):
		return (self.__payload.toVector(), OutputMapper.toVector(self.__trafficType))


class TrainingSampleBatch():
	def __init__(self):
		self.__samples = []
	

	def add(self, sample):
		assert(isinstance(sample, TrainingSample))
		self.__samples.append(sample)
	

	def clear(self):
		self.__samples = []
	

	def shuffle(self):
		random.shuffle(self.__samples)


	def toVectors(self):
		inputVector  = []
		outputVector = []

		for sample in self.__samples:
			currentVectors = sample.toVectors()
			inputVector.append(currentVectors[0])
			outputVector.append(currentVectors[1])


		return (inputVector, outputVector)
			
