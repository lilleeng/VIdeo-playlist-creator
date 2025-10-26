# Input album folder containing mp3-files and a cover image.
# Filename formats for the songs will be "n.s", with n a number and s the name of the song.
# Filename for the image will be "cover."
# Makes a video with the cover image and the songs

from moviepy import *
import numpy as np
import os

# Enter album data directory
datadir = input("Album folder directory:\n")
# datadir = "C:\\Users\\klill\\Music\\Tatsuro Yamashita\\Sync of Summer (2023)"
# datadir = "C:\\Users\\klill\\Music\\Tatsuro Yamashita\\[1984.xx.xx] Come Along II (VBR)"

# Confirm content to be used
songs, imgs, others = [], [], []
for file in os.listdir(path=datadir):
    if file == 'cover.jpg' or file == 'backcover.jpg':
        imgs.append(file)
        continue
    splitted_file_name = file.split('.')
    try:
        int(splitted_file_name[0])
        songs.append(file)
    except:
        others.append(file)
songs.sort()
print('Images to be used:')
for img in imgs:
    print(img)
print('\nSongs to be used:')
for song in songs:
    print(song)
print('\nFiles to be ignored:')
for other in others:
    print(other)
proceed = input('\nProceed with an empty input: ')
if proceed != '':
    exit()

# Enter output directory
output_path = input('Video playlist output path: (empty is same as input path)\n')

# Video processing
cover_img = os.path.join(datadir, "cover.jpg")
# backcover_img = os.path.join(datadir, "backcover.jpg")    # ignore for now
for file in songs:
    song_name, file_ext = file.rsplit('.', maxsplit=1)
    video = ImageClip(cover_img, duration=1)
    video.write_videofile(os.path.join(output_path, song_name + '.mp4'),
                          fps=1,
                          audio=os.path.join(datadir, file))
    video.close()
