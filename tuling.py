import requests
import json

postdata = {
    "key": "4085eeed768a4ec1848398e339f8f8bb",
    "info": "你在哪里",
    "loc":"广东省深圳市",
    "userid":"123456"
}

def tuling(text):
    postdata['info'] = text
    r = requests.post("http://www.tuling123.com/openapi/api",data=postdata)
    res = json.loads(r.text)['text']
    return res

#print(tuling('说什么'))
