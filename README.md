# ImageCompressionEnhancement

# Compression and enhancement of Image Quality

## Problem 🌍 
With plethora of images transferring between client and server we sometimes choke the bandwidth. Companies that primarily play with images face repeated problem of ***image movement***, ***cost*** and ***poor quality***. Considering the speed of development I have integrated 'high quality' lossy image compression and image quality enhancement project of mine. 

## Installation instructions 
The project run inside docker container so you do not need to worry about any installation. Just follow simple instructions.

Download the project using
```bash
git clone https://github.com/arindammalik/ImageCompressionEnhancement.git
```
### Installation and playing with docker images

Install docker if already not installed through below link
Linux [🔗](https://docs.docker.com/engine/install/ubuntu/)
Windows [🔗](https://docs.docker.com/docker-for-windows/install/)
MacOS [🔗](https://docs.docker.com/docker-for-mac/install/)


### Go inside the root folder
```
cd ImageCompressionEnhancement
```

### Create docker image from Docker File inside 
#### Linux
```
docker build .
```

Check if docker image has been successfully created:
```
docker images
``` 
Let's say your docker image name is imagecompressionimage

Use following command to run docker instance 
```
docker run --name dEnhancement -p 9001:5000 -v ImageCompressionEnhancement/:/app/ --memory=4000m -dit imagecompressionimage
```

### Want to try the API you created? Try the API you created 
#### POST url:
```
http://localhost:9001/api/compressImage?url=https://brieftake.com/wp-content/uploads/2019/09/ad-f.jpg&fileName=dummy102-3.jpeg
```


#### You can also use the following curl for ease:
```
curl --location --request GET 'http://localhost:9001/api/compressImage?url=https://brieftake.com/wp-content/uploads/2019/09/ad-f.jpg&fileName=dummy102-3.jpeg'
```

![pageres](MainPic.jpg "Main")


###This will return compressed image with ***~83% reduced size*** and of ***enhanced quality***.


croppedImage
![pageres](CompressedImage.jpg "Result")



## Stuck somewhere?
Please feel free to reach out to me here:
[Arindam Malik](mailto:arindammalik96@gmail.com)
