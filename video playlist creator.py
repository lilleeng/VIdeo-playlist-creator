
# Input album folder containing mp3-files and a cover image.
# Filename formats for the songs will be "n.s", with n a number and s the name of the song.
# Filename for the image will be "cover."
# Makes a video with the cover image and the songs

from moviepy import *
import numpy as np
import os

datadir = "C:\\Users\\klill\\Downloads\\Tatsuro Yamashita (For Kjetils eyes only)\\Tatsuro Yamashita (For Kjetils eyes only)\\[1982.01.21] For You (VBR)"
cover_img = os.path.join(datadir, "Cover.jpg")
song_name = "01. Sparkle"
song = os.path.join(datadir, song_name + ".mp3")

audio = AudioFileClip(song)

song_duration = 4*60 + 14   # ideally gotten from audio

video = ImageClip(cover_img, duration=song_duration)


video.with_audio(audio)

video.write_videofile("Sparkle.mp4", 
                      fps=1, 
                      codec='libx264',
                      audio_codec='libmp3lame')
video.close()
print("done.")