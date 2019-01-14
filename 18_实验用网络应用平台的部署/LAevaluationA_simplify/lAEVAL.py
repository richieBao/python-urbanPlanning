from flask import Flask, render_template, url_for, request, session  # 导入了Flask 类，这个类的一个实例是WSGI程序
from config import DevConfig  # 从配置文件中调入DevConfig部分配置
from exts import db
from models import Imageseval, imagesinfodf
import pandas as pd
import sqlite3
from conversionofCoordi import wgs84togcj02, gcj02tobd09
from imgPred_recognizer import predConfig
from imgPred_training import ERFTrainer
import cv2
import os

app = Flask(__name__)  # 实例化Flask类，把模块/包的名字传给它，这样Flask就会知道它将要到哪里寻找模板，静态文件之类的东西。
app.config.from_object(DevConfig)

db.init_app(app)  # 将app对象传给SQLAlchemy，初始化SQLAlchemy，并自动从app配置中读取信息，自动连接到数据库。


# db.create_all() #可以用于测试SQLAlchemy是否连接到数据库

@app.route('/')  # 使用route() 装饰器告诉Flask哪个网址将会触发之下所定义的函数。/同时可以为特定的函数生成网址，并返回想要显示在用户浏览器的信息。
def index():
    return render_template('index.html')

@app.route('/results/')  # 使用route() 装饰器告诉Flask哪个网址将会触发之下所定义的函数。/同时可以为特定的函数生成网址，并返回想要显示在用户浏览器的信息。
def results():
    evalResults = [{'name': imagename.split('/')[-1][:-4], 'value': good + 100} for imagename, good in
                   db.session.query(Imageseval.imagename, Imageseval.good).all()]
    # print(evalResults)
    locationResults = {
    imagename.split('/')[-1][:-4]: gcj02tobd09(wgs84togcj02(long, lat)[0], wgs84togcj02(long, lat)[1]) for
    imagename, long, lat in db.session.query(imagesinfodf.imagename, imagesinfodf.long, imagesinfodf.lat).all()}
    # print(locationResults)
    imgLocVal = {
        'imgLoc': locationResults,
        'imgVal': evalResults
    }
    return render_template('results.html', **imgLocVal)

@app.route('/eval/', methods=['GET', 'POST'])  # 给图片打分
def eval():
    # print(imagesinfodf.query.get(1).imagename) #测试是否能正确读取数据库数据
    context = {'imgEval': imagesinfodf.query.all(), 'imgNum': len(imagesinfodf.query.all())}
    # print(context)
    if request.method == 'GET':
        return render_template('eval.html', **context)
    else:
        image_name = request.form.get('image_path')
        imgIdx = request.form.get('image_id')
        evalRX = int(request.form.get('eval'))
        # print(image_name,' ',imgIdx,' ',evalRX)
        imgCurrent = Imageseval.query.filter(Imageseval.imagename == image_name).first()
        # print(Imageseval.query.get(1).imagename)
        # print(imgCurrent)
        if evalRX == 1:
            print('ok')
            goodV = 1
            mediumV = 0
            poorV = 0
            evalV = u"好"  # 中文一定要加u，即unicode( str_name )，否则服务器段如果是py2.7，会提示错误。
        elif evalRX == -1:
            goodV = 0
            mediumV = 0
            poorV = 1
            evalV = u"差"
        elif evalRX == 0:
            goodV = 0
            mediumV = 1
            poorV = 0
            evalV = u"中"
        else:
            pass
        # print(goodV,mediumV,poorV,evalV)
        if not imgCurrent:
            imagesevalData = Imageseval(imagename=image_name, good=goodV, medium=mediumV, poor=poorV, eval=evalV)
            db.session.add(imagesevalData)
            db.session.commit()
        else:
            queryResults = [(good, medium, poor) for good, medium, poor in
                            db.session.query(Imageseval.good, Imageseval.medium, Imageseval.poor).filter(
                                Imageseval.imagename == image_name)]
            print(queryResults)
            goodAdd = queryResults[0][0] + goodV
            mediumAdd = queryResults[0][1] + mediumV
            poorAdd = queryResults[0][2] + poorV
            if goodAdd > mediumAdd and goodAdd > poorAdd:
                evalN = u"好"
            elif mediumAdd > goodAdd and mediumAdd > poorAdd:
                evalN = u"中"
            elif poorAdd > goodAdd and poorAdd > mediumAdd:
                evalN = u"差"
            else:
                evalN = u"中"
            imagesevalDic = {'good': goodAdd, 'medium': mediumAdd, 'poor': poorAdd, 'eval': evalN}
            # print(imagesevalDic)
            Imageseval.query.filter_by(imagename=image_name).update(imagesevalDic)
            # db.session.add(imagesevalData)
            db.session.commit()

    return render_template('eval.html', **context)

@app.route('/imgprediction/')  # 图像识别/分类预测
def imgprediction():
    predInfo = predConfig().pred()
    # print(predInfo)
    # predDic={'predName':predInfo.keys(),'predValue':predInfo.values()}
    predDic = {'pred': [(key, predInfo[key]) for key in predInfo.keys()]}
    return render_template('imgprediction.html', **predDic)

if __name__ == '__main__':  # if __name__ =='__main__': 确保服务器只在直接用Python解释器执行该脚本时运行，而不会在导入模块时运行。
    app.run()  # run() 函数来运行本地服务器以及编写的应用。结束应用则在erminal终端中使用Ctrl+C。

'''
服务器端中文字符前不加u提示错误
ProgrammingError: (sqlite3.ProgrammingError) You must not use 8-bit bytestrings unless you use a text_factory 
that can interpret 8-bit bytestrings (like text_factory = str). It is highly recommended that you instead just 
switch your application to Unicode strings. [SQL: u'UPDATE imageseval SET good=?, medium=?, poor=?, eval=? WHERE 
imageseval.imagename = ?'] [parameters: (3, 0, 0, '\xe5\xa5\xbd', u'static/images/imresize/img_0321.jpg')] 
(Background on this error at: http://sqlalche.me/e/f405)

'''
