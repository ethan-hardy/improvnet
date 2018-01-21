from midi import read_file
from track_info import TRACKS
from rnn import Rnn
import numpy as np
from constants import SEQUENCE_LENGTH

_LOWEST_NOTE = 58

# 36 semitones possible (bell tone Bb up to altissimo B)
# we have an rnn for each note, which outputs the
# probability that note should play next
# inp[0:14] - 1 if corresponding note was played last step,
#   0 otherwise (only one note should be 1)
# these 15 notes correspond to a range of notes from a
# perfect fifth below the rnn's note to a perfect fifth above
# eg, inp[7] is the note itself
# inp[15] - 1 if note played was begun last step,
#   0 if it was a continuation of a previous note
# inp[16:27] - 1 if corresponding pitch is a chord tone
#   for this step, 0 otherwise

def _create_note_tensor(reference_note, note):
  tensor = [0] * 27
  distance = note - reference_note
  if distance >= -7 && distance <= 7:
    # note is within the range we care about
    tensor[distance + 7] = 1

  tensor[15] = 1 if note['is_note_beginning'] else 0
  for tone in note['chord'].chord_tones:
    tensor[16 + tone] = 1

  return tensor

def _create_note_tensors(note):
  return [ _create_note_tensor(ref, note) for ref in range(36) ]

def _create_input_tensor(notes, chords, ticks_per_beat):
  for ind, note in enumerate(notes):
    chord_index = int(ind / ticks_per_beat) % len(chords)
    note['chord'] = chords[chord_index]
    # convert from midi pitch to our 36 semitone system
    note['pitch'] = note['pitch'] - _LOWEST_NOTE

  return [ _create_note_tensors(note) for note in notes ]

def _encode(bit):
  # return [
  #   bit,
  #   0 if bit is 1 else 1
  # ]
  return bit

def _split(arr, chunk_size):
  # discards the last chunk if it doesn't fit perfectly
  ind = 0
  result = []
  while ind + chunk_size <= len(arr):
    result.append(arr[ind:ind+chunk_size])

  return result

rnn = Rnn()
for progression in TRACKS:
  notes, ticks_per_beat = read_file(progression.midi_filename)
  input_data = _create_input_tensor(notes, chords, ticks_per_beat)
  input_labels = [
    [ _encode(nt[7]) for nt in note_tensors ] for note_tensors in input_data
  ]
  del input_data[-1]
  del input_labels[0]

  rnn.train(
    _split(input_data, SEQUENCE_LENGTH),
    _split(input_labels, SEQUENCE_LENGTH)
  )


# TODO: automate fetching of sheet music pdfs and conversion to midi?
