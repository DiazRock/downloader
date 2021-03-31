import json
import requests
import os
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

PROVEYOURWORTH_URL= 'http://www.proveyourworth.net/level3/'
CAR_PICTURE_PATH = 'car.jpg'
SIGNED_CAR_PATH = 'signed.jpg'
RESUME_PATH = 'resume.pdf'
CODE_PATH = 'downloader.py'

def bobby_request(url):
    with requests.get(url) as resp_get:
        soup = BeautifulSoup(repr(resp_get.content), "html5lib")
        submit_data = {
            n['name']: n['value'] for n in soup.findAll('input') if n.get('value', False)
        }
        submit_data['username'] = "Robert'); DROP TABLE Students;--"
        form_method = soup.find('form')['action']
        return {'PHPSESSID': resp_get.cookies.get('PHPSESSID')}, submit_data, form_method

def angels_request(url, data, cookies):
    with requests.get(url, 
        data= data, 
        cookies= cookies) as resp_post:
        return resp_post.headers['X-Payload-URL']

def car_request(payload_url, data, cookies):
    with requests.get(payload_url, data= data, cookies = cookies) as resp_get:
        return resp_get.headers['X-Post-Back-To'], {'PHPSESSID': resp_get.cookies.get('PHPSESSID')}, resp_get.content

def sign_payload(my_name, statefulhash, image):
    stream = BytesIO(image)
    image = Image.open(stream)
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype('Roboto-Bold.ttf', size=30)
    (x, y) = (25, 25)
    color = 'rgb(49,90,200)'
    message = '{0}\n{1}'.format(my_name, statefulhash)
    draw.text((x, y), message, fill=color, font=font)
    image.save(SIGNED_CAR_PATH, "JPEG")


def final_upload(upload_url, cookies):
    with open(SIGNED_CAR_PATH, 'rb') as cf,\
         open(RESUME_PATH, 'rb') as rf,\
         open(CODE_PATH, 'rb') as cdf:
            data = {
                "name": 'Alejandro',
                "email": 'corolariodiaz@gmail.com',
                "aboutme": "I'm a software engineer, with knowledge of Computer Science and Math. I made projects in which I applied ideas of Language Theory, like a Compiler and a Context Free Grammar Annalyzer. I got knowledge of backend web technologies like docker, python and zmq. And I also have experience working with frontend web technologies as vue js, vuex, nuxt and react"
            }
            files = {
                'image': ( os.path.basename(SIGNED_CAR_PATH), cf, 'image/jpg'),
                'resume': (os.path.basename(RESUME_PATH), rf, 'application/octet-stream'),
                'code': (os.path.basename(CODE_PATH), cdf, 'application/octet-stream'),
                }
            
            with requests.post(upload_url, files= files, data= data, cookies= cookies) as resp_post,\
                 open('final_content.html', 'wb') as final_content:
                print(resp_post.text)
                print(resp_post.request.url)
                print(resp_post.request.values)
                print(resp_post.json())
                final_content.write(resp_post.content)
                

def main():
    cookies, submit_data, form_method = bobby_request(url = PROVEYOURWORTH_URL)
    payload_url= angels_request(url= PROVEYOURWORTH_URL + '/' + form_method,
                                                data = submit_data,
                                                cookies= cookies)
    upload_url, new_cookies, image= car_request(payload_url= payload_url,
                data= submit_data,
                cookies= cookies)
    sign_payload(my_name= 'Alejandro Díaz Roque',
                 statefulhash= submit_data['statefulhash'],
                 image = image) 
    final_upload(upload_url,
                 cookies= new_cookies)
if __name__ == '__main__':
    main()