FROM tiangolo/uwsgi-nginx-flask:latest

#RUN pip install --upgrade pip==9.0.1
RUN pip3 install numpy scipy pandas pillow urllib3 scikit-learn opencv-python flask-restful flask 
RUN pip install requests

RUN apt-get update
RUN apt-get install libjpeg-turbo-progs -y


CMD [ "python", "smush/main.py" ]
#sudo docker build -t image-enhancement .
#docker run --name dEnhancement -p 9001:5000 -v /home/arindam/Desktop/projects/ImageCpression/smush.py/:/app/ -it image-enhancement
