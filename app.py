
from flask import Flask, render_template, request, Response, send_from_directory
import os, json, shutil

from utils import FileHelper
from utils.TensorFlowhelper import execCmd

app = Flask(__name__)

# 生成随机字符串，防止图片名字重复
# ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 16))
ran_str = 'upload'
# 定义一个图片存放的位置
png_location = os.path.join(os.path.dirname(__file__), 'static','images')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/')
def go_index_1():
    # file_location = os.path.join(os.path.dirname(__file__), 'CSV\\uploads')
    # del_file(file_location)
    FileHelper.clearUploadedData(True)
    return render_template('img_index.html')

@app.route('/go_index')
def go_index_2():
    # file_location = os.path.join(os.path.dirname(__file__), 'CSV\\uploads')
    # del_file(file_location)
    FileHelper.clearUploadedData(True)
    return render_template('img_index.html')

@app.route('/go_config')
def go_config():
    spectrum = request.args.get('spectrum')
    file_location = os.path.join(os.path.dirname(__file__), 'CSV\\uploads')
    png_location = os.path.join(os.path.dirname(__file__), 'PNG')
    FileHelper.create_csv_folder(file_location, png_location)
    return render_template('config.html',spectrum=spectrum, file_location=file_location)

@app.route('/get_item_list')
def get_item_list():
    path = os.path.join(os.getcwd(),'testItemList')
    result = getFilesByPath(path)
    jsonstr = json.dumps(result)
    return jsonstr

def getFilesByPath(path):
    result = []
    fs = os.listdir(path)
    for f in fs:
        tmp_path = os.path.join(path, f)
        print(tmp_path)
        result.append(f)
    return result

def getFilesByPath_json(path):
    result = []
    fs = os.listdir(path)
    for f in fs:
        tmp_path = os.path.join(path, f)
        print(tmp_path)
        result.append({'file_name':f, 'file_path':tmp_path, 'config':'', 'overlay':''})
    return result

def Response_headers(content):
    resp = Response(content)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/img_upload',methods=['POST','GET'])
def img_upload():
    try:
        shutil.rmtree(png_location)
        os.mkdir(png_location)
        if request.method == 'POST':
            for item in request.files:
                # 获取图片文件
                img = request.files[item]
                # 图片名称
                imgName = ran_str + '.' + img.filename.split('.')[1]
                # 图片path和名称
                file_path = os.path.join(png_location, imgName)
                # 保存图片
                img.save(file_path)
                # 这个是图片的访问路径，需返回前端（可有可无）
                url = '/static/img/brands/' + imgName
                # 要返回前端的json
                resData = {
                    "uploaded": 1,
                    "fileName": imgName,
                    "url": url
                }
                # 返回json 到前端
                return json.dumps(resData, ensure_ascii=False)
    except BaseException as exp:
        print(exp)
        result = {'state': 'error'}
        jsonstr = json.dumps(result)
        return jsonstr

def return_img_stream(img_local_path):
    """
    工具函数:
    获取本地图片流
    :param img_local_path:文件单张图片的本地绝对路径
    :return: 图片流
    """
    import base64
    img_stream = ''
    with open(img_local_path, 'r') as img_f:
        img_stream = img_f.read()
        img_stream = base64.b64encode(img_stream)
    return img_stream


@app.route('/img_show')
def img_show():
    # for root, dirs, files in os.walk(png_location):
    #     for file in files:
    #         img_path = os.path.join(root, file)
    #         print(img_path)
    out_put = execCmd()
    return render_template('img_show.html', out_put=out_put)

@app.route('/upload_file')
def upload_file():
    file_location = request.args.get('file_location')
    result = getFilesByPath(file_location)
    jsonstr = json.dumps(result)
    return jsonstr

@app.route('/getCSV')
def getCSV():
    spectrum = request.args.get('spectrum')
    # file_location = request.args.get('file_location')
    basepath = os.path.dirname(__file__)  # 当前文件所在路径
    file_location = os.path.join(basepath, 'CSV\\uploads')
    result = getFilesByPath_json(file_location)
    jsonstr = json.dumps(result)
    return jsonstr



@app.route("/download/<filepath>", methods=['GET'])
def download_file(filepath):
    # 此处的filepath是文件的路径，但是文件必须存储在static文件夹下， 比如images\test.jpg
    return app.send_static_file(filepath)

@app.route("/deleteFile", methods=['GET'])
def deleteFile():
    file_name = request.args.get('file_name')
    result = FileHelper.deleteFile(file_name)
    jsonstr = json.dumps(result)
    return jsonstr

def del_file(path):
    ls = os.listdir(path)
    for i in ls:
        c_path = os.path.join(path, i)
        if os.path.isdir(c_path):
            del_file(c_path)
        else:
            os.remove(c_path)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000, debug=True, threaded=True)
