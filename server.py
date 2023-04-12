from flask import Flask, request, Response, render_template
import cv2
import numpy as np
import io
from photomosaics import photomosaics, color_distance_deltaE, color_distance_euclid

app = Flask(__name__)

@app.route("/", methods=['GET'])
def hello_world():
    return render_template('index.html')

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return Response('No image file uploaded', status=400)
        if 'tile_size' not in request.form:
            return Response('No tile size provided', status=400)
        if 'method' not in request.form:
            return Response('No color distance method provided', status=400)

        img = request.files['image'].read()
        tile_size = int(request.form['tile_size'])
        if tile_size > 500 or tile_size <= 0:
            raise Exception(f'Invalid tile_size: {tile_size}')
        if request.form['method'] not in ["deltaE", "euclid"]:
            raise Exception(f'Invalid color distance method')
        method = color_distance_deltaE if request.form['method'] == "deltaE" else color_distance_euclid

        npimg = np.frombuffer(img, np.uint8)
        
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        img = photomosaics(img, tile_size, method)
        img = cv2.resize(img, (500, 500))
        _, img_encoded = cv2.imencode('.jpg', img)
        
        img_bytes = io.BytesIO(img_encoded)
        
        response = Response(img_bytes.getvalue(), content_type='image/jpeg')
    
        return response
    
    except Exception as e:
        print(f'An exception has occurred: {str(e)}')
        return Response(f'An exception occurred: {str(e)}', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)