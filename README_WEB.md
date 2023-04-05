# PHOTOMOSAICS

Simple photomosaics program using OpenCV in python. Also contains a web server able to execute the program. You can find the github repository [here](https://github.com/Fastrings/Photomosaics).

<figure>
  <img
  src="https://raw.githubusercontent.com/Fastrings/Photomosaics/master/out.png"
  alt="Photomosaics example">
  <figcaption>Above, the input image on the left and the result on the right, using a tile size of 30</figcaption>
</figure>

## PREREQUISITES

This project uses packages that are not in the python standard library, meaning it is needed to install them (using pip for example). Please refer to the [requirements](https://github.com/Fastrings/Photomosaics/blob/master/requirements.txt) file for a list of all the packages needed to make the project work properly.

## HOW TO USE

Add all the images you want to see in the final results to the [source](https://github.com/Fastrings/Photomosaics/tree/master/Source_Images) folder. <br>
Simply run:

- ``python photomosaics.py 'input' 'tile_size'`` 

With 'input' being the path to your input image and 'tile_size' being the precision you want to use. Keep in mind that the lower 'tile_size' is, the more precise the output will be, meaning the program will take to run.

## HTTP SERVER

This project contains an http server used to run the photomosaic logic. Send a POST request to the /process_image endpoint and the server will include in the response the image resulting from running the photomosaics program. Make sure to include an image and the tile_size of you choosing to the request.

To run the server, simply run:

- ``python server.py``

It will launch the server in your current terminal window.

Once this is done, you can use any tool of your choosing, like cURL or Postman, to request the server.

For example, here is a request using cURL:

```
curl -X POST -F 'image=@image.jpg' -F 'tile_size=-1' [url]
```

Obviously, don't forget to replace some arguments:
- image.jpg by the path to your image
- -1 by an actual tile size you want to use
- [url] by the url of your own server. If you use mine, the url is: http[]()://localhost:8000/process_image

## DOCKER

For this section, you need to have docker installed. Please refer to the [Docker docs](https://docs.docker.com/) for more information.

WARNING: If you also followed the [HTTP Server](#http-server) section, don't forget to stop the server before running the docker container, or make sure that they are not both running on the same port.

Once Docker is installed on your machine, navigate to the root of this project and run the following commands

- ``docker build -t 'name' . `` -> Building the docker image, with any 'name' you want. Do not forget the '.', it is important.
- ``docker run -d -p 8000:8000 'name'`` -> Launch a docker container based off the image you created just before. Replace 'name' with the name of the image you just created.

## PHOTO CREDITS

- Source Images
    - Images taken from [T91 Dataset](https://www.kaggle.com/datasets/ll01dm/t91-image-dataset) on Kaggle.
    - Images taken from [A to Z Flowers - Features & Images](https://www.kaggle.com/datasets/kkhandekar/a-to-z-flowers-features-images) on Kaggle.
- Example Image Input
    - Photo by James Wheeler from Pexels: https://www.pexels.com/photo/symmetrical-photography-of-clouds-covered-blue-sky-1486974/