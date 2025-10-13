
# Input album folder containing mp3-files and a cover image.
# Filename formats for the songs will be "n.s", with n a number and s the name of the song.
# Filename for the image will be "cover."
# Makes a video with the cover image and the songs

from moviepy import *
import numpy as np
import os

datadir = input("Album folder directory:\n")
# datadir = "C:\\Users\\klill\\Downloads\\Tatsuro Yamashita (For Kjetils eyes only)\\Tatsuro Yamashita (For Kjetils eyes only)\\Tatsuro Yamashita - Rarities (2002) (FLAC)"



cover_img = os.path.join(datadir, "Coverr.jpg")
song_name = "01. Sparkle.mp3"
# song = os.path.join(datadir, song_name + ".mp3")



video = ImageClip(cover_img, duration=1)
video.write_videofile("Rarities cover and Sparkle song.mp4", 
                      fps=1,
                      audio=song_name)
video.close()
