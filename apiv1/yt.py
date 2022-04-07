import youtube_dl

from .models import Video

class YT:
    def __init__(self, url):
        self.url = url

        self.ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'logger': MyLogger(),
                'progress_hooks': [self.my_hook],
                'download_archive': '/code/dl/archive',
                'keepvideo': True,
                'cachedir': '/code/dl/cache',
                'outtmpl': '/code/dl/%(title)s.%(ext)s',
            }

    def my_hook(self, d):
        if d['status'] == 'downloading':
            print('Downloadingg it ')
        if d['status'] == 'error':
            print('Error happened')
        if d['status'] == 'finished':
            print('download finished converting nopw')
    
    def run(self):

        # newvid = Video.objects.create(url=self.url)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    def error(self, msg):
        print(msg)