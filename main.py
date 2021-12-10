import os
import mutagen
import miniaudio
import numpy as np
from scipy.io.wavfile import write

music_folder = '/home/olegsea/Music'
# music_folder = input()

# audiofile = mutagen.File('/home/olegsea/Music/Camellia/Force! (Album)/12 かめりあ - ふぉーす！.flac')
audiofile = mutagen.File(f'{music_folder}/audio200.mp3')
print(audiofile)

# stream = miniaudio.stream_file(f'/home/olegsea/music/camellia/force! (album)/12 かめりあ - ふぉーす！.flac')
# stream = miniaudio.stream_file(f'{music_folder}/audio200.mp3')
# with miniaudio.PlaybackDevice() as device:
#   device.start(stream)
#   input()
file = miniaudio.decode_file(f'input.mp3')
# file = miniaudio.decode_file(f'{music_folder}/audio200.mp3')
print(file)

write('test.wav', file.sample_rate, np.vstack((np.array(file.samples[0::2]), np.array(file.samples[1::2]))).transpose())