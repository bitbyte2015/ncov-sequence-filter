import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import numpy as np

SEQUENCE_LENGTH = 29903

arrayPosition = 0

def countSamples(filename):
  file = open(filename, "r")
  lines = sum(1 for line in file)
  return int(lines/2)

def sequenceToArray(fastaEntry, recombinant):
  inputString = []
  nucleotideValues =    {
  "-": 0.0833333333333,
  "N": 0.25,
  "A": 0.416666666667,
  "T": 0.583333333333,
  "C": 0.75,
  "G": 0.916666666667
  }
  for char in fastaEntry:
    inputString.append(nucleotideValues.get(char, 0.25))
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
      x_data[arrayPosition, 0] = sequenceData[0]
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

input_shape = (1, 1, SEQUENCE_LENGTH)

model = keras.Sequential()
model.add(layers.Dropout(0.0)) #dropout model used to prevent overfitting during training
model.add(layers.Conv1D(256, 1, activation='relu', input_shape=input_shape[1:]))
model.add(layers.MaxPooling1D(1, 1))
model.add(layers.Conv1D(128, 1, activation='relu'))
model.add(layers.MaxPooling1D(1, 1))
model.add(layers.Conv1D(64, 1, activation='relu'))
model.add(layers.MaxPooling1D(1, 1))
model.add(layers.Dense(32, activation='relu'))
model.add(layers.Dense(8, activation='relu'))
model.add(layers.Dense(1, activation='sigmoid'))

model.load_weights('trained_weights/weights')

SEQUENCE_COUNT = countSamples("data/aligned.fasta")
x_data = np.empty([SEQUENCE_COUNT, 1, SEQUENCE_LENGTH], dtype=float) # define our placeholder arrays
y_data = np.empty([SEQUENCE_COUNT, 1], dtype=float)

sequenceNames = parseAlignedFasta("data/aligned.fasta", False, True)

predictions = model.predict(x_data)
normalizedPredictions = []

for item in predictions:
  if(item >= 0.5):
    item = 1
  else:
    item = 0
  normalizedPredictions.append(item)

for i in range(len(normalizedPredictions)):
  if(normalizedPredictions[i]==1):
    print(sequenceNames[i].replace(">", ""), end=', ')
