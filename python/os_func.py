import os

# 遍历文件夹下所以文件(一级目录)
def get_dir_files(path):
    files = os.listdir(path)
    return files

print(get_dir_files("check_homework/homework"))

# 截去文件扩展名
def get_filename(file_name):
    # 最后一级
    base = os.path.basename(file_name)
    # 不带扩展名的文件名
    name = os.path.splitext(base)[0]
    # 文件扩展名
    # exp_name = os.path.splitext(base)[1]
    return name

print(get_filename(__file__))

# 获取一个文件的绝对路径
def get_abspath(filename):
    return os.path.abspath(filename)

# print(get_abspath('os_func.py'))

# 获取一个文件的所在的目录，这里给的文件如果是相对路径，只会返回相对路径
def get_dir(filename):
    return os.path.dirname(filename)

# print(get_dir(__file__))

# 创建目录
import shutil
def create_dir(path):
    if os.path.isdir(path):
        # os.rmdir(path) 删除空文件夹
        shutil.rmtree(path) # 递归删去目录及下所有文件
    
    os.mkdir(path)

# path = get_dir(__file__)
# create_dir(os.path.join(path, "test_r"))
