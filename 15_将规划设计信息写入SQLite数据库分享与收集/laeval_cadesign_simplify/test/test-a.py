from flask import Flask,request,make_response
import datetime

app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello Flask!'

@app.route('/user/<name>')
def user(name):
    return '<h1>Hello,%s!</h1>'% name

@app.route('/set_cookie')
def set_cookie():
    outdate = datetime.datetime.today() + datetime.timedelta(days=30)
    response=make_response('<h1>this doc carries a cookie!</h1>')
    response.set_cookie('name','caDesign',expires=outdate)
    return response

@app.route('/get_cookie')
def get_cookie():
    name=request.cookies.get('name')
    print('##################################################',name)
    return name

@app.route('/del_cookie')
def del_cookie():
    response=make_response('delete cookie')
    response.set_cookie('Name','',expires=0)
    return response

@app.route('/del_cookie2')
def del_cookie2():
    response=make_response('delete cookie2')
    response.delete_cookie('Name')
    return response

if __name__ == '__main__':
    app.run()