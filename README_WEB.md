# PHOTOMOSAICS

Simple photomosaics program using OpenCV in python. You can find the github repository [here](https://github.com/Fastrings/Photomosaics).

The photomosaic algorithm is a way to create a large image by using smaller images as tiles. Each tile is chosen to best match the colors of the corresponding section of the large image.

<figure>
  <img
  src="https://raw.githubusercontent.com/Fastrings/Photomosaics/master/out.png"
  alt="Photomosaics example">
  <figcaption style="text-align: center;">Above, the input image on the left and the result on the right, using a tile size of 30.</figcaption>
</figure>

## HOW IT WORKS

The input image is first resized to be an exact multiple of the tile size.

Then, the library of images is loaded and a [KDTree](https://en.wikipedia.org/wiki/K-d_tree) is constructed from the average colors of the library images. 

A blank output image is created with the same dimensions as the input image. 

The script then loops through each tile in the input image, finds the best matching library image, and pastes it onto the corresponding section of the output image.

## PREREQUISITES

This project uses packages that are not in the python standard library, meaning it is needed to install them (using pip for example). Please refer to the [requirements](https://github.com/Fastrings/Photomosaics/blob/master/requirements.txt) file for a list of all the packages needed to make the project work properly.

## HOW TO USE

Beforehand, add all the images you want to see in the final results to the [source](https://github.com/Fastrings/Photomosaics/tree/master/Source_Images) folder.

To launch the program, simply run:

```bash
python photomosaics.py -i 'input' -t 'tile_size' -m 'method'
``` 

With:
- 'input' being the path to your input image (only jpeg format is supported for now)
- 'tile_size' being the precision you want to use. Keep in mind that the lower 'tile_size' is, the more precise the output will be, meaning the program will take longer to run.
- 'method' being the color distance method you want to use. Only 2 are supported as of right now: euclid (for [Euclidean Distance](https://en.wikipedia.org/wiki/Euclidean_distance)) or deltaE (for [delta E color distance](https://en.wikipedia.org/wiki/Color_difference#CIEDE2000)).

For a more complete description of how to use this program, you can run the following command in the terminal:

```bash
python photomosaics.py -h
```

## HTTP SERVER

This project contains an http server used to run the photomosaic logic. Send a POST request to the /process_image endpoint and the server will include in the response the image resulting from running the photomosaics program. Make sure to include an image and the tile_size of your choosing to the request.

Running the server works differently depending on the OS you are using.

On Windows, you can install [waitress](https://docs.pylonsproject.org/projects/waitress/) or [mod_wsgi](https://modwsgi.readthedocs.io/). In development I chose to use the former but if you want to use the latter, please refer to their documentation as there are a few more steps necessary to run the server. You can run waitress like so:

```bash
waitress-serve --host 127.0.0.1 --port 8000 server:app
```

On UNIX, you can install any WSGI server of your choosing. I personnally used [Gunicorn](https://gunicorn.org/) to replace the flask development server in the docker implementation. You can run gunicorn like so:

```bash
gunicorn --workers 1 --timeout 0 --bind 0.0.0.0:8000 server:app
```

It will launch the server in your current terminal window.

Once this is done, you can use any tool of your choosing, like cURL or Postman, to request the server.

For example, here is a request using cURL:

```bash
curl -X POST -F 'image=@image.jpg' -F 'tile_size=-1' [url]
```

Obviously, don't forget to replace some arguments in the request above:
- image.jpg by the path to your image
- -1 by an actual tile size you want to use
- [url] by the url of your own server. If you use mine, the url is: http[]()://localhost:8000/process_image

## DOCKER

For this section, you need to have docker installed. Please refer to the [Docker docs](https://docs.docker.com/) for more information.

WARNING: If you also followed the [HTTP Server](#http-server) section, don't forget to stop the server before running the docker container, or make sure that they are not both running on the same port.

Once Docker is installed on your machine, navigate to the root of this project and run the following commands:

```bash
docker build -t 'name' . 
``` 
This will build the docker image, with any 'name' you want. Do not forget the '.', it is important.

```bash
docker run -d -p 8000:8000 'name'
```
This launches a docker container based off the image you created just before. Replace 'name' with the name of the image you just created.

## PHOTO CREDITS

- Source Images
    - Images taken from [T91 Dataset](https://www.kaggle.com/datasets/ll01dm/t91-image-dataset) on Kaggle.
    - Images taken from [A to Z Flowers - Features & Images](https://www.kaggle.com/datasets/kkhandekar/a-to-z-flowers-features-images) on Kaggle.
- Example Image Input
    - Photo by James Wheeler from Pexels: https://www.pexels.com/photo/symmetrical-photography-of-clouds-covered-blue-sky-1486974/