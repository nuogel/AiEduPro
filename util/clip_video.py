from moviepy.editor import *
from util.clip_subtitle import ClipSubtitle
import cv2


class ClipVideo:
    def __init__(self):
        self.cliper_subtitle = ClipSubtitle()
        ...

    def clip_video(self, video_path, clip_subs, save_dir, just_show_video):
        '''

        :param video_path:  the raw video path
        :param clip_subs:  the time  clip path
        :param save_dir:  path to save clipped video.
        :return:
        '''

        video = VideoFileClip(video_path)
        for sub in clip_subs:
            start_time = sub[1]
            end_time = sub[2]
            _clip = video.subclip(start_time, end_time)
            # _clip = video.resize((1080, 700))
            _clip = self._clip_raw_words(_clip)
            key_words = ''  # ''KEY WORD'
            _clip = self._add_new_words(_clip, text=sub[3] + '\n' + key_words + sub[4])
            if just_show_video:
                _clip.preview()
                print(sub[3])
            else:
                save_path = save_dir + sub[0] + '.mp4'

                if os.path.isfile(save_path):
                    os.remove(save_path)
                _clip.write_videofile(save_path)

    def _clip_raw_words(self, clip, height_of_words=100, ratio=0.85):
        def clip_button_words(image):
            shape = image.shape
            height = int(shape[0] * ratio)
            image = image[:height, ...]
            # cv2.imshow('img', image)
            # cv2.waitKey()
            return image

        video = clip.fl_image(clip_button_words)
        return video

    def _add_new_words(self, clip, text):
        # txt_clip = TextClip(text, fontsize=30, color='white')
        # # Say that you want it to appear 10s at the center of the screen
        # txt_clip = txt_clip.set_pos('bottom').set_duration(clip.duration).set_start(0)
        # # Overlay the text clip on the first video clip
        # video = CompositeVideoClip([clip, txt_clip])
        # # video = concatenate_videoclips(video)
        text_size = (1080, 200)
        # txtClip0 = TextClip(text[0], color='white', font="FangSong", kerning=5, fontsize=20)
        # txtClip1 = TextClip(text[1], color='red', font="FangSong", kerning=5, fontsize=20)
        # txtClip2 = TextClip(text[2], color='white', font="FangSong", kerning=5, fontsize=20)
        txtClip = TextClip(text, color='white', font="FangSong", stroke_width=1,stroke_color='white', kerning=5, fontsize=20)
        text_video = txtClip.set_pos('center').set_duration(clip.duration).set_start(0)
        video = CompositeVideoClip([text_video], size=text_size)

        # video = CompositeVideoClip([clip, video], size=video_size)
        video = clips_array([[clip], [video]])
        return video


if __name__ == '__main__':
    video_path = "../datasets/videos/Zootopia/Zootopia.2016.疯狂动物城.720p.Chi_Eng.ZMZ-BD-MP4.mp4"
    subtitle_path = "../datasets/videos/Zootopia/Zootopia.2016.1080p.BluRay.x264-SPARKS/Zootopia.2016.1080p.BluRay.x264-SPARKS.简体&英文.ass"
    save_dir = 'datasets/videos/Zootopia/Zootopia_clips/'
    video_cliper = ClipVideo()
    video_cliper.clip_video(video_path, subtitle_path, save_dir)
