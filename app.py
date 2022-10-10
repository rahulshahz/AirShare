import os
from flask import Flask, request, redirect, render_template,url_for
import random
from stat import S_ISREG, ST_CTIME, ST_MODE
import os, sys, time
from flask import send_file
app = Flask(__name__)
@app.route('/')
def hello():
    lst=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9','a', 'b', 'c', 'd', 'e', 'f', 'g', 'h',
                     'i', 'j', 'k', 'm', 'n', 'o', 'p', 'q',
                     'r', 's', 't', 'u', 'v', 'w', 'x', 'y',
                     'z']
    str=''
    for i in range(16):

        str=str+random.choice(lst)
    print(str)
    l=list(str)
    random.shuffle(l)
    str=''.join(l)
    current_directory = os.getcwd()
    current_directory=current_directory+"/static/"
    final_directory = os.path.join(current_directory, str)
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    return render_template("next.html",str=str)

@app.route('/<string:str>',methods=['GET','POST'])

def show(str):
    if request.method=='POST':
        UPLOAD_FOLDER=os.getcwd()+"/static/"+str
        app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
        files = request.files.getlist("file")
        for file in files:
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return redirect('/{str}'.format(str=str))
    dirpath = "static/{str}/".format(str=str)

    # get all entries in the directory w/ stats
    entries = (os.path.join(dirpath, fn) for fn in os.listdir(dirpath))
    entries = ((os.stat(path), path) for path in entries)

    # leave only regular files, insert creation date
    entries = ((stat[ST_CTIME], path)
               for stat, path in entries if S_ISREG(stat[ST_MODE]))
    #NOTE: on Windows `ST_CTIME` is a creation date 
    #  but on Unix it could be something else
    #NOTE: use `ST_MTIME` to sort by a modification date
    lstdate=[]
    lstpath=[]
    
    for cdate, path in sorted(entries):
        
        lstdate.append(time.ctime(cdate))
        lstpath.append(os.path.basename(path))
    d1=zip(lstpath,lstdate)
        # print(time.ctime(cdate), os.path.basename(path))
    
    
    return render_template("file.html",string=str,d1=d1)

@app.route('/static/<string:str>/<string:path>/Delete')
def world(path,str):
    location='./static/'+str+'/'+path
    print(location)
    if os.path.isfile(location):
        os.remove(location)
        print("File has been deleted")
        
    else:
        print("File does not exist")
    return redirect(url_for("show",str=str))
    
if __name__=="__main__":
    app.run(port=8090)