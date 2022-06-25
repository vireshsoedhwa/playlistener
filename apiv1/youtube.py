import youtube_dl
from .models import MediaResource
from django.core.files.base import ContentFile
from django.core.files import File

import re

class YT:

    def __init__(self, mediaobject):
        self.mediaobject = mediaobject

        self.ydl_opts = {
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '320',
            }],
            'logger':
            MyLogger(),
            'progress_hooks': [self.my_hook],
            # 'download_archive': '/code/dl/archive',
            'download_archive':
            '/code/dl/' + str(mediaobject.id) + '/archive',
            'keepvideo': False,
            'cachedir': False,
            # 'forcetitle':
            # True,
            # 'writeinfojson':
            # '/code/dl/' + str(mediaobject.id),
            'restrictfilenames': True,
            'outtmpl': '/code/dl/%(id)s/%(title)s.%(ext)s',
        }

    def my_hook(self, d):
        print(d['status'])
        if d['status'] == 'downloading':
            # print('Downloadingg it ' + str(d['downloaded_bytes']) + "/" +
            #       str(d['total_bytes']))
            pass
        if d['status'] == 'error':
            print('Error happened')
            self.mediaobject.busy = False
            self.mediaobject.save()
        if d['status'] == 'finished':
            print('download finished')

            get_just_filename = re.search(r"(.*\/)([^\/]*)\.[a-zA-Z0-9]*",
                                          d['filename'])
            # self.mediaobject.title = get_just_filename.group(2)
            self.mediaobject.audiofile.name = get_just_filename.group(
                1) + get_just_filename.group(2) + ".mp3"
            self.mediaobject.download_finished = True
            self.mediaobject.busy = False
            self.mediaobject.save()

    def run(self):
        youtube_target_url = "https://youtube.com/watch?v=" + self.mediaobject.id

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            jsontry = ydl.extract_info(youtube_target_url,
                                       download=False,
                                       ie_key=None,
                                       extra_info={},
                                       process=True,
                                       force_generic_extractor=False)
            
            self.mediaobject.title = jsontry["title"]
            self.mediaobject.description = jsontry["description"]
            self.mediaobject.download_finished = False
            self.mediaobject.busy = True
            self.mediaobject.save()
            ydl.download([youtube_target_url])
            
class MyLogger(object):

    def debug(self, msg):
        print("DEBUG")
        print(msg)
        pass

    def warning(self, msg):
        print("WARNING")
        print(msg)
        pass

    def error(self, msg):
        print("ERROR")
        print(msg)


# for reference
# {'status': 'downloading', 'downloaded_bytes': 17131, 'total_bytes': 17131, 'tmpfilename':
# '/code/dl/tPEE9ZwTmy0/Shortest Video on Youtube.m4a.part', 'filename':
# '/code/dl/tPEE9ZwTmy0/Shortest Video on Youtube.m4a', 'eta': 0, 'speed':
# 128899.3488425494, 'elapsed': 0.43769383430480957, '_eta_str': '00:00',
# '_percent_str': '100.0%', '_speed_str': '125.88KiB/s', '_total_bytes_str': '16.73KiB'}