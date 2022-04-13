# chat/consumers.py
from cgitb import text
import json
from channels.generic.websocket import WebsocketConsumer
import re
from channels.db import database_sync_to_async
from .models import Video
from django_q.tasks import async_task, result, fetch
from .testclass import Testclass
from .youtube import YT

import time
# def finished_task(task):
#     print(task.result.status)
#     if task.result.status == 'converted':
#         task.result.ready = True
#         task.result.save()
#     else:
#         task.result.ready = False
#         task.result.save()

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        print("connected")

    def disconnect(self, message):
        print("disconnected")

    def receive(self, text_data):

        print("ayyyy")

        self.send(text_data=json.dumps({
            'status': "submitted"
            }))

        print(text_data)

        vid = Video.objects.create(url=self.url, urlid=self.urlid)

        # import time

        # time.sleep(5)

        # self.send(text_data=json.dumps({
        #     'status': "wowowo"
        #     }))
        
        # time.sleep(5)

        # self.send(text_data=json.dumps({
        #     'status': "test"
        #     }))
        
        # time.sleep(5)

        # self.send(text_data=json.dumps({
        #     'status': "anolther test"
        #     }))

    # async def validate_url(self, url):
    #     x = re.search("(https?://)?(www\.)?youtube\.(com|ca)/watch\?v=([-\w]+)", url)
    #     if x == None:
    #         print("validation failed")
    #         self.url = ''
    #         self.urlid = ''
    #         await self.send(text_data=json.dumps({
    #         'status': "rejected"
    #         }))
    #         return False
    #     else:
    #         print("validation passed")
    #         self.url = url
    #         self.urlid = x.group(4)
    #         # return x.group(4)
    #         return True

    # def get_vid(self):        
    #     try:
    #         print("database check")
    #         vid = Video.objects.get(urlid=self.urlid)
    #         print("vid exists")
    #         # add check to see if download was finished. if not then restart download
    #         return vid
    #     except:
    #         print("not found")
    #         vid = Video.objects.create(url=self.url, urlid=self.urlid)
    #         vid.save()
    #         async_task('apiv1.task.get_video', vid, sync=False, hook='apiv1.consumers.finished_task')
    #         # task = fetch(task_id)
    #         # # and can be examined
    #         # if not task.success:
    #         #     print('An error occurred: {}'.format(task.result))
    #         #     return False
    #         print("NEW vid created: " + vid.urlid)
    #         return vid



    # def polling(self):        
    #     try:
    #         vid = Video.objects.get(urlid=self.urlid)
    #         print("vid found")
    #         return vid
    #     except:
    #         print("not found")
    #         return False

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)

    #     if await self.validate_url(text_data_json['url']):
    #         print("validatedd")
    #     else:
    #         print("dsfgdsf")

    #     if text_data_json['request_type'] == "submit":
    #         print ("submission command")           
    #         vid = await database_sync_to_async(self.get_vid)() 
    #         # print("getvid")
    #         await self.send(text_data=json.dumps({
    #         'status': "submitted"
    #         }))

    #     elif text_data_json['request_type'] == "polling":
    #         print ("POLLING")     
    #         vid = await database_sync_to_async(self.get_vid)()     

    #         if vid:
    #             await self.send(text_data=json.dumps({
    #             'status': vid.status,
    #             'downloaded_bytes': vid.downloaded_bytes,
    #             'total_bytes' : vid.total_bytes
    #             }))
    #         else:
    #             await self.send(text_data=json.dumps({
    #             'status': "error",
    #             'downloaded_bytes': '0',
    #             'total_bytes' : '0'
    #             }))

    #     else:
    #         print ("ERROR")

    #         # await self.send(text_data=json.dumps({
    #         #     'status': vid.status,
    #         #     'downloaded_bytes': vid.downloaded_bytes,
    #         #     'total_bytes' : vid.total_bytes
    #         # }))

    # async def disconnect(self, message):
    #     pass


