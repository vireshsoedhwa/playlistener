class Testclass:
    def __init__(self, url, callback):
        self.url = url
        self.callback = callback

    def run(self):

        # newvid = Video.objects.create(url=self.url)
        self.callback("hello")
