from aip import AipFace

""" 你的 APPID AK SK """
APP_ID = '10450796'
API_KEY = 'CYhzMn3DpZ7k8alFGmGSYWjG'
SECRET_KEY = 'GVczCug7RaOZArn4Gdz8SeMtD9FYaB1o'

aipFace = AipFace(APP_ID, API_KEY, SECRET_KEY)

# 读取图片
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# # 定义参数变量
# options = {
#     'max_face_num': 1,
#     'face_fields': "age,beauty,expression,faceshape",
# }
#
# # 调用人脸属性检测接口
# result = aipFace.detect(get_file_content('img\\jkr.jpg'), options=options)

# aipFace.addUser(
#                 '中文',
#                 '中文',
#                 'group1',
#                 get_file_content('img\\jkr.jpg')
#                 )
#
# result = aipFace.getGroupUsers('group1')

# options = {
#       'user_top_num': 2,
#         'face_top_num': 2,
#     }
#
# result= aipFace.identifyUser(
#                   'group1',
#                   get_file_content('img\\jkr.jpg'),
#                   options
#                 )
#
# print(result)