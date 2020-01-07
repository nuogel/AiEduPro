import os


class ClipSubtitle:
    def __init__(self):
        ...

    def _is_chinese(self, uchar):
        """判断一个unicode是否是汉字"""
        if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
            return True
        else:
            return False

    def _is_alphabet(self, uchar):
        """判断一个unicode是否是英文字母"""
        if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
            return True
        else:
            return False

    def _read_subtitles(self, path):
        basename = os.path.basename(path).split('.')[-1]
        subtitles_clip = []
        if basename == 'ass':
            f = open(path, 'r', encoding='utf-16')  # utf-16 utf-8
            try:
                a = f.readlines()
            except:
                return None
            else:
                lines = a
            i = 0
            for line in lines:
                if ("Dialogue" in line):
                    tmp = line.split(',')
                    # print(tmp)
                    # print(line)
                    clip_start_time, clip_end_time = tmp[1], tmp[2]

                    english_subtitle = line.split("}")[-1].strip()
                    '''判断是否不为空，并是全英文'''
                    if len(english_subtitle) == 0:
                        continue
                    elif not self._is_alphabet(english_subtitle[0].strip()):
                        continue

                    '''判断中文是否不为空'''
                    try:
                        chinese_subtitle = line.split(',,')[1].split('{')[0][:-2]
                    except:
                        chinese_subtitle = []
                        print('sorry')
                    if len(chinese_subtitle) == 0:
                        continue
                    if not self._is_chinese(chinese_subtitle):
                        continue

                    '''判断是否为大写开头'''
                    firstW = english_subtitle[0]
                    if firstW.islower():
                        linestyle = 'Continue'
                    else:
                        linestyle = 'Start'
                    subtitle_clip = [clip_start_time, clip_end_time, english_subtitle, chinese_subtitle, linestyle]
                    i += 1
                    subtitles_clip.append(subtitle_clip)

        elif basename == 'art':
            print('art')

        return subtitles_clip

    def combine_subtitle(self, subtitles_clip):
        subtitles_clip_list = []
        i = 0
        while i < len(subtitles_clip):
            start_time = subtitles_clip[i][0]
            end_time = subtitles_clip[i][1]
            english_subtitle = subtitles_clip[i][2]
            chinese_subtitle = subtitles_clip[i][3]
            i += 1
            # if i == 344:
            #     a=0
            if i < len(subtitles_clip):
                # print(i, len(subtitles_clip))
                while subtitles_clip[i][4] == 'Continue':
                    english_subtitle += ('\n' + subtitles_clip[i][2])
                    chinese_subtitle += ('\n' + subtitles_clip[i][3])
                    end_time = subtitles_clip[i][1]
                    if i + 1 < len(subtitles_clip):
                        i += 1
                    else:
                        break

            # print(i, start_time, end_time, english_subtitle, chinese_subtitle)
            subtitles_clip_list.append([start_time, end_time, english_subtitle, chinese_subtitle])
        return subtitles_clip_list

    def _save_txt(self, subtitles_clip, save_path):
        f = open(save_path, 'w', encoding='utf-8')
        for i, sub in enumerate(subtitles_clip):
            txt = '{};{};{};{};{}\n'.format(sub[0], sub[1], sub[2], sub[3], sub[4])
            f.write(txt)
        f.close()

    def clip(self, title_path, combine=True, save_path=None):
        result_subs = self._read_subtitles(title_path)
        if result_subs is None:return None
        if combine:
            result_subs = self.combine_subtitle(result_subs)
        basename = os.path.basename(title_path)
        tmp = basename.split('.')
        basename = tmp[0] + '_' + tmp[1]  # + '_' + tmp[2]  # 依文件名字的情况修改。
        basename = basename.lower()

        for i, r_sub in enumerate(result_subs):
            id = basename + '_' + str(i)
            r_sub.insert(0, id)
            print(i, ': ', result_subs[i])
        if save_path:
            save_sub_path = os.path.join(save_path, basename + '.txt')
            self._save_txt(result_subs, save_sub_path)
        return result_subs

