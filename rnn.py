import numpy as np
import tensorflow as tf
from constants import *

def _create_input(note_ind, last_note_ind, chord):
  input = []
  for i in range(BATCH_SIZE):
    batch_inp = [0] * INPUT_SIZE
    note_offset = note_ind - input_labels
    if note_offset == REST:
      batch_inp[15] = 1
    elif note_offset <= 14 and note_offset >= 0:
      batch_inp[note_offset] = 1
      if note_ind == last_note_ind:
        batch_inp[16] = 0
    for tone in chord.chord_tones:
      batch_inp[17 + tone] = 1
    input.append(batch_inp)

  return input

def _lstm_cell():
  # TODO: dropout
  return tf.contrib.rnn.BasicLSTMCell(LSTM_STATE_SIZE)

class Rnn:
  def __init__(self):
    self._build_graph()

  def _build_predict_graph():


  def _build_graph():
    weights = {
      'out': tf.Variable(tf.random_normal([LSTM_STATE_SIZE, NUM_CLASSES]))
    }
    biases = {
      'out': tf.Variable(tf.random_normal([NUM_CLASSES]))
    }

    self.input_data = tf.placeholder(tf.int32, shape=[SEQUENCE_LENGTH, BATCH_SIZE, INPUT_SIZE])
    self.input_labels = tf.placeholder(tf.int32, shape=[SEQUENCE_LENGTH, BATCH_SIZE])
    self.stacked_lstm = tf.contrib.rnn.MultiRNNCell(
      [ _lstm_cell() for _ in range(NUM_LAYERS) ])
    init_state = stacked_lstm.zero_state(BATCH_SIZE, tf.float32)

    outputs, state = tf.contrib.rnn.static_rnn(
      self.stacked_lstm,
      self.input_data,
      initial_state=init_state
    )
    output = tf.reshape(tf.concat(outputs, 1), [-1, LSTM_STATE_SIZE])
    logits = tf.nn.xw_plus_b(output, weights['out'], biases['out'])
    logits = tf.reshape(logits, [BATCH_SIZE, SEQUENCE_LENGTH, NUM_CLASSES])

    loss = tf.contrib.seq2seq.sequence_loss(
      logits,
      self.input_labels,
      tf.ones([BATCH_SIZE, SEQUENCE_LENGTH], dtype=tf.float32),
      average_across_timesteps=False,
      average_across_batch=True
    )

    loss_op = tf.reduce_sum(
      loss
    )
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=LEARNING_RATE)
    self.train_op = optimizer.minimize(loss_op)


    # prediction graph section
    self.current_input = tf.placeholder(tf.int32, shape=[BATCH_SIZE, INPUT_SIZE])
    self.last_state = init_state
    prediction_output, self.last_state = self.stacked_lstm(self.current_input, self.last_state)
    prediction_logits = tf.nn.xw_plus_b(prediction_output, weights['out'], biases['out'])
    play_probs = tf.stack(prediction_logits, axis=1)[1]
    self.prediction = tf.top_k(play_probs)
    # TODO: make an op to reset hidden state, which we can run after each epoch

  def generate(chord_progression, first_note_ind):
    with tf.Session() as sess:
      notes = []
      last_note_ind = REST
      next_note_ind = first_note_ind
      for time_step_chord in chord_progression:
        inp = _create_input(next_note_ind, last_note_ind, time_step_chord)
        [pred_prob], [pred_ind] = sess.run(self.prediction, feed_dict={
          self.current_input: inp
        })
        # TODO: make nn predict for inp[16]
        # (for now we can assume two back to back same notes are connected)
        notes.append(next_note_ind)
        last_note_ind = next_note_ind
        next_note_ind = pred_ind if pred_prob > MIN_PROB_THRESHOLD else REST
      return notes

  def train(input_data, input_labels):
    with tf.Session() as sess:
      sess.run(tf.global_variables_initializer())
      for i, datum in enumerate(input_data):
        sess.run(self.train_op, feed_dict={
          self.input_data: datum,
          self.input_labels: input_labels[i]
        })
      # TODO: storing / restoring the model

