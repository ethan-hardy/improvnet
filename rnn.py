import numpy as np
import tensorflow as tf

BATCH_SIZE = 36 # to make things clean conceptually, a batch has the data for each note (36 notes)
LSTM_STATE_SIZE = 128 # this is arbitrary atm
INPUT_SIZE = 27
NUM_CLASSES = 2 # one hot encoding on <play this note, don't play this note>
NUM_LAYERS = 3


def _lstm_cell():
  # TODO: dropout
  return tf.contrib.rnn.BasicLSTMCell(LSTM_STATE_SIZE)

class Rnn:
  def __init__(self):
    self._build_graph()

  def _build_graph():
    weights = {
      'out': tf.Variable(tf.random_normal([LSTM_STATE_SIZE, NUM_CLASSES]))
    }
    biases = {
      'out': tf.Variable(tf.random_normal([NUM_CLASSES]))
    }

    input_data = tf.placeholder(tf.int32, shape=[None, BATCH_SIZE, INPUT_SIZE])
    input_labels = tf.placeholder(tf.int32, shape=[None, BATCH_SIZE])
    stacked_lstm = tf.contrib.rnn.MultiRNNCell(
      [ _lstm_cell() for _ in range(NUM_LAYERS) ])
    init_state = stacked_lstm.zero_state(BATCH_SIZE, tf.float32)

    outputs, state = tf.contrib.rnn.static_rnn(
      stacked_lstm,
      input_data,
      initial_state=init_state
    )
    output = tf.reshape(tf.concat(outputs, 1), [-1, LSTM_STATE_SIZE])
    logits = tf.nn.xw_plus_b(output, weights['out'], biases['out'])
    logits = tf.reshape(logits, [BATCH_SIZE, self.num_steps, NUM_CLASSES])

    loss = tf.contrib.seq2seq.sequence_loss(
      logits,
      input_labels,
      tf.ones([BATCH_SIZE, self.num_steps], dtype=tf.float32),
      average_across_timesteps=False,
      average_across_batch=True
    )

    loss_op = tf.reduce_sum(
      loss
    )
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=learning_rate)
    train_op = optimizer.minimize(loss_op)

  def train(input_tensors, input_labels):

