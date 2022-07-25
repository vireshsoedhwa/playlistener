import youtube_dl
from .models import MediaResource, DownloadProgress
from django.core.files.base import ContentFile
from django.core.files import File
from django.conf import settings

import re
import logging
logger = logging.getLogger(__name__)


class YT:
    def __init__(self, mediaobject):
        self.mediaobject = mediaobject

        self.ydl_opts = {
            'writethumbnail': True,
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            },
                {'key': 'EmbedThumbnail', }],
            'logger':
            MyLogger(),
            'progress_hooks': [self.my_hook],
            # 'download_archive': '/code/dl/archive',
            'download_archive':
            settings.MEDIA_ROOT + str(mediaobject.id) + '/archive',
            'keepvideo': False,
            'cachedir': False,
            # 'forcetitle':
            # True,
            # 'writeinfojson':
            # '/code/dl/' + str(mediaobject.id),
            'restrictfilenames': True,
            # 'outtmpl': '/code/dl/%(id)s/%(title)s.%(ext)s',
            'outtmpl': settings.MEDIA_ROOT + str(mediaobject.id) + '/%(title)s.%(ext)s',
        }

        self.downloadprogress = DownloadProgress.objects.create(
            object=mediaobject)
        self.downloadprogress.save()

    def my_hook(self, d):
        print(d['status'])
        if d['status'] == 'downloading':
            progress = (d['downloaded_bytes']/d['total_bytes'])*100
            self.downloadprogress.eta = d['eta']
            self.downloadprogress.elapsed = d['elapsed']
            self.downloadprogress.speed = d['speed']
            self.downloadprogress.progress = progress
            self.downloadprogress.save()
        if d['status'] == 'error':
            self.mediaobject.download_finished = False
            self.mediaobject.busy = False
            self.mediaobject.save()
        if d['status'] == 'finished':
            get_just_filename = re.search(r"(.*\/)([^\/]*)\.[a-zA-Z0-9]*",
                                          d['filename'])
            self.mediaobject.audiofile.name = get_just_filename.group(
                1) + get_just_filename.group(2) + ".mp3"
            self.mediaobject.download_finished = True
            self.mediaobject.busy = False
            self.mediaobject.save()

    def run(self):
        youtube_target_url = "https://youtube.com/watch?v=" + \
            str(self.mediaobject.youtube_id)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            jsontry = ydl.extract_info(youtube_target_url,
                                       download=False,
                                       ie_key=None,
                                       extra_info={},
                                       process=True,
                                       force_generic_extractor=False)

            # check if genre is there
            try:
                self.mediaobject.genre = jsontry["genre"]
                logger.info("genre found")
            except:
                logger.info("genre not available")

            self.mediaobject.title = jsontry["title"]
            self.mediaobject.description = jsontry["description"]
            self.mediaobject.download_finished = False
            self.mediaobject.busy = True
            self.mediaobject.save()
            ydl.download([youtube_target_url])


class MyLogger(object):

    def debug(self, msg):
        if settings.DEBUG:
            logger.info(msg)
        pass

    def warning(self, msg):
        logger.warn(msg)
        pass

    def error(self, msg):
        logger.error(msg)


# for reference
# {'status': 'downloading', 'downloaded_bytes': 17131, 'total_bytes': 17131, 'tmpfilename':
# '/code/dl/tPEE9ZwTmy0/Shortest Video on Youtube.m4a.part', 'filename':
# '/code/dl/tPEE9ZwTmy0/Shortest Video on Youtube.m4a', 'eta': 0, 'speed':
# 128899.3488425494, 'elapsed': 0.43769383430480957, '_eta_str': '00:00',
# '_percent_str': '100.0%', '_speed_str': '125.88KiB/s', '_total_bytes_str': '16.73KiB'}
