# Input album folder containing mp3-files and a cover image.
# Filename formats for the songs will be "n.s", with n a number and s the name of the song.
# Filename for the image will be "cover."
# Makes a video with the cover image and the songs

from moviepy import *
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from PIL import Image
from pydub import AudioSegment
import os
import re

def get_content_in_path(path):
    songs, imgs, others = [], {}, []

    for file in os.listdir(path=path):
        if file.lower() == 'cover.jpg':
            imgs['cover'] = file
            continue
        elif file.lower() == 'backcover.jpg':
            imgs['backcover'] = file
            continue
        splitted_file_name = file.split('.')
        try:
            int(splitted_file_name[0])
            songs.append(file)
        except:
            others.append(file)
            
    if (len(imgs) == 0):
        raise Exception("No cover images found.")
    if (len(songs) == 0):
        raise Exception("No songs found.")
    
    # sort songs
    def sorting_method(filename):
        match = re.match(r'^([\d\.]+)', filename)
        numeric_parts = tuple(int(s) for s in match.group(1).split('.') if s.isdigit())
        return numeric_parts
    songs = sorted(songs, key=sorting_method)

    return (songs, imgs, others)

def print_msg_and_list(msg, list):
    print(msg)
    for l in list:
        print(l)

def merge_images(frontcover_path, backcover_path, output_path):
    fc = Image.open(frontcover_path)
    bc = Image.open(backcover_path)

    new_img_size = find_optimal_img_size(fc.size[0], fc.size[1], bc.size[0], bc.size[1])
    fc_resized = fc.resize(new_img_size)
    bc_resized = bc.resize(new_img_size)

    merged_img = Image.new("RGB", (new_img_size[0]*2, new_img_size[1]))
    merged_img.paste(fc_resized)
    merged_img.paste(bc_resized, (new_img_size[0], 0))

    merged_img.save(output_path)

def adjust_to_even(width, height):
    # Micro adjusting resolution in case of odd numbers and in a optimal way
    if width % 2 == 1:
        if width < height:
            width += 1
        else:
            width -= 1

    if height % 2 == 1:
        if width < height:
            height -= 1
        else:
            height += 1
    return (width, height)

def find_optimal_img_size(c_im_w, c_im_h, bc_im_w, bc_im_h):
    # Find "optimal" image size
    r_ = ( (c_im_w / c_im_h) + (bc_im_w / bc_im_h) ) / 2    # Average image aspect ratio
    s = max( (c_im_w+c_im_h)/2, (bc_im_w+bc_im_h)/2 )   # Largest average side length
    a = (2*r_) / (1+r_) # upscale factor
    b = 2 / (1+r_)      # downscale factor

    w = round(s*a)  # width
    h = round(s*b)  # height
    w, h = adjust_to_even(w, h)

    return (w, h)   # new image size

def write_video(img_path, complete_output_path, complete_audio_path):
    video = ImageClip(img_path, duration=1)
    video.write_videofile(complete_output_path,
                          fps=1,
                          audio=complete_audio_path)
    video.close()

def print_song_timestamps(song_names, song_lengths):
    # Format:
    # Timestamp | Song name
    # 0:00:00   | 01. The Theme from Big Wave
    # 0:32:14   | 02. Jody
    # 1:05:32   | 03. Only with You
    # 2:31:19   | 04. Magic Ways

    # Timestamp | Song name
    # 00:00     | 01. The Theme from Big Wave
    # 14:14     | 02. Jody
    # 23:32     | 03. Only with You
    # 31:19     | 04. Magic Ways
    
    # Find max name length
    mnl = max([len(song) for song in song_names])    # max name length

    # Find total album length
    # tal = sum(song_durations)   # last time stamp    # NOT NEEDED

    # Check if total album length is greater than one hour
    INCLUDE_HOUR_STAMP = sum(song_durations) >= 3600

    # Print headers
    print(f'\nTimestamp | Song')

    # Print song name and timestamp with correct spacing
    timestamp = 0
    i = 0
    for song in song_names:

        # For calculating hour, minute, seconds, it rounds to the nearest integer.
        # It will never round to times below 0:00:00 because the smallest value passed to
        # the function is 0. But it could round up to a time value which is greater than
        # the video.
        ts = int(timestamp)
        s = ts % 60 
        s = str(s) if s >= 10 else '0' + str(s)
        m = (ts - 3600*(ts//3600)) // 60
        m = str(m) if m >= 10 else '0' + str(m)
        
        if INCLUDE_HOUR_STAMP:
            h = str(ts // 3600)
            print(f'{h+':'+m+':'+s:<{len('Timestamp')}} | {song}')
        else:
            print(f'{m+':'+s:<{len('Timestamp')}} | {song}')

        timestamp += song_lengths[i]
        i += 1


### USER INPUT ###
# Flow:
# 1. Enter album data directory
# 2. Confirm content to be used
# 3. Single video album playlist or multiple individual songs of videos
# 4. Enter output directory
# 5. Proceed confirmation

# Enter album data directory
datadir = input("Album folder directory:\n- ")

# Confirm content to be used
songs, imgs, others = get_content_in_path(datadir)
print_msg_and_list('\nImages to be used:', imgs.values())
print_msg_and_list('\nSongs to be used:', songs)
if (len(others) != 0):
    print_msg_and_list('\nFiles to be ignored:', others)

# Single video album playlist or multiple individual songs of videos
PLAYLIST_FORM_CHOICE = ''
while (not PLAYLIST_FORM_CHOICE in ['1', '2']):
    print('\nChoose an option')
    print('1: Single long video')
    print('2: Multiple videos')
    PLAYLIST_FORM_CHOICE = input('- ')

# Enter output directory
output_path = input('\nVideo playlist output path: (empty is same as input path)\n- ')
if (output_path == ''):
    output_path = datadir

PROCEED_CHOICE = input('\nProceed to processing with an empty input,\nExit with other input:\n- ')
if PROCEED_CHOICE != '':
    exit()



### VIDEO PROCESSING ###

# Prepare image
img_path = os.path.join(datadir, 'cover_img_temp.jpg')
if (len(imgs) == 2):
    #merge
    cover_path = os.path.join(datadir, imgs['cover'])
    backcover_path = os.path.join(datadir, imgs['backcover'])
    merge_images(cover_path, backcover_path, img_path)
elif (len(imgs) == 1):
    #use one image
    for key in imgs.keys():
        img_path = os.path.join(datadir, imgs[key])
        new_img = Image.open(img_path)
        w = new_img.size[0]
        h = new_img.size[1]
        w, h = adjust_to_even(w, h)
        new_img = new_img.resize((w,h))
        new_img.save(img_path)
else:
    raise Exception(f'Found 0 or more than 2 images to be used:\n{imgs}')


# Single or multiple video(s)

# Paths for temporary image and audio files
full_album_video_path = ''
full_album_audio_path = ''

if (PLAYLIST_FORM_CHOICE == '1'):   # Single long video
    # Preparing variables
    album_name = datadir.rsplit('\\', maxsplit=1)[1]
    full_album_video_path = os.path.join(output_path, album_name + '.mp4')
    full_album_audio_path = os.path.join(output_path, album_name + '.flac')
    full_album_audio = AudioSegment.empty()
    song_durations = []
    # FIRST_ITERATION = True

    # Making full album audio file and gathering names of songs without file extension
    print('\nStiching audio files...')
    song_names = []
    for song in songs:
        print(f'+ {song} ...')
        
        segment = AudioSegment.from_file(os.path.join(datadir, song))
        song_durations.append(segment.duration_seconds)
        full_album_audio += segment
        
        song_name, _ = os.path.splitext(song)
        song_names.append(song_name)

    full_album_audio.export(os.path.join(output_path, album_name + '.flac'))
    print('Audio file made.')

    # Making video
    write_video(img_path, 
                os.path.join(output_path, album_name + '.mp4'),
                os.path.join(output_path, album_name + '.flac'))
    
    print_song_timestamps(song_names, song_durations)

if (PLAYLIST_FORM_CHOICE == '2'):   # Multiple videos
    # Making videos
    for song in songs:
        song_name, _ = song.rsplit('.', maxsplit=1)
        write_video(img_path, 
                    os.path.join(output_path, song_name + '.mp4'),
                    os.path.join(datadir, song))

# Deleting temporary files
if (len(imgs) == 2):
    os.remove(img_path)
if (PLAYLIST_FORM_CHOICE == '1'):
    os.remove(full_album_audio_path)