# import re

# l = ['1. Funky Flushin_.mp3', 
#      '10. Itsuka.mp3', 
#      '2. Silent Screamer.mp3', 
#      '7. Sparkle.mp3',
#      '3. Eien no Full Moon.mp3', 
#      '5. Yoru no tsubasa (Nightwing).mp3', 
#      '4. Love Talkin_ (Honey It_s You).mp3', 
#      '6. Amaku kiken na kaori.mp3', 
#      '8. Loveland, Island.mp3', 
#      '11. Your Eyes.mp3', 
#      '9. Ride on Time.mp3']

# def sorting_method(filename):
#         match = re.match(r'^([\d\.]+)', filename)
#         numeric_parts = tuple(int(s) for s in match.group(1).split('.') if s.isdigit())
#         return numeric_parts

# l = sorted(l, key=sorting_method)


# for i in l:
#     print(i)

from pydub import AudioSegment
import os

# datadir = 'C:\\Users\\klill\\Music\\Tatsuro Yamashita\\[1984.xx.xx] Come Along II (VBR)'
# datadir = 'C:\\Users\\NintendoDS\\Music\\Tatsuro Yamashita\\Sonorite (2005)'
# song1 = os.path.join(datadir, '01. Midas Touch.flac')
# song2 = os.path.join(datadir, '04. 忘れないで.flac')

datadir = 'C:\\Users\\NintendoDS\\Music\\Tatsuro Yamashita\\Moonglow (1979)'
song1 = os.path.join(datadir, '3. Rainy Walk.mp3')
song2 = os.path.join(datadir, '6. Hot Shot.mp3')

# Create some initial audio segments (e.g., from files or silence)
sound1 = AudioSegment.from_file(song1)
sound2 = AudioSegment.from_file(song2)


# Start with the first sound
combined_sound = sound1

# Use += to append subsequent sounds
combined_sound += sound2

# Export the final combined sound
combined_sound.export("final_combined_sound.flac")
