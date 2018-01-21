_PITCH_MAP = {
  'C': 0,
  'D': 2,
  'E': 4,
  'F': 5,
  'G': 7,
  'A': 9,
  'B': 11
}
_PITCH_COUNT = 12
_CHORD_FORMULAS = {
  'm7': [3, 7, 10],
  '7': [4, 7, 10],
  'dim7': [3, 6, 9],
  'hdim7': [3, 6, 10],
  'maj7': [4, 7, 11],
  '': [4, 7],
  'm': [3, 7]
}

def _get_pitch(root, modifier):
  return (root + modifier) % _PITCH_COUNT

def _make_chord_tones(root, formula):
  offsets = [0] + _CHORD_FORMULAS[formula]
  return [ _get_pitch(root, offset) for offset in offsets ]

class Chord:
  def __init__(self, string):
    letter = string[0].upper()
    if letter not in _PITCH_MAP:
      raise 'Invalid chord letter'

    if string[1] == '#':
      modifier = 1
    elif string[1] == 'b':
      modifier = -1
    else:
      modifier = 0

    formula_start_ind = 1 if modifier == 0 else 2
    formula = string[formula_start_ind:]

    self.root = _get_pitch(_PITCH_MAP[letter], modifier)
    self.chord_tones = _make_chord_tones(self.root, formula)

_DURATIONS = {
  '-': -1, # replaced based on bar length
  '.': 2,
  ',': 1
}

def _parse_chords(chords_str, bar_length):
  chords_str += '|'

  chord_start = 0
  chord_end = None
  chords = []
  duration = None

  for ind, char in enumerate(chords_str):
    if char in _DURATIONS:
      incr = bar_length if _DURATIONS[char] == -1 else _DURATIONS[char]
      duration = incr if duration is None else duration + incr
      chord_end = ind if chord_end is None else chord_end
    elif duration is not None:
      last_chord_str = chords_str[chord_start:chord_end]
      chord = Chord(last_chord_str)
      chords.extend([chord] * duration)
      chord_end = None
      chord_start = ind
      duration = None

  return chords


class Progression:
  def __init__(self, midi_filename, chords_str, bar_length=4):
    self.midi_filename = midi_filename
    self.chords = _parse_chords(chords_str, bar_length)
