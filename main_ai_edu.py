from util.clip_subtitle import ClipSubtitle
from util.clip_video import ClipVideo, VideoFileClip
import glob
import os


class ClipSolver:
    def __init__(self):
        self.sub_cliper = ClipSubtitle()
        self.vid_cliper = ClipVideo()

    def _prepare(self, data_path, clip_video, key_word):
        # Prepare Path
        save_sub_dir = data_path + '/clip_subtitle/'

        if key_word:
            save_vid_dir = data_path + '/KeyWords/'
        else:
            save_vid_dir = data_path + '/clip_video/'
        os.makedirs(save_sub_dir, exist_ok=True)
        os.makedirs(save_vid_dir, exist_ok=True)

        # Prepare data
        sub_path_list = glob.glob(data_path + '/raw_subtitle/*.ass')
        # vid_path_list = glob.glob(data_path + '/raw_video/*.mp4')
        vid_path_list = glob.glob('D:/UserData/Downloads/' + '老友记第1季/*.mp4')[:5]
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

    def clip(self, data_path, combine_lines=False, clip_video=False, just_show_video=True, key_words=None, combine_videos=True):
        key_words = self.vid_cliper.init_clip(key_words)

        path_list, save_sub_dir, save_vid_dir = self._prepare(data_path, clip_video, key_words)
        for i, raw_path in enumerate(path_list):
            if not clip_video:
                result_subs = self.sub_cliper.clip(raw_path, combine=combine_lines, save_path=save_sub_dir)
            else:
                sub_path, vid_path = raw_path.split(';;')
                result_subs = self.sub_cliper.clip(sub_path, combine=combine_lines, save_path=save_sub_dir)
                self.vid_cliper.clip_video(vid_path, result_subs, save_dir=save_vid_dir, just_show_video=just_show_video, key_word=key_words, combine_videos=combine_videos)
        self.vid_cliper._combine_all_video(save_vid_dir)


if __name__ == '__main__':
    data_path = 'E:/LG/AI EDU/datasets/friends'
    key_words = ["stupid", "I love you", "How could you", "What's going on", 'awkward', 'horrible']

    solver = ClipSolver()
    combine_videos = True
    solver.clip(data_path, combine_lines=False, clip_video=True, just_show_video=False, key_words=key_words, combine_videos=combine_videos)  # ee
