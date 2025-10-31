import os
from moviepy import *
from mutagen.mp3 import MP3
from mutagen.oggvorbis import OggVorbis
from mutagen.flac import FLAC
from PIL import Image

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
    
def make_video(cover, backcover, song):
    song_duration = get_audio_duration(song)
    cover_clip = ImageClip(cover, duration=song_duration)
    backcover_clip = ImageClip(backcover, duration=song_duration/2)
    full_clip = CompositeVideoClip(clips=[cover_clip, backcover_clip])
    full_clip.write_videofile('two clips.mp4', fps=1, audio=song)
    full_clip.close()

datadir = 'C:\\Users\\klill\\Music\\Tatsuro Yamashita\\[1984.xx.xx] Come Along II (VBR)'
song_path = os.path.join(datadir, '5. Yoru no tsubasa (Nightwing).mp3')
cover_path = os.path.join(datadir, 'cover.jpg')  # 500 x 440, 25:22
backcover_path = os.path.join(datadir, 'backcover.jpg') # 539 x 452, 539:452



# error in CompositeVideoClip with argument clips=[backcover_clip, cover_clip] instead of clips=[cover_clip, backcover_clip]
# backcover.jpg has larger dimensions; something to do with layers?
# test with PILLOW: set sizes
# solution with PILLOW: readjust sizes of images to all be the same

cover_im = Image.open(cover_path)
backcover_im = Image.open(backcover_path)

print(cover_im.format, cover_im.size, cover_im.mode)
print(backcover_im.format, backcover_im.size, backcover_im.mode)

cover_im = cover_im.resize((500, 500))
backcover_im = backcover_im.resize((500, 500))

print(cover_im.format, cover_im.size, cover_im.mode)
print(backcover_im.format, backcover_im.size, backcover_im.mode)



make_video(cover_im, backcover_im, song_path)
