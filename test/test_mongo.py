# coding=utf-8
from pymongo import MongoClient
from gridfs import GridFS
import os


def connect_database(db_name, tabel_name=None):
    client = MongoClient('localhost', 27017)

    mydb = client[db_name]

    # dblist = client.list_database_names()
    # if "lgdb" in dblist:
    #     print("数据库已存在！")

    if tabel_name is not None:
        mytable = mydb[tabel_name]

        # collist = mydb.list_collection_names()
        # if "sites" in collist:  # 判断 sites 集合是否存在
        #     print("集合已存在！")
    else:
        mytable = None

    return mydb, mytable


def insert_item(tabel):
    mydict = {"name": "RUNOOB", "alexa": "10000", "url": "https://www.runoob.com"}
    x = tabel.insert_one(mydict)
    print(x)
    print(x.inserted_id)

    mylist = [
        {"name": "Taobao", "alexa": "100", "url": "https://www.taobao.com"},
        {"name": "QQ", "alexa": "101", "url": "https://www.qq.com"},
        {"name": "Facebook", "alexa": "10", "url": "https://www.facebook.com"},
        {"name": "知乎", "alexa": "103", "url": "https://www.zhihu.com"},
        {"name": "Github", "alexa": "109", "url": "https://www.github.com"},
        {"names": "Github", "alexas": "109", "urls": "https://www.github.com"},
    ]

    tabel.insert_many(mylist)


# def delet_db():
#
def find_item(tabel):
    for x in tabel.find():
        print(x)
    print('---------------------')
    myquery = {"name": "RUNOOB"}
    mydoc = tabel.find(myquery)  # .limit(3)
    for x in mydoc:
        print(x)


def update_item(tabel):
    print('---------------------')
    myquery = {"alexa": "10000"}
    newvalues = {"$set": {"alexa": "12345"}}

    # mycol.update_one(myquery, newvalues) # 只匹配查找到的第一条；
    tabel.update_many(myquery, newvalues)  # 匹配查找到的所有；
    for x in tabel.find():
        print(x)


def delete_item(tabel):
    print('---------------------')
    myquery = {"name": "RUNOOB"}
    # mycol.delete_one(myquery) #只匹配查找到的第一条；
    tabel.delete_many(myquery)  # 匹配查找到的所有；
    for x in tabel.find():
        print(x)


def delete_all_ietm(tabel):
    print('---------------------')
    x = tabel.delete_many({})
    print(x.deleted_count, "个文档已删除")
    for x in tabel.find():
        print(x)


def delete_dict(tabel):
    print('---------------------')
    tabel.drop()


######GridFS大文件操作############
def insertFile(db, filePath, fileName):
    fs = GridFS(db, 'fileDepot')
    with open(filePath, 'rb') as fileObj:
        data = fileObj.read()
        id = fs.put(data, filename=fileName)
        print(id)
        fileObj.close()


def main_movies(db):
    folder_path = 'datasets/videos/Zootopia/Zootopia_clips/'
    grid_db = GridFS(db)
    for i, file in enumerate(os.listdir(folder_path)):
        file_path = folder_path + file
        movie_f = open(file_path, 'rb')
        # data = {'movie_data': movie_data, 'movie_name': file}
        grid_db.put(filename=file, data=movie_f.read(), filetype=file.split('.')[1])
        movie_f.close()
        if i > 10:
            exit()


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
        if file.filename =="Zootopia_0.mp4":
            with open(file.filename, 'wb') as f:
                while True:
                    data = file.read()
                    if not data:
                        break
                    f.write(data)


db, tabel = connect_database(db_name='moviedb')
download_to_local(db)
# main_movies(db)
