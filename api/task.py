# import youtube_dl
import time
# from .models import DownloadProgress
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings
from .youtube import YT
from .helper import create_hash
import time
import os

import logging
logger = logging.getLogger(__name__)


def get_video(mediaresource):

    youtube_process = YT(mediaresource)
    youtube_process.run()

    # add md5 to mediaresource record
    if(mediaresource.youtube_data.download_finished):
        mediaresource.md5_generated = create_hash(mediaresource.audiofile.path)
        mediaresource.save()

    # delete archive file that youtube dl creates
    if os.path.exists(settings.MEDIA_ROOT + str(mediaresource.id) + '/archive'):
        os.remove(settings.MEDIA_ROOT +
                  str(mediaresource.id) + '/archive')
        logger.info("deleting youtubedl archive file")


# def test_task():
#     time.sleep(10)

#     return "task fucntioniinsns"
    # try:
    #     newdownload = YT(vidobject.urlid, vidobject)
    #     newdownload.run()

    #     path = '/code/dl/' + vidobject.urlid
    #     from os import listdir
    #     from os.path import isfile, join
    #     onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    #     vidobject.filename = onlyfiles[0]

    #     # f = open('/code/dl/' + vidobject.urlid + '/' + onlyfiles[0],'r')
    #     # myfile = File(f)
    #     # contentfile = ContentFile(f, name=onlyfiles[0])

    #     vidobject.audiofile.name = '/code/dl/' + vidobject.urlid + '/' + onlyfiles[0]
    #     vidobject.status = "converted"
    #     vidobject.save()
    # except:
    #     return vidobject

    # return vidobject
