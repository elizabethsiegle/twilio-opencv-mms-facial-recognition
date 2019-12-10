from object_detection.utils import ops as utils_ops
import numpy as np
import cv2
import requests
import os
import sys
import matplotlib.pyplot as plt

from io import StringIO
from PIL import Image
sys.path.append("..")
from flask import Flask, request, redirect, send_from_directory
from twilio.twiml.messaging_response import MessagingResponse

DOWNLOAD_DIRECTORY = "/Users/lsiegle/Desktop/python/face_recognition"

app = Flask(__name__)
@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    """Respond to incoming with a simple text message."""
    resp = MessagingResponse()

    # Load the cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    if request.values['NumMedia'] != '0':
        # Use the message SID as a filename.
        filename = request.values['MessageSid'] + '.png'
        with open(filename, 'wb') as f:
            image_url = request.values['MediaUrl0']
            f.write(requests.get(image_url).content)
            # perform face detection
            # load the photograph
            img = cv2.imread(filename)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                img = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = img[y:y+h, x:x+w]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        plt.imsave('receivedimg.png', img)
        msg = resp.message("got your message!")
        msg.media('http://lizzie.ngrok.io/uploads/receivedimg')
    else:
        resp.message("Try sending a picture message.")

    return str(resp)


@app.route('/uploads/receivedimg', methods=['GET', 'POST'])
def uploaded_file(filename='receivedimg.png'):
    return send_from_directory(DOWNLOAD_DIRECTORY,
                               filename)


if __name__ == "__main__":
    app.run(debug=True)


