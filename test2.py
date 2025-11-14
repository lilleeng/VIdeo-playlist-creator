from moviepy import *
import os
from PIL import Image

def find_optimal_img_size(c_im_w, c_im_h, bc_im_w, bc_im_h):
    # Find "optimal" image size
    r_ = ( (c_im_w / c_im_h) + (bc_im_w / bc_im_h) ) / 2    # Average image aspect ratio
    s = max( (c_im_w+c_im_h)/2, (bc_im_w+bc_im_h)/2 )   # Largest average side length
    a = (2*r_) / (1+r_) # upscale factor
    b = 2 / (1+r_)      # downscale factor
    
    w = round(s*a)  # width
    h = round(s*b)  # height

    # Micro adjusting in case of odd numbers and in a optimal way
    if w % 2 == 1:
        if w < h:
            w += 1
        else:
            w -= 1

    if h % 2 == 1:
        if w < h:
            h -= 1
        else:
            h += 1

    return (w, h)   # new image size

datadir = 'C:\\Users\\NintendoDS\\Music\\Tatsuro Yamashita\\Moonglow (1979)'

imgp = os.path.join(datadir, 'Cover.jpg')
imge = Image.open(imgp)
imgp2 = os.path.join(datadir, 'backcover.jpg')
imge2 = Image.open(imgp2)
# s = (500, 500)
s = find_optimal_img_size(imge.size[0], imge.size[1], imge2.size[0], imge2.size[1])
# s = (1204, 1205)    # (1203, 1201)
print(s)
imge = imge.resize(s)
imge2 = imge2.resize(s)

imgn = Image.new('RGB', (s[0]*2, s[1]))
imgn.paste(imge)
imgn.paste(imge2, (s[0], 0))
imgn.save('temp_img.jpg')

# img = os.path.join(datadir, 'cover_img_temp.jpg')
img = 'temp_img.jpg'

video = ImageClip(img, duration=5)
video.write_videofile('temp image test.mp4', fps=1)
                    #   audio='C:\\Users\\NintendoDS\\Videos\\Tatsuro Yamashita\\Moonglow\\Moonglow (1979).flac')


# in main code is makes a new file with format 'RGB' and saves to path ending with '.jpg'
# these are two potential issues
# nope, its because odd numbers are bad for video side lengths