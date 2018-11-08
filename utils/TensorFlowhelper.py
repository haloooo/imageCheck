# coding: GB2312
import os, re
# execute command, and return the output
def execCmd():
    # r = os.popen(cmd)
    # text = r.read()
    # r.close()
    py_path = os.path.join(os.getcwd(),'utils','classify_image.py')
    pic_path = os.path.join(os.getcwd(),'static','images','upload.jpg')
    cmd = 'python3 ' + py_path + ' --image_file ' + pic_path
    text = os.popen(cmd).readlines()[0]
    print(cmd)
    return text
