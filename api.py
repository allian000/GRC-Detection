import requests
from datetime import datetime
import json

web_api_url = "http://127.0.0.1:8000/"


class readCommand:
    def readMsg(command,image_name):
        if command == 'command 0':
            pass
        elif command == 'command 1':
            pass
        elif command == 'command 2':
            pass
        elif command == 'command 3':
            pass
        elif command == 'command 4':
            callAPI.crtaetRecord(4,image_name)
        elif command == 'command 5':
            pass
        else:
            pass

class callAPI:
    def crtaetRecord(command:int,image_url:str):
        now = datetime.now()
        d = now.strftime("%d/%m/%Y")
        t = now.strftime("%H:%M:%S")
        url = web_api_url + "images/" + image_url #http://127.0.0.1:8000/images/frame0
        response = requests.post(web_api_url+"createRecord/", json = {
            "command":command,
            "date":d,
            "time":t,
            "image_url": url,
            "state":"unwatch",
            })
        print(response,"command: ",command," url: ",image_url)