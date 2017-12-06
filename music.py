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

def _getPitch(root, modifier):
  return (root + modifier) % _PITCH_COUNT

def _makeChordTones(root, formula):
  offsets = [0] + _CHORD_FORMULAS[formula]
  return [ _getPitch(root, offset) for offset in offsets ]

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

    formulaStartInd = 1 if modifier == 0 else 2
    formula = string[formulaStartInd:]

    self.root = _getPitch(_PITCH_MAP[letter], modifier)
    self.chordTones = _makeChordTones(self.root, formula)

_DURATIONS = {
  '-': -1, # replaced based on bar length
  '.': 2,
  ',': 1
}

def _parseChords(chordsStr, barLength):
  chordsStr += '|'

  chordStart = 0
  chordEnd = None
  chords = []
  duration = None

  for ind, char in enumerate(chordsStr):
    if char in _DURATIONS:
      incr = barLength if _DURATIONS[char] == -1 else _DURATIONS[char]
      duration = incr if duration is None else duration + incr
      chordEnd = ind if chordEnd is None else chordEnd
    elif duration is not None:
      lastChordStr = chordsStr[chordStart:chordEnd]
      chord = Chord(lastChordStr)
      chords.extend([chord] * duration)
      chordEnd = None
      chordStart = ind
      duration = None

  return chords


class Progression:
  def __init__(self, midiFilename, chordsStr, barLength=4):
    self.midiFilename = midiFilename
    self.chords = _parseChords(chordsStr, barLength)
