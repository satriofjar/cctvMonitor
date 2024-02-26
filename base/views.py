from django.shortcuts import render
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import cv2
import vlc
import time

# Create your views here.
def home(request):
    context = {

    }

    return render(request, 'base/index.html', context)

def cctv(request):
    context = {

    }

    return render(request, 'base/cctv.html', context)


@gzip.gzip_page
def stream(request):
    # Inisialisasi VLC Player
    instance = vlc.Instance()
    player = instance.media_player_new()

    # URL stream RTSP
    rtsp_url = 'rtsp://labs:yBtYHJ35Hk@mediastreaming.grupoavantia.com.br/Operacional/avantia_frente_sede.stream'


    # Buka stream
    media = instance.media_new(rtsp_url)
    player.set_media(media)

    # Callback untuk handle streaming
    def stream_generator():
        while True:
            # Jika player udah play, kirim frame video ke client
            if player.get_state() == vlc.State.Playing:
                video_frame = player.video_get_size()
                if video_frame:
                    frame, width, height, pitch = player.video_get()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
                # time.sleep(0.04)  # Delay untuk menjaga kecepatan streaming
                time.sleep(0.4)
            else:
                # time.sleep(0.1)  # Jika belum play, tunggu sebentar
                time.sleep(1)  # Jika belum play, tunggu sebentar

    # Setting HTTP response sebagai streaming
    return StreamingHttpResponse(stream_generator(), content_type='multipart/x-mixed-replace; boundary=frame')


def gen(camera):
    video = cv2.VideoCapture()
    video.open(camera)
    print("streaming live feed of ",camera)
    while True:
        success, frame = video.read()  
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#url:"localhost:8000/camera_feed"
def camerafeed(request): 
    return StreamingHttpResponse(gen("rtsp://labs:yBtYHJ35Hk@mediastreaming.grupoavantia.com.br/Operacional/avantia_frente_sede.stream"),content_type="multipart/x-mixed-replace;boundary=frame")