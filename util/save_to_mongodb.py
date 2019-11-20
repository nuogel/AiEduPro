# coding=utf-8
from pymongo import MongoClient
from gridfs import GridFS
import os


def connect_database(db_name, tabel_name=None):
    client = MongoClient('localhost', 27017)
    mydb = client[db_name]
    if tabel_name is not None:
        mytable = mydb[tabel_name]
    else:
        mytable = None
    return mydb, mytable


def main_movies(db, clip_f, folder_path):
    grid_db = GridFS(db)
    clip_info = [line.split(";") for line in open(clip_f, encoding='utf-8').readlines()]

    for i, clip in enumerate(clip_info):
        fileid = clip[0]
        file_path = folder_path + fileid + '.mp4'
        if not os.path.isfile(file_path):
            print('no such a file:', file_path)

        movie_f = open(file_path, 'rb')
        grid_db.put(data=movie_f.read(),
                    filenameID=fileid,
                    start_time=clip[1],
                    end_time=clip[2],
                    english_subtitle=clip[3],
                    chinese_subtitle=clip[4])
        print('saved :', file_path)
        movie_f.close()


def download_to_local(db):
    fs = GridFS(db)
    cursor = fs.find()

    # with open(file.filename, 'wb') as f:
    #         while True:
    #             data = file.read()
    #             if not data:
    #                 break
    #             f.write(data)
    for file in cursor:
        if file.filename == "Zootopia_0.mp4":
            with open(file.filename, 'wb') as f:
                while True:
                    data = file.read()
                    if not data:
                        break
                    f.write(data)


if __name__ == '__main__':
    movie_folder_path = '../datasets/videos/Zootopia/Zootopia_clips/'
    clip_file = '../datasets/videos/Zootopia/Zootopia.txt'

    db, tabel = connect_database(db_name='moviedb')
    # download_to_local(db)
    # main_movies(db, clip_file, movie_folder_path)
