import os
from pathlib import Path
from zipfile import ZipFile
import zipfile 
import shutil
from io import BytesIO 
from flask import Flask, render_template, request,redirect,send_file,send_from_directory
import pickle
import time 
app = Flask(__name__)
feat =[]
fi=""
@app.route("/")
def index():
    try:
        print("Creating Workspace...")
        shutil.rmtree("received")
        shutil.rmtree("images")
        os.mkdir("images")
        os.mkdir("received")
        try:
            shutil.rmtree("yolov5")
            try:
                shutil.rmtree("yolov7")
            except:
                 print("")
        except:
            print("")
             
    except:
        print("")
    return render_template("check2.html")


@app.route("/upload",methods=['GET', 'POST'])
def upload_chunk():
    file = request.files["file"]
    file_uuid = request.form["dzuuid"]
    global fi
    fi = file_uuid
    # Generate a unique filename to avoid overwriting using 8 chars of uuid before filename.
    filename = "data.zip"
    save_path = Path("received", filename)
    current_chunk = int(request.form["dzchunkindex"])

    with open(save_path, "ab") as f:
        f.seek(int(request.form["dzchunkbyteoffset"]))
        f.write(file.stream.read())

    total_chunks = int(request.form["dztotalchunkcount"])

    # Add 1 since current_chunk is zero-indexed
    if current_chunk + 1 == total_chunks:
        # This was the last chunk, the file should be complete and the size we expect
        if os.path.getsize(save_path) != int(request.form["dztotalfilesize"]):
            return "Size mismatch.", 500

    return redirect("/jump")

@app.route("/jump",methods=['GET', 'POST'])
def item():
    print("inhere")
    try:
        with ZipFile("received/data.zip", 'r') as zip_ref:
            zip_ref.extractall("images")
    except:
        print("")

    return render_template("check.html")

@app.route("/predict", methods=['POST'])
def pred():
    features = [str(i) for i in (request.form.values())]
    global feat 
    feat = features[0]
    print(features)
    classs = features[1].split(",")
    model = pickle.load(open('model.pkl','rb'))
    a = model("images/labels","output_dir","images/images",1,yolo=int(features[0]),classes=classs,train_ratio = float(features[2]))
    cmd=""
    if int(feat)==5:
        print("YO5")
    elif int(feat)==7:
        print("YO7")
    return redirect('file-downloads')

@app.route('/file-downloads/')
def file_downloads():
    s='past_data/'+fi[:6]+"_"+"data"
    try:
        if int(feat)==5:
            shutil.make_archive(s, 'zip', 'yolov5')
        elif int(feat)==7:
            shutil.make_archive(s, 'zip', 'yolov7')
        print(s)
        return render_template('check3.html',data="yees")
    except Exception as e:
        return str(e)

@app.route('/return-files/')
def return_files_tut():
    t = fi[:6]+"_"+"data.zip"
    print(t)
    return send_from_directory(directory="past_data",path=t , as_attachment=True)

if __name__ == '__main__':
    app.run(host="localhost")