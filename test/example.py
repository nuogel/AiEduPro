from moviepy.editor import *
import numpy as np
import shutil
from moviepy.video.tools.segmenting import findObjects

clip = VideoFileClip("datasets/friends_10_04.mp4", audio=True). \
    subclip(292.5, 299)  # .crop(486, 180, 1196, 570)

# clip.preview()

w, h = clip.size

# A CLIP WITH A TEXT AND A BLACK SEMI-OPAQUE BACKGROUND
#
txt = TextClip("开春， so hard...", font='FangSong',
               color='red', fontsize=24)

rotMatrix = lambda a: np.array([[np.cos(a), np.sin(a)],
                                [-np.sin(a), np.cos(a)]])


def vortexout():
    xx = lambda x: x * 20 + 100
    yy = lambda y: 10 if (int(y) % 1 == 1) else 20
    return lambda t: (xx(t), yy(t))


txt_mov = txt.set_pos(vortexout())

# FINAL ASSEMBLY
final = CompositeVideoClip([clip, txt_mov])
# final.subclip(0, 5).preview()
out = final.subclip(0, 6).resize(0.5)
# out.preview()
w_path = "datasets/friends.mp4"
if os.path.isfile(w_path):
    os.remove(w_path)
out.write_videofile(w_path, fps=24)
