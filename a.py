from flask import Flask, render_template, send_from_directory, url_for, request, redirect, after_this_request, make_response
import os
import shutil
import logging
import datetime
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 8*1024*1024*1024*100
directory = 'data\\'
# remove = 0
# logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
# handler = logging.FileHandler('logs.log') # creates handler for the log file
# logger.addHandler(handler) # adds handler to the werkzeug WSGI logger

@app.route('/')
@app.route('/<string:a>')
def mainpage(a=''):
    if str(request.cookies.get('login'))!='None':
        # print(request.cookies.get('login'))
        return redirect('/get/'+request.cookies.get('login'))
    else:
        return render_template('index1.html', a = a)


@app.route('/get')
@app.route('/get/')
@app.route('/get/<path:a>')
def main(a=''):
    folder_path = os.path.join(directory, a)
    id = request.cookies.get('login')
    if os.path.isfile(folder_path):
        if 'all' in a or id in a or id == 'Shresth':
            return send_from_directory(os.path.dirname(folder_path), os.path.basename(folder_path), as_attachment=True)
        else:
            return redirect('/')
    files = os.listdir(folder_path)
    folders = [f for f in files if os.path.isdir(os.path.join(folder_path, f))]
    files = [f for f in files if os.path.isfile(os.path.join(folder_path, f))]
    b = a[:]
    if b != '' and '/' in b:
        while b[-1] != '/':
            b = b[:-1]
        b = b[:-1]
        b = '/'+b
    else:
        b = '/'
    if 'all' in a or id in a or id == 'Shresth':
        return render_template('index.html', folders=folders, files=files, folder=a, b='/get/'+b)
    else:
        return redirect('/')
        

@app.route('/fol')
@app.route('/fol/<path:g>')
@app.route('/fol/<path:g>/')
def fol(g = ''):
    folder_path = os.path.join(directory, g)
    shutil.make_archive(str(folder_path)+'', 'zip', folder_path)
    return send_from_directory(os.path.dirname(folder_path), os.path.basename(str(folder_path)+'.zip'), as_attachment=True)
    
    
@app.route('/delete')
@app.route('/delete/<path:c>')
def delete(c = ''):
    try:
        folder_path = os.path.join(directory, c)
        if len(c.split('/')) <= 1:
            return redirect('/')
        # os.rmdir(folder_path)
        shutil.rmtree(folder_path, ignore_errors = True)
        # return 'DONE'
        if '/' in c:
            while c[-1] != '/':
                c = c[:-1]
        if '/' in c:
            return redirect('/get/'+c[:-1])
        else:
            return redirect('/')
    except Exception as e:
        return str(e)

@app.route('/deletefile')
@app.route('/deletefile/<path:d>')
def deletefile(d = ''):
    try:
        folder_path = os.path.join(directory, d)
        # return str(folder_path)
        os.remove(folder_path)
        if '/' in d:
            while d[-1] != '/':
                d = d[:-1]
        if '/' in d:
            return redirect('/get/'+d[:-1])
        else:
            return redirect('/get/')
        # return redirect('/'+d)
    except Exception as e:
        return str(e)

@app.route('/create', methods = ['POST'])
@app.route('/create/<path:e>', methods = ['POST'])
def createfolder(e = ''):
    if e == 'thehomepage':
        e = ''
    path = os.path.join(directory, e)
    name = request.form['name']
    os.makedirs(os.path.join(path, name))
    return redirect('/get/'+e)
    # return 'done'

@app.route('/upload', methods=['POST'])
@app.route('/upload/<path:folder>/', methods=['POST'])
@app.route('/upload/<path:folder>', methods=['POST'])
def upload_file(folder=''):
    if folder == 'thehomepage':
        folder = ''
    folder_path = os.path.join(directory, folder)
    files = request.files.getlist("file")
    for file in files:
        file.save(os.path.join(folder_path, file.filename))
    expected_size = request.content_length
    file_length = os.path.getsize(os.path.join(folder_path, file.filename))
    file_size = os.path.getsize(os.path.join(folder_path, file.filename))
    while True:
        uploaded_bytes = os.path.getsize(os.path.join(folder_path, file.filename))
        progress = int((uploaded_bytes / file_size) * 100)
        if progress >= 95:
            break
        print(f'Upload progress: {progress}%')
    return redirect('/get/'+folder)

@app.route('/upload1', methods=['POST'])
@app.route('/upload1/<path:folder>/', methods=['POST'])
@app.route('/upload1/<path:folder>', methods=['POST'])
def upload_file1(folder=''):
    if folder == 'thehomepage':
        folder = ''
    folder_path = os.path.join(directory, folder)
    files = request.files.getlist("file1")
    os.chdir(folder_path)
    for i in files:
        # print(i.filename)
        initials = i.filename.split('/')
        path = ''
        for g in initials[:-1]:
            path+=g+'/'
            if not os.path.exists(path):
                os.mkdir(path)
        i.save(os.path.join(folder_path, i.filename))
        
    return redirect('/get/'+folder)
    # return str(expected_size)+str('adjk;f')+str(file_length)
    
@app.route('/signup', methods = ['POST', 'GET'])
@app.route('/signup/', methods = ['POST', 'GET'])
def sign_up():
    if str(request.cookies.get('login'))!='None':
        # print(request.cookies.get('login'))
        return redirect('/get/'+request.cookies.get('login'))
    id = request.form['id']
    passw = request.form['pass']
    file = open('accounts', 'r')
    read = file.read().split('\n')
    res = make_response(redirect('/'))
    for i in read:
        if i.split(':')[0] == id:
            return redirect('/a')
    # print(str(id)+':'+str(passw))
    if not os.path.exists(os.path.join(directory, str(id))):
        os.mkdir(os.path.join(directory, str(id)))
    file = open('accounts', 'a')
    file.write(str(id)+':'+str(passw)+'\n')
    res = make_response(redirect('/'))
    expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)
    res.set_cookie("login", value=str(id), expires = expiration_date)
    return res
    # return redirect('/get/'+str(id))
@app.route('/signin', methods = ['POST', 'GET'])
@app.route('/signin/', methods = ['POST', 'GET'])
def sign_in():
    if str(request.cookies.get('login'))!='None':
        # print(request.cookies.get('login'))
        return redirect('/get/'+request.cookies.get('login'))
    id = request.form['id']
    passw = request.form['pass']
    # print(str(id)+':'+str(passw))
    # if not os.path.exists(os.path.join(directory, str(id))):
    #     os.mkdir(os.path.join(directory, str(id)))
    file = open('accounts', 'r')
    read = file.read().split('\n')
    res = make_response(redirect('/'))
    for i in read:
        if i.split(':')[0] == id:
            if i.split(':')[1] == passw:
                expiration_date = datetime.datetime.now() + datetime.timedelta(days=30)
                res.set_cookie("login", value=str(id), expires = expiration_date)
                return res
            else:
                return redirect('/w')
    
    return redirect('/n')
                
    # return res
    # return redirect('/get/'+str(id))

@app.route('/logout/')
def logout():
    if str(request.cookies.get('login'))=='None':
        # print(request.cookies.get('login'))
        return redirect('/')
    else:
        res = make_response(redirect('/'))
        res.set_cookie("login", value='None', expires = 0)
        return res


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5000')