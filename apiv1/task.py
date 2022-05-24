# import youtube_dl 
import time
from .models import Resource
from django.core.files.base import ContentFile
from django.core.files import File

from .youtube import YT

def get_video(vidobject):
    print("THE URL: " + vidobject.url)

    try:
        newdownload = YT(vidobject.urlid, vidobject)
        newdownload.run()

        path = '/code/dl/' + vidobject.urlid
        from os import listdir
        from os.path import isfile, join
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        vidobject.filename = onlyfiles[0]
        
        # f = open('/code/dl/' + vidobject.urlid + '/' + onlyfiles[0],'r')
        # myfile = File(f)
        # contentfile = ContentFile(f, name=onlyfiles[0])

        vidobject.audiofile.name = '/code/dl/' + vidobject.urlid + '/' + onlyfiles[0]
        vidobject.status = "converted"
        vidobject.save()
    except:
        return vidobject

    return vidobject