from moviepy.editor import VideoFileClip

av_file_path = 'E:/LG/GitHub/AiEduPro/datasets/friends.mp4'
result_file_path = '../datasets/rotate90.mp4'

video = VideoFileClip(av_file_path)
video = video.rotate(-90)
video.write_videofile(result_file_path)
