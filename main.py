from midi import readFile

readFile('ladybird.mid')


# 36 semitones possible (bell tone Bb up to altissimo B)
# inp[0:35] - 1 if corresponding note was played last step, 0 otherwise (only one note should be 1)
# inp[36] - 1 if note played was begun last step, 0 if it was a continuation of a previous note
# inp[37:48] - 1 if corresponding pitch is a chord tone for this step, 0 otherwise
