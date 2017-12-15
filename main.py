from midi import readFile
from track_info import TRACKS
from rnn import train
import numpy as np

_LOWEST_NOTE = 58

# 36 semitones possible (bell tone Bb up to altissimo B)
# inp[0:35] - 1 if corresponding note was played last step,
#   0 otherwise (only one note should be 1)
# inp[36] - 1 if note played was begun last step,
#   0 if it was a continuation of a previous note
# inp[37:48] - 1 if corresponding pitch is a chord tone
#   for this step, 0 otherwise

def _createNoteTensor(note):
  tensor = [0] * 49
  tensor[note['pitch'] - _LOWEST_NOTE] = 1
  tensor[36] = 1 if note['isNoteBeginning'] else 0
  for tone in note['chord'].chordTones:
    tensor[37 + tone] = 1

  return tensor

def _createInputTensor(notes, chords, ticksPerBeat):
  for ind, note in enumerate(notes):
    chordIndex = int(ind / ticksPerBeat) % len(chords)
    note['chord'] = chords[chordIndex]

  return notes

for progression in TRACKS:
  notes, ticksPerBeat = readFile(progression.midiFilename)
  inputTensor = _createInputTensor(notes, chords, ticksPerBeat)
  train(inputTensor)

# TODO: automate fetching of sheet music pdfs and conversion to midi?
