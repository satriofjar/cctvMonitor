from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
from . models import Floor, Camera

# Create your views here.
def home(request):
    floors = Floor.objects.all()
    floor = get_object_or_404(Floor, id=1)
    cameras = floor.camera_set.all()
    context = {
        'floors': floors,
        'floor': floor,
        'cameras': cameras,
    }   

    return render(request, 'base/index.html', context)


def floor_cctv(request, pk):
    floors = Floor.objects.all()
    floor = get_object_or_404(Floor, id=pk)
    cameras = floor.camera_set.all()
    context = {
        'floors': floors,
        'floor': floor,
        'cameras': cameras,
    }   

    return render(request, 'base/index.html', context)

def cctv(request, id_floor, id_camera):
    floors = Floor.objects.all()
    floor = get_object_or_404(Floor, id=id_floor)
    cameras = floor.camera_set.exclude(id=id_camera)
    camera = floor.camera_set.get(id=id_camera)
    context = {
        'floors': floors,
        'floor': floor,
        'cameras': cameras,
        'camera': camera,
    }   

    return render(request, 'base/cctv.html', context)


@csrf_exempt
def show_thumbnail(request, pk):
    # Buka koneksi ke stream RTSP
    url = 'rtsp://labs:yBtYHJ35Hk@mediastreaming.grupoavantia.com.br/Operacional/avantia_frente_sede.stream'
    camera = Camera.objects.get(id=pk)
    cap = cv2.VideoCapture(camera.url)

    # Baca frame pertama dari stream
    ret, frame = cap.read()

    # Ubah frame menjadi format gambar
    ret, buffer = cv2.imencode('.jpg', frame)
    thumbnail_data = buffer.tobytes()

    # Pastikan untuk melepaskan koneksi setelah selesai
    cap.release()

    # Tampilkan gambar thumbnail sebagai HttpResponse
    return HttpResponse(thumbnail_data, content_type='image/jpeg')


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
def camerafeed(request, pk): 
    url = "rtsp://labs:yBtYHJ35Hk@mediastreaming.grupoavantia.com.br/Operacional/avantia_frente_sede.stream"
    camera = Camera.objects.get(id=pk)
    return StreamingHttpResponse(gen(camera.url),content_type="multipart/x-mixed-replace;boundary=frame")