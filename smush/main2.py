from flask import Flask,request,send_file
from flask_restful import reqparse
from smush import *
import os
import uuid
import gc
import threading
from datetime import datetime
import time
#author Arindam Malik
#April 2020

#app = Flask(__name__)
#parser = reqparse.RequestParser()

'''@app.route("/")
def hello():
    return "Image Compression is up and running."
'''
#@app.route('/api/compressImage', methods=['GET', 'POST'])
def compressEnhanceImage():
    now = datetime.now()
    current_milli_time = lambda: int(round(time.time() * 1000))
    
    f = open(os.getcwd()+"/threadId2", "a")
    f.write("\n"+str(threading.get_ident())+"  "+now.strftime("%d/%m/%Y %H:%M:%S")+"  "+str(current_milli_time()))
    f.close()
    gc.collect()
    #parser.add_argument("url")
    #parser.add_argument("fileName")
    #args = parser.parse_args()
    #fileName='abc'
    id = str(uuid.uuid4()) 
    requestUrl = 'https://serving.photos.photobox.com/77093964967b1fee88321e5249f44a859d495c423a178eabd485538c47cf0fc9e928c80c.jpg'
    requestPath = os.getcwd()+"/imagesProcessingNew/"+'img5'
    if requestUrl:
        getImage(requestUrl,requestPath)
        #imageToReturn=send_file(requestPath, mimetype='image/jpeg', as_attachment=True)
        #os.remove(requestPath)
        #return imageToReturn
    #return "unsufficient data"  

def main():
    compressEnhanceImage()
main()
#if __name__ == '__main__':
#    app.run(host='0.0.0.0', debug=True, port=5000)
