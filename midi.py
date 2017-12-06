from mido import MidiFile

QUANTIZATION = 4 # 4 quantization steps per beat
REST = -1

def _getNoteGroup(pitch, duration):
  return [ { 'pitch': pitch, 'isNoteBeginning': ind == 0 } for ind in range(0, duration)]

def _createQuantizedList(track, ticksPerBeat):
  # midi files put some space between note offs and subsequent
  # note offs. we need to bridge these spaces so note lengths
  # divide evenly and can be quantized for neural net input
  for index, msg in enumerate(track):
    if msg.type == 'note_on':
      first_note_ind = index
      break

  track = track[first_note_ind:-1] # take out end of file message
  notes = []

  for msg in track:
    # TODO: triplets
    if msg.type == 'note_on':
      restDuration = round(msg.time / ticksPerBeat * QUANTIZATION)
      if restDuration > 0:
        notes.extend(getNoteGroup(REST, restDuration))
    elif msg.type == 'note_off':
      noteDuration = round(msg.time / ticksPerBeat * QUANTIZATION)
      notes.extend(getNoteGroup(msg.note, noteDuration))

  return notes

  # notes are in the form of
  # { pitch: <int>, isNoteBeginning: <bool> }
  # -1 pitch is for a rest


def readFile(filename):
  file = MidiFile(filename)

  return createQuantizedList(file.tracks[0], file.ticks_per_beat)
