from util.clip_subtitle import ClipSubtitle
from util.clip_video import ClipVideo
import glob
import os


class ClipSolver:
    def __init__(self, is_serials=True, save_subtitle_path=None):
        self.sub_cliper = ClipSubtitle()
        self.vid_cliper = ClipVideo()

    def _prepare(self, data_path, clip_video):
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
            return out_list
        else:
            return sub_path_list

    def clip(self, data_path, clip_video=False, just_show_video=True):
        path_list = self._prepare(data_path, clip_video)
        save_sub_dir = data_path + '/clip_subtitle/'
        save_vid_dir = data_path + '/clip_video/'
        if not os.path.isdir(save_sub_dir):
            os.mkdir(save_sub_dir)
        if not os.path.isdir(save_vid_dir):
            os.mkdir(save_vid_dir)
        for i, raw_path in enumerate(path_list):
            if not clip_video:
                result_subs = self.sub_cliper.clip(raw_path, combine=True, save_path=save_sub_dir)
            else:
                sub_path, vid_path = raw_path.split(';;')
                result_subs = self.sub_cliper.clip(sub_path, combine=True, save_path=save_sub_dir)
                self.vid_cliper.clip_video(vid_path, result_subs, save_dir=save_vid_dir, just_show_video=just_show_video)


if __name__ == '__main__':
    data_path = 'E:/LG/AI EDU/datasets/friends'
    solver = ClipSolver()
    solver.clip(data_path, clip_video=True, just_show_video=False)  # eee
