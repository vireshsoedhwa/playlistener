import youtube_dl 
from .models import Video
from django.core.files.base import ContentFile
from django.core.files import File

class YT:
    def __init__(self, url, vidobject):
        self.url = url
        self.vidobject = vidobject

        self.ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [self.my_hook],
                # 'download_archive': '/code/dl/archive',
                # 'keepvideo': True,
                # 'cachedir': '/code/dl/cache',
                'outtmpl': '/code/dl/%(id)s/%(title)s.%(ext)s',
            }

    def my_hook(self, d):
        self.vidobject.status = d['status']
        if d['status'] == 'downloading':
            print('Downloadingg it ' + str(d['downloaded_bytes']) + "/" + str(d['total_bytes']))
            self.vidobject.downloaded_bytes = d['downloaded_bytes']
            self.vidobject.total_bytes = d['total_bytes']            
        if d['status'] == 'error':
            print('Error happened')
        if d['status'] == 'finished':
            print('download finished')        
        self.vidobject.save()
    
    def run(self):
        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])

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