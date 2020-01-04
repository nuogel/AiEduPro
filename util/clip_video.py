from moviepy.editor import *
from util.clip_subtitle import ClipSubtitle
import cv2


class ClipVideo:
    def __init__(self):
        self.cliper_subtitle = ClipSubtitle()
        self.combine_list = []
        ...

    def clip_video(self, vid_path, clip_subs, save_dir, just_show_video, key_word=None):
        '''

        :param video_path:  the raw video path
        :param clip_subs:  the time  clip path
        :param save_dir:  path to save clipped video.
        :return:
        '''
        video = VideoFileClip(vid_path)

        for sub in clip_subs:
            start_time = sub[1]
            end_time = sub[2]
            if key_word:
                text = self._clip_words_to3list(sub, key_word)
            else:
                text = sub[3] + '\n' + sub[4]
            if text is None: continue
            _clip = video.subclip(start_time, end_time)
            # _clip = _clip.resize((1080, 700))
            _clip = self._clip_raw_words(_clip)
            _clip = self._add_new_words(_clip, text=text)  # ,[]   + '\n'
            self.combine_list.append(_clip)
            if just_show_video:
                _clip.preview()
            else:
                save_path = os.path.join(save_dir, sub[0] + '.mp4')

                if os.path.isfile(save_path):
                    os.remove(save_path)
                _clip.write_videofile(save_path)
            print(sub)
        video.reader.close()
        video.audio.reader.close_proc()

    def _clip_raw_words(self, clip, ratio=0.85):
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
        text_size = (1080, 200)
        fontsize = 20
        if isinstance(text, list):
            l0 = len(text[0])
            l1 = len(text[1])
            l2 = len(text[2])
            l3 = len(text[3])
            fontsize_r = fontsize * 0.75
            x0 = (text_size[0] - (l0 + l1 + l2) * fontsize_r) // 2
            y0 = text_size[1] // 2 - 30
            txt_clips_all = []
            if l0 != 0:
                txtClip0 = TextClip(text[0], color='white', font="FangSong", stroke_width=0.5, stroke_color='white', kerning=5, fontsize=fontsize)
                text_video0 = txtClip0.set_pos((x0, y0)).set_duration(clip.duration).set_start(0)
                txt_clips_all.append(text_video0)
            if l1 != 0:
                txtClip1 = TextClip(text[1], color='red', font="FangSong", stroke_width=0.5, stroke_color='red', kerning=5, fontsize=fontsize)
                text_video1 = txtClip1.set_pos((int(x0 + l0 * fontsize_r), y0)).set_duration(clip.duration).set_start(0)
                txt_clips_all.append(text_video1)

            if l2 != 0:
                txtClip2 = TextClip(text[2], color='white', font="FangSong", stroke_width=0.5, stroke_color='white', kerning=5, fontsize=fontsize)
                text_video2 = txtClip2.set_pos((int(x0 + (l0 + l1) * fontsize_r), y0)).set_duration(clip.duration).set_start(0)
                txt_clips_all.append(text_video2)

            if l3 != 0:
                txtClip3 = TextClip(text[3], color='white', font="FangSong", stroke_width=0.5, stroke_color='white', kerning=5, fontsize=fontsize)
                text_video3 = txtClip3.set_pos(('center', y0 + 30)).set_duration(clip.duration).set_start(0)
                txt_clips_all.append(text_video3)

            video = CompositeVideoClip(txt_clips_all, size=text_size)
        else:
            txtClip = TextClip(text, color='white', font="FangSong", stroke_width=0.5, stroke_color='white', kerning=5, fontsize=fontsize)  #
            text_video = txtClip.set_pos('center').set_duration(clip.duration).set_start(0)
            video = CompositeVideoClip([text_video], size=text_size)

        video = clips_array([[clip], [video]])
        return video

    def _clip_words_to3list(self, sub, key_words):
        if key_words not in sub[3]:
            # print('finding ...', key_words)
            return None
        else:
            print('found ...', key_words)
            w_list = sub[3].split(key_words)
            w_list.insert(1, key_words)
            w_list.append(sub[4])
            return w_list

    def _combine_all_video(self, save_dir):
        save_path = os.path.join(save_dir, 'combine.mp4')
        video_combine = concatenate_videoclips(self.combine_list)
        if os.path.isfile(save_path):
            os.remove(save_path)
        print('combining the videos')
        video_combine.write_videofile(save_path)


if __name__ == '__main__':
    video_path = "../datasets/videos/Zootopia/Zootopia.2016.疯狂动物城.720p.Chi_Eng.ZMZ-BD-MP4.mp4"
    subtitle_path = "../datasets/videos/Zootopia/Zootopia.2016.1080p.BluRay.x264-SPARKS/Zootopia.2016.1080p.BluRay.x264-SPARKS.简体&英文.ass"
    save_dir = 'datasets/videos/Zootopia/Zootopia_clips/'
    video_cliper = ClipVideo()
    video_cliper.clip_video(video_path, subtitle_path, save_dir)
