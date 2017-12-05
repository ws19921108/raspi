from aip import AipFace, AipSpeech
import threading
import time
""" 你的 APPID AK SK """
APP_ID = '10450796'
API_KEY = 'CYhzMn3DpZ7k8alFGmGSYWjG'
SECRET_KEY = 'GVczCug7RaOZArn4Gdz8SeMtD9FYaB1o'

aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# result = aipSpeech.asr(get_file_content('audio.mp3'), 'pcm', 16000, {
#     'lan': 'zh',
# })
# print(result)
# # 定义参数变量
# options = {
#     'max_face_num': 1,
#     'face_fields': "age,beauty,expression,faceshape",
# }
#
# # 调用人脸属性检测接口
# result = aipFace.detect(get_file_content('img\\jkr.jpg'), options=options)
#
# aipFace.addUser(
#                 '1',
#                 'jkr',
#                 'group1',
#                 get_file_content('img\\jkr.jpg')
#                 )
#
# result = aipFace.getGroupUsers('group1')
#
# options = {
#       'user_top_num': 1,
#         'face_top_num': 1,
#     }
#
# result= aipFace.identifyUser(
#                   'group1',
#                   get_file_content('img\\jkr2.jpg')
#                 )

# result = aipFace.getGroupUsers('group1')
#
# for user in result['result']:
#     aipFace.deleteGroupUser('group1', user['uid'])

# print(result)
