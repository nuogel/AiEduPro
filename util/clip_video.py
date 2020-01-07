from moviepy.editor import *
from util.clip_subtitle import ClipSubtitle
import cv2


class ClipVideo:
    def __init__(self):
        self.cliper_subtitle = ClipSubtitle()
        self.combine_dict = {}

    def init_clip(self, key_words):
        key_words_out = []
        for key_word in key_words:
            key_words_out.append(key_word.strip())
            self.combine_dict[key_word] = []
        return key_words_out

    def clip_video(self, vid_path, clip_subs, save_dir, just_show_video, key_word=None, combine_videos=True):
        '''

        :param video_path:  the raw video path
        :param clip_subs:  the time  clip path
        :param save_dir:  path to save clipped video.
        :return:
        '''
        video = VideoFileClip(vid_path)

        for sub in clip_subs:
            # len_clips = 1000
            # if len(self.combine_dict) > len_clips:
            #     continue

            start_time = sub[1]
            end_time = sub[2]
            if key_word:
                found_keyword_dict = self._clip_words_tolist(sub, key_word)
            else:
                found_keyword_dict = {'_KeyWord': sub[3] + '\n' + sub[4]}
            if found_keyword_dict['_KeyWord'] is False: continue

            se_clip = video.subclip(start_time, end_time)
            for k, v in found_keyword_dict.items():
                if v == True or v == []: continue
                _clip = self._clip_raw_words(se_clip)
                _clip = self._add_new_words(_clip, text=v)  # ,[]   + '\n'
                self.combine_dict[k].append(_clip)

            if just_show_video and not combine_videos:
                se_clip.preview()
            elif not combine_videos:
                save_path = os.path.join(save_dir, sub[0] + '.mp4')

                if os.path.isfile(save_path):
                    os.remove(save_path)
                se_clip.write_videofile(save_path)
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
        text_size = (1280, 200)
        fontsize = 40
        if isinstance(text, list):
            head_word = text[1]
            l0 = len(text[0])  # before KEYWORD
            l1 = len(text[1])  # KEYWORD
            l2 = len(text[2])  # after KEYWORD
            l3 = len(text[3])  # chiness
            x0 = -1
            while x0 < 0:  # when there is no place for every words,the min the fontsize.
                fontsize_r = fontsize * 0.65
                x0 = (text_size[0] - (l0 + l1 + l2) * fontsize_r) // 2
                fontsize -= 1

            y0 = text_size[1] // 2 - fontsize - 20
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
                text_video3 = txtClip3.set_pos(('center', y0 + fontsize + 10)).set_duration(clip.duration).set_start(0)
                txt_clips_all.append(text_video3)

            txtvideo = CompositeVideoClip(txt_clips_all, size=text_size)
        else:
            txtClip = TextClip(text, color='white', font="FangSong", stroke_width=0.5, stroke_color='white', kerning=5, fontsize=fontsize)  #
            text_video = txtClip.set_pos('center').set_duration(clip.duration).set_start(0)
            txtvideo = CompositeVideoClip([text_video], size=text_size)
            head_word = ''

        headClip = TextClip(head_word, color='red', font="FangSong", stroke_width=0.5, stroke_color='red', kerning=5, fontsize=fontsize)  #
        head_video = headClip.set_pos('center').set_duration(clip.duration).set_start(0)
        head_video = CompositeVideoClip([head_video], size=text_size)

        video = clips_array([[head_video], [clip], [txtvideo]])
        return video

    def _clip_words_tolist(self, sub, key_words):
        found_keyword_dict = {}
        found_keyword_dict['_KeyWord'] = False
        for key_word in key_words:
            if (key_word + ' ' in sub[3]) or (key_word + ',' in sub[3]) or (key_word + '.' in sub[3]) or (key_word + ';' in sub[3]):
                print('found ...', key_word)
                w_list = sub[3].split(key_word)
                w_list.insert(1, key_word)
                w_list.append(sub[4])
                found_keyword_dict[key_word] = w_list
                found_keyword_dict['_KeyWord'] = True
        return found_keyword_dict

    def _combine_all_video(self, save_dir):
        for k, v in self.combine_dict.items():
            print('------->>>>Found :"', k, '": ', len(v))
            if v == []: continue
            save_path = os.path.join(save_dir, k + '.mp4')
            video_combine = concatenate_videoclips(v)
            video_combine.write_videofile(save_path)
