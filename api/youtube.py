import youtube_dl
from .models import MediaResource
from django.core.files.base import ContentFile
from pathlib import Path
from django.core.files import File
from django.conf import settings
from youtube_dl.utils import ExtractorError, YoutubeDLError

import re
import logging
logger = logging.getLogger(__name__)


class YT:
    def __init__(self, mediaobject):
        self.mediaobject = mediaobject
        self.filename_mp3 = ""

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
            'download_archive':
            settings.MEDIA_ROOT + str(mediaobject.id) + '/archive',
            'keepvideo': False,
            'cachedir': False,
            # 'forcetitle':
            # True,
            # 'writeinfojson':
            # '/code/dl/' + str(mediaobject.id),
            'restrictfilenames': True,
            'outtmpl': settings.MEDIA_ROOT + str(mediaobject.id) + '/temp/%(title)s.%(ext)s',
        }

    def my_hook(self, d):
        if d['status'] == 'downloading':
            progress = (d['downloaded_bytes']/d['total_bytes'])*100
            self.mediaobject.youtubedata.eta = d['eta']
            self.mediaobject.youtubedata.elapsed = d['elapsed']
            self.mediaobject.youtubedata.speed = d['speed']
            self.mediaobject.youtubedata.downloadprogress = progress
            self.mediaobject.youtubedata.save()
        if d['status'] == 'error':
            self.mediaobject.youtubedata.status = "FAILED"
            self.mediaobject.youtubedata.save()
        if d['status'] == 'finished':
            path = Path(d['filename'])
            if path.is_file():
                # print(path.name)
                # print(path.stem)
                self.filename_mp3 = '/temp/' + path.stem + '.mp3'

    def run(self):
        youtube_target_url = "https://youtube.com/watch?v=" + \
            str(self.mediaobject.youtubedata.youtube_id)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            extracted_info = None
            extracted_info = ydl.extract_info(youtube_target_url,
                                              download=False,
                                              ie_key=None,
                                              extra_info={},
                                              process=True,
                                              force_generic_extractor=False)
            # check if genre is there
            try:
                self.mediaobject.genre = extracted_info["genre"]
                logger.info("genre found")
            except:
                logger.info("genre not available")

            self.mediaobject.title = extracted_info["title"]
            self.mediaobject.description = extracted_info["description"]
            self.mediaobject.save()

            ydl.download([youtube_target_url])
            path = Path(settings.MEDIA_ROOT +
                        str(self.mediaobject.id) + self.filename_mp3)
            if path.is_file():
                # print(f'The file {self.filename_mp3} exists')
                with path.open(mode='rb') as f:
                    self.mediaobject.audiofile = File(f, path.name)
                    self.mediaobject.audiofile.name = path.name
                    self.mediaobject.youtubedata.status = 'DONE'
                    self.mediaobject.youtubedata.save()
                    self.mediaobject.save()
                    return True
            else:
                self.mediaobject.youtubedata.status = 'FAILED'
                self.mediaobject.youtubedata.save()
                self.mediaobject.youtubedata.error = "Failed to download file"
                self.mediaobject.save()

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
