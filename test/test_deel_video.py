from moviepy.editor import *
import math
import matplotlib.pyplot as plt
import numpy as np
from moviepy.video.io.bindings import mplfig_to_npimage

path = 'E://LG\programs//NLP//AiEduPro//datasets//lstm_net.avi'
path = 'E://LG//programs//QT//ENV_SYS//my_video//2.mp4'
clip = VideoFileClip(path).subclip(10, 55)  # (10 second to 20second)
# clip1 = clip.fx(vfx.mirror_x)
# clip2 = clip.fx(vfx.mirror_y)
clip3 = clip.resize((400, 300))
clip3.write_videofile('E://LG//programs//QT//ENV_SYS//my_video//2_2.mp4')

# font = TextClip.list('font') #查看字体
# font = TextClip.list('font') #查看字体

# #将4个按顺序串起来
# mov_new = concatenate([clip, clip1, clip2, clip3])
# mov_new.write_videofile('new_movie.mp4')
#
# #将4个按行列拼起来
# mov_new = clips_array([[clip, clip1], [clip2, clip3]])
# mov_new.write_videofile('new_movie2.mp4')
###############################
# CompositeVideoClips
# video = CompositeVideoClip([clip, clip1, clip2, clip3], size=(720, 460))
# video.write_videofile('new_movie3.mp4')

###########################
# video = CompositeVideoClip([clip1, # starts at t=0
#                             clip2.set_start(5), # start at t=5s
#                             clip3.set_start(9)]) # start at t=9s
# video.write_videofile('new_movie4.mp4')
# ########################
# video = CompositeVideoClip([clip1, # starts at t=0
#                             clip2.set_start(5).crossfadein(1),
#                             clip3.set_start(9).crossfadein(1.5)])
# video.write_videofile('new_movie5.mp4')
##############################
# video = CompositeVideoClip([clip1,
#                            clip2.set_pos((45,150)),
#                            clip3.set_pos((90,100))])
# video.write_videofile('new_movie6.mp4')
###################################
# video = (clip
#         .fx( vfx.resize, width=460) # resize (keep aspect ratio)
#         .fx( vfx.speedx, 1.5) # double the speed
#         .fx( vfx.colorx, 1.2)) # darken the picture
# video.write_videofile('new_movie7.mp4')

###################################
#
# video = clip.fl_time(lambda t: 3*t)
# video.write_videofile('new_movie8.mp4')

######################################
# def invert_green_blue(image):
#     return image[:, :, [0, 2, 1]]
#
#
# video = clip.fl_image(invert_green_blue)
# video.write_videofile('new_movie9.mp4')
# ##########################################

# def scroll(get_frame, t):
#     """
#     This function returns a 'region' of the current frame.
#     The position of this region depends on the time.
#     """
#     frame = get_frame(t)
#     frame_region = frame[int(t):int(t) + 360, :]
#     return frame_region
#
#
# video = clip.fl(scroll)
# video.write_videofile('new_movie10.mp4')
###########################################
# clip.save_frame("frame.png", t=2) # saves the frame a t=2s

############################################
# clip.show() # shows the first frame of the clip
# clip.show(8.5) # shows the frame of the clip at t=8.5s
# clip.show(10.5, interactive = True)

##################################################
# clip.preview() # preview with default fps=15
# clip.preview(fps=25)
# clip.preview(fps=15, audio=False) # don't generate/play the audio.
# clip.preview(fps=22000)
############################################
# ipython_display(clip, width=400) # HTML5 will resize to 400 pixels
#############################################
# x = np.linspace(-2, 2, 200)
# duration = 2
# fig, ax = plt.subplots()
# def make_frame(t):
#     ax.clear()
#     ax.plot(x, np.sinc(x**2) + np.sin(x + 2*np.pi/duration * t), lw=3)
#     ax.set_ylim(-1.5, 2.5)
#     return mplfig_to_npimage(fig)
#
# animation = VideoClip(make_frame, duration=duration)
# animation.write_gif('matplotlib.gif', fps=20)
###############################################


###############Audio############################
# audioclip = AudioFileClip('E://LG\programs//NLP//AiEduPro//lstm_net.avi').subclip(10, 20)
# audioclip.write_audiofile('datasets/audio1.mp3')
#################################################
# audioclip = clip.audio
# audioclip.write_audiofile('datasets/audio2.mp3')
###########################################
# maskclip = VideoClip(makeframe, duration=4, ismask=True)
# maskclip = ImageClip("my_mask.jpeg", ismask=True)
# maskclip = VideoFileClip(path, has_mask=True).subclip(10, 20)
# maskclip.preview()

