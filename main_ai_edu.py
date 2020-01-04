from util.clip_subtitle import ClipSubtitle
from util.clip_video import ClipVideo, VideoFileClip
import glob
import os


class ClipSolver:
    def __init__(self, is_serials=True, save_subtitle_path=None):
        self.sub_cliper = ClipSubtitle()
        self.vid_cliper = ClipVideo()

    def _prepare(self, data_path, clip_video, key_word):
        # Prepare Path
        save_sub_dir = data_path + '/clip_subtitle/'

        if not os.path.isdir(save_sub_dir):
            os.mkdir(save_sub_dir)

        if key_word:
            key_words_dir = data_path + '/KeyWords/'
            save_vid_dir = os.path.join(key_words_dir, key_word)
            if not os.path.isdir(key_words_dir):
                os.mkdir(key_words_dir)
            if not os.path.isdir(save_vid_dir):
                os.mkdir(save_vid_dir)
        else:
            save_vid_dir = data_path + '/clip_video/'
            if not os.path.isdir(save_vid_dir):
                os.mkdir(save_vid_dir)

        # Prepare data
        sub_path_list = glob.glob(data_path + '/raw_subtitle/*.ass')
        vid_path_list = glob.glob(data_path + '/raw_video/*.mp4')
        if clip_video:
            out_list = []
            # TODO:判断名字是否一样。
            for vid_path in vid_path_list:
                vid_basename = os.path.basename(vid_path)
                vid_tmp = vid_basename.split('.')
                vid_name = vid_tmp[1] + '.' + vid_tmp[2]
                for sub_path in sub_path_list:
                    sub_basename = os.path.basename(sub_path)
                    if vid_name.lower() in sub_basename.lower():
                        out_list.append(sub_path + ';;' + vid_path)
                        break
            return out_list, save_sub_dir, save_vid_dir
        else:
            return sub_path_list, save_sub_dir, save_vid_dir

    def clip(self, data_path, combine_lines=False, clip_video=False, just_show_video=True, key_word=None):
        path_list, save_sub_dir, save_vid_dir = self._prepare(data_path, clip_video, key_word)

        for i, raw_path in enumerate(path_list):
            if not clip_video:
                result_subs = self.sub_cliper.clip(raw_path, combine=combine_lines, save_path=save_sub_dir)
            else:
                sub_path, vid_path = raw_path.split(';;')
                result_subs = self.sub_cliper.clip(sub_path, combine=combine_lines, save_path=save_sub_dir)
                self.vid_cliper.clip_video(vid_path, result_subs, save_dir=save_vid_dir, just_show_video=just_show_video, key_word=key_word)
        self.vid_cliper._combine_all_video(save_vid_dir)


if __name__ == '__main__':
    data_path = 'E:/LG/AI EDU/datasets/friends'
    solver = ClipSolver()
    key_word = "What's going on"  # 'awkward'  # None  # 'you'  #
    solver.clip(data_path, combine_lines=False, clip_video=True, just_show_video=False, key_word=key_word)  # eee
