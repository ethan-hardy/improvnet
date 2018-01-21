from mido import Midi_file

QUANTIZATION = 4 # 4 quantization steps per beat
REST = -1

def _get_note_group(pitch, duration):
  return [ { 'pitch': pitch, 'is_note_beginning': ind == 0 } for ind in range(0, duration)]

def _create_quantized_list(track, ticks_per_beat):
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
      rest_duration = round(msg.time / ticks_per_beat * QUANTIZATION)
      if rest_duration > 0:
        notes.extend(get_note_group(REST, rest_duration))
    elif msg.type == 'note_off':
      note_duration = round(msg.time / ticks_per_beat * QUANTIZATION)
      notes.extend(get_note_group(msg.note, note_duration))

  return notes

  # notes are in the form of
  # { pitch: <int>, is_note_beginning: <bool> }
  # -1 pitch is for a rest


def read_file(filename):
  file = Midi_file(filename)

  return _create_quantized_list(file.tracks[0], file.ticks_per_beat), file.ticks_per_beat
