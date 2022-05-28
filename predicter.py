import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np
import sys

SEQUENCE_LENGTH = 29903

arrayPosition = 0

def countSamples(filename):
  file = open(filename, "r")
  lines = sum(1 for line in file)
  return int(lines/2)

def sequenceToArray(fastaEntry, recombinant):
  inputString = []
  nucleotideValues = {
      "-": [0.0, 0.0, 0.0, 0.0],
      "N": [0.0, 0.0, 0.0, 0.0],
      "A": [1.0, -1.0, -1.0, -1.0],
      "T": [-1.0, 1.0, -1.0, -1.0],
      "C": [-1.0, -1.0, 1.0, -1.0],
      "G": [-1.0, -1.0, -1.0, 1.0]
  }
  for char in fastaEntry:
    inputString.append(nucleotideValues.get(char, [0.0, 0.0, 0.0, 0.0]))
  if(recombinant):
    onesPlaceholder = np.ones((1, 1))
  else:
    onesPlaceholder = np.zeros((1, 1))
  return (np.array([inputString]),np.array(onesPlaceholder))

def parseAlignedFasta(filename, recombinant, returnNamedList):
  global x_data, y_data, arrayPosition
  sequenceNames = []
  evenLine = False
  file = open(filename, "r")
  for line in file:
    if(evenLine):
      line = line.rstrip('\n')
      sequenceData = sequenceToArray(line, recombinant)
      x_data[arrayPosition] = sequenceData[0]
      y_data[arrayPosition, 0] = sequenceData[1]
      evenLine = False
      arrayPosition+=1
    else:
      evenLine = True
      if(returnNamedList):
        line = line.rstrip('\n')
        sequenceNames.append(line)
  file.close()
  return sequenceNames

model = keras.Sequential()
model.add(layers.Input(shape=(SEQUENCE_LENGTH, 4)))
model.add(layers.Dropout(0.0))
model.add(layers.Flatten())
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dropout(0.05))
model.add(layers.Dense(64, activation='relu'))
model.add(layers.Dropout(0.05))
model.add(layers.Dense(256, activation='relu'))
model.add(layers.Dense(119612))
model.add(layers.Reshape((29903, 4)))

model.load_weights('trained_weights/weights')

SEQUENCE_COUNT = countSamples("data/aligned.fasta")
x_data = np.empty([SEQUENCE_COUNT, SEQUENCE_LENGTH, 4], dtype=float)
y_data = np.empty([SEQUENCE_COUNT, 1], dtype=float)

arrayPosition = 0

sequenceNames = parseAlignedFasta("data/aligned.fasta", False, True)

predictions = model.predict(x_data)
normalizedPredictions = []

for item in zip(x_data,predictions):
  y_true = tf.cast(item[0], tf.float32)
  y_pred = tf.cast(item[1], tf.float32)
  elements_equal_to_value = tf.equal(y_true, 0.0)
  inverted = tf.equal(elements_equal_to_value, False)
  as_ints = tf.cast(inverted, tf.int32)
  as_float = tf.cast(inverted, tf.float32)
  NTcount = tf.reduce_sum(as_ints)
  y_true = tf.math.multiply(y_true, as_float)
  y_pred = tf.math.multiply(y_pred, as_float)
  MSE = y_true-y_pred
  MSE = MSE*MSE
  MSE = tf.reduce_sum(MSE)/tf.cast(NTcount, tf.float32)
  if(MSE >= float(sys.argv[1])):
    MSE = 1
  else:
    MSE = 0
  normalizedPredictions.append(MSE)

for i in range(len(normalizedPredictions)):
  if(normalizedPredictions[i]==1):
    print(sequenceNames[i].replace(">", ""), end=',')
