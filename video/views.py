from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, StreamingHttpResponse, HttpResponseServerError
from django.urls import reverse
from django.contrib import messages
from django.views.decorators import gzip
import cv2
import time
import base64

imagen_base64 = None
imagen_read = None

# Create your views here.
def index(request):
    return render(request,'index.html', {'inicia_captura':False, "imagen_capturada":None})

def iniciar_video(request):
    return render(request,'index.html', {'inicia_captura':True, "imagen_capturada":imagen_base64})

def detener_video(request):
    if imagen_read is not None:
        cv2.imwrite("media/opencv/test.jpg", imagen_read)
    
    return render(request,'index.html', {'inicia_captura':False, "imagen_capturada":imagen_base64})

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    def __del__(self):
        print("del")
        self.video.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        try:
            _,image = self.video.read()                
            _,jpeg = cv2.imencode('.jpg', image)            

            global imagen_base64
            global imagen_read 
            frame_b64 = base64.b64encode(jpeg)
            imagen_base64 = frame_b64.decode("utf-8")
            imagen_read = image

            return jpeg.tobytes()
        except KeyboardInterrupt:
            self.video.release()
            cv2.destroyAllWindows()
            exit(0)
        except Exception:
            self.video.release()
            cv2.destroyAllWindows()
            exit(0)
            
def gen(camera):
    try:
        while True:
            frame = camera.get_frame()
            yield(b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    except:
        print("aborted 2")

@gzip.gzip_page
def live_video(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("aborted")


'''

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        (self.grabbed, self.frame) = self.video.read()
        threading.Thread(target=self.update, args=()).start()

    def __del__(self):
        self.video.release()

    def get_frame(self):
        image = self.frame
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def update(self):
        while True:
            (self.grabbed, self.frame) = self.video.read()

cam = VideoCamera()

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@gzip.gzip_page
def live_video(request):
    try:
        return StreamingHttpResponse(gen(VideoCamera()), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        print("aborted")

'''