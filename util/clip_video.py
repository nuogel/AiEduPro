from moviepy.editor import *
from util.clip_subtitle import ClipSubtitle


class ClipVideo:
    def __init__(self):
        self.cliper_subtitle = ClipSubtitle()
        ...

    def clip_video(self, video_path, clip_subs, save_dir):

        video = VideoFileClip(video_path)
        for sub in clip_subs:
            start_time = sub[1]
            end_time = sub[2]
            _clip = video.subclip(start_time, end_time)

            if save_dir is None:
                _clip.resize(0.2).preview()
                print(sub[3])
            else:
                save_path = save_dir + sub[0]+'.mp4'

                if os.path.isfile(save_path):
                    os.remove(save_path)
                _clip.write_videofile(save_path, fps=24, codec="mpeg4")


if __name__ == '__main__':
    video_path = "datasets/videos/Zootopia/Zootopia.2016.疯狂动物城.720p.Chi_Eng.ZMZ-BD-MP4.mp4"
    subtitle_path = "datasets/videos/Zootopia/Zootopia.2016.1080p.BluRay.x264-SPARKS/Zootopia.2016.1080p.BluRay.x264-SPARKS.简体&英文.ass"
    save_dir = 'datasets/videos/Zootopia/Zootopia_clips/'
    video_cliper = ClipVideo()
    video_cliper.clip_video(video_path, subtitle_path, save_dir)
