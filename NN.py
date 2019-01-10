#!/usr/bin/env python3

import tensorflow as tf
from tensorflow.keras import layers
import numpy as np

class NN():
	def __init__(self, inputVectorSize, outputVectorSize):
		self.model = tf.keras.Sequential([
			layers.Dense(inputVectorSize, activation='linear'),
			layers.Dense(64, activation='relu'),
			layers.Dense(64, activation='relu'),
			layers.Dense(64, activation='relu'),
			layers.Dense(outputVectorSize, activation='softmax')
		])

		self.model.compile(
			optimizer = tf.train.AdamOptimizer(),
			loss = 'categorical_crossentropy',
			metrics = ['accuracy']
		)

	def load(self, path):
		self.model.load_weights(path)

	
	def save(self, path):
		self.model.save_weights(path)

	
	def train(self, inputVector, outputVector):
		self.model.fit(
			np.array(inputVector),
			np.array(outputVector),
			epochs = 1000,
			verbose = 2
		)
	
	
	def predict(self, inputVector):
		return self.model.predict(
			np.array([inputVector])
		)

	

