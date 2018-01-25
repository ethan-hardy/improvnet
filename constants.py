BATCH_SIZE = 36 # to make things clean conceptually, a batch has the data for each note (36 notes)
LSTM_STATE_SIZE = 128 # this is arbitrary atm
INPUT_SIZE = 28
NUM_CLASSES = 2 # one hot encoding on <play this note, don't play this note>
NUM_LAYERS = 3
SEQUENCE_LENGTH = 64 # 4 bars
NUM_EPOCHS = 3
LEARNING_RATE = 0.001
MIN_PROB_THRESHOLD = 0.5 # if all note probs are below this, we predict a rest

QUANTIZATION = 4 # 4 quantization steps per beat
REST = -1