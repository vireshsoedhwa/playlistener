import youtube_dl

from .models import Video


class YT:

    def __init__(self, url, progresshook):
        self.url = url

        self.ydl_opts = {
            'format':
            'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'logger':
            MyLogger(),
            'progress_hooks': [progresshook],
            'download_archive': '/code/dl/archive',
            'keepvideo': False,
            # 'skip_download': True,
            'cachedir': '/code/dl/cache',
            'outtmpl': '/code/dl/' + url + '/' + '%(title)s.%(ext)s',
        }

    # def my_hook(self, d):
    #     if d['status'] == 'downloading':
    #         print('Downloadingg it ')
    #     if d['status'] == 'error':
    #         print('Error happened')
    #     if d['status'] == 'finished':
    #         print('download finished converting nopw')

    def run(self):

        # newvid = Video.objects.create(url=self.url)

        with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
            ydl.download([self.url])


class MyLogger(object):

    def debug(self, msg):
        print("test1")
        print(msg)
        pass

    def warning(self, msg):
        print("test2")
        print(msg)
        pass

    def error(self, msg):
        print("test3")
        print(msg)