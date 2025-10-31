import os
from moviepy import *
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from PIL import Image

datadir = 'C:\\Users\\klill\\Music\\Tatsuro Yamashita\\[1984.xx.xx] Come Along II (VBR)'
song_path = os.path.join(datadir, '5. Yoru no tsubasa (Nightwing).mp3')
cover_path = os.path.join(datadir, 'cover.jpg')  # 500 x 440, 25:22
backcover_path = os.path.join(datadir, 'backcover.jpg') # 539 x 452, 539:452

def get_audio_duration(song_file_path):
    try:
        if song_file_path.lower().endswith(".mp3"):
            audio = MP3(song_file_path)
        elif song_file_path.lower().endswith(".ogg"):
            audio = OggVorbis(song_file_path)
        elif song_file_path.lower().endswith(".flac"):
            audio = FLAC(song_file_path)
        else:
            print("Unsupported file format for mutagen.")
            return None
        return audio.info.length
    except Exception as e:
        print(f"Error getting duration with mutagen: {e}")
        return None
    
def make_adjusted_images(cover_path, backcover_path):
    cover_adjusted_path = os.path.join(datadir, 'cover_temp.jpg')
    backcover_adjusted_path = os.path.join(datadir, 'backcover_temp.jpg')
    c_im = Image.open(cover_path)
    bc_im = Image.open(backcover_path)

    new_img_size = find_optimal_img_size(c_im.size[0], c_im.size[1], bc_im.size[0], bc_im.size[1])
    c_im_resized = c_im.resize(new_img_size)
    bc_im_resized = bc_im.resize(new_img_size)
    c_im_resized.save(cover_adjusted_path)
    bc_im_resized.save(backcover_adjusted_path)

    c_im.close()
    c_im_resized.close()
    bc_im.close()
    bc_im_resized.close()
    return (cover_adjusted_path, backcover_adjusted_path)

def find_optimal_img_size(c_im_w, c_im_h, bc_im_w, bc_im_h):
    # Find "optimal" image size
    r_ = ( (c_im_w / c_im_h) + (bc_im_w / bc_im_h) ) / 2    # Average image aspect ratio
    s = max( (c_im_w+c_im_h)/2, (bc_im_w+bc_im_h)/2 )   # Largest average side length
    a = (2*r_) / (1+r_) # upscale factor
    b = 2 / (1+r_)      # downscale factor
    return ( round(s*a), round(s*b) )   # new image size

def remove_temp_images(cover_adjusted_path, backcover_adjusted_path):
    os.remove(cover_adjusted_path)
    os.remove(backcover_adjusted_path)
    
def make_video_two_clips(cover, backcover, song):
    song_duration = get_audio_duration(song)
    cap, bap = make_adjusted_images(cover, backcover)
    cover_clip = ImageClip(cap, duration=song_duration/2)
    backcover_clip = ImageClip(bap, duration=song_duration)
    full_clip = CompositeVideoClip(clips=[backcover_clip, cover_clip])
    full_clip.write_videofile('two clips.mp4', fps=1, audio=song)
    cover_clip.close()
    backcover_clip.close()
    full_clip.close()
    remove_temp_images(cap, bap)

def make_video_adjacent_imgs(cover, backcover, song):
    song_duration = get_audio_duration(song)


# error in CompositeVideoClip with argument clips=[backcover_clip, cover_clip] instead of clips=[cover_clip, backcover_clip]
# backcover.jpg has larger dimensions; something to do with layers?
# test with PILLOW: set sizes
# solution with PILLOW: readjust sizes of images to all be the same


make_video_two_clips(cover_path, backcover_path, song_path)


