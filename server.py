from flask import Flask, request, Response
import cv2
import numpy as np
import io
from photomosaics import photomosaics

app = Flask(__name__)

@app.route('/process_image', methods=['POST'])
def process_image():
    try:
        if 'image' not in request.files:
            return Response('No image file uploaded', status=400)
        if 'text' not in request.form:
            return Response('No text data provided', status=400)

        img = request.files['image'].read()
        text = request.form['text']
        npimg = np.frombuffer(img, np.uint8)
        
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
        img = photomosaics(img, int(text))
        _, img_encoded = cv2.imencode('.jpg', img)
        
        img_bytes = io.BytesIO(img_encoded)
        
        response = Response(img_bytes.getvalue(), content_type='image/jpeg')
    
        return response
    
    except Exception as e:
        print(f'An exception has occurred: {str(e)}')
        return Response(f'An exception occurred: {str(e)}', status=500)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)