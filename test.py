import wave
import numpy as np
import openal
# import the time module, for sleeping during playback
import time

samplerate = 44100

# A note on the left channel for 1 second.
t = np.linspace(0, 1, samplerate)
left_channel = 0.5 * np.sin(2 * np.pi * 440.0 * t)

# Put the channels together with shape (2, 44100).
audio = np.array([left_channel]).T

# Convert to (little-endian) 16 bit integers.
audio = (audio * (2 ** 15 - 1)).astype("<h")

# def write_wav():
# 	with wave.open("temp.wav", "w") as f:
# 		# 1 Channel.
# 		f.setnchannels(1)
# 		# 2 bytes per sample.
# 		f.setsampwidth(2)
# 		f.setframerate(samplerate)
# 		f.writeframes(audio.tobytes())

# 	# open our wave file
# write_wav()
# source :openal.Source = openal.oalOpen("temp.wav")
# source = openal.Source(openal.Buffer(audio))
# source.set_position([1.0, 0, 0])

# source.play()

# # check if the file is still playing
# while source.get_state() == openal.AL_PLAYING:
# 	# wait until the file is done playing
# 	time.sleep(1)
	
# release resources (don't forget this)
openal.oalQuit()
file_ = wave.open("temp.wav")
print(file_)