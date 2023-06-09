from flask import Flask, request, Response, render_template
import cv2, io
import numpy as np
from photomosaics import photomosaics, color_distance_deltaE, color_distance_euclid

app = Flask(__name__)

def process_image(img, tile_size, method, format):
    npimg = np.frombuffer(img, np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    img = photomosaics(img, tile_size, method)
    img = cv2.resize(img, (500, 500))
    _, img_encoded = cv2.imencode(format, img)
    return io.BytesIO(img_encoded)

def get_format(input_format):
    if input_format is None or input_format == 'jpg':
        return '.jpg'
    elif input_format == 'png':
        return '.png'
    else:
        raise Exception(f'Invalid format provided: {input_format}')

def get_method(input_method):
    if input_method == 'deltaE':
        return color_distance_deltaE
    elif input_method == 'euclid':
        return color_distance_euclid
    else:
        raise Exception(f'Invalid color distance method provided: {input_method}')
    
def get_content_type(input_content):
    if input_content == '.jpg':
        return 'image/jpeg'
    elif input_content == '.png':
        return 'image/png'
    else:
        raise Exception(f'File format unknown: {input_content}')

def get_tile_size(input_tile):
    tile_size = int(input_tile)
    if tile_size > 500 or tile_size <= 0:
            raise Exception(f'Invalid tile_size: {tile_size}')
    
    return tile_size

@app.route("/", methods=['GET'])
def home():
    return render_template('photomosaics.html')

@app.route('/readme', methods=['GET'])
def readme():
    return render_template('readme.html')

@app.route('/process_image', methods=['POST'])
def process_request():
    try:
        if 'image' not in request.files:
            return Response('No image file uploaded', status=400)
        if 'tile_size' not in request.form:
            return Response('No tile size provided', status=400)
        if 'method' not in request.form:
            return Response('No color distance method provided', status=400)
        
        img = request.files['image'].read()
        format = get_format(request.form.get('format', None))
        method = get_method(request.form['method'])
        tile_size = get_tile_size(request.form['tile_size'])
        
        img_bytes = process_image(img, tile_size, method, format)
        content_type = get_content_type(format)

        return Response(img_bytes.getvalue(), content_type=content_type)
        
    except Exception as e:
        app.logger.error(f'An exception has occurred: {str(e)}')
        return Response(f'An exception has occurred: {str(e)}', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)