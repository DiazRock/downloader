import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
from pathlib import Path


PROVEYOURWORTH_URL= 'https://www.proveyourworth.net/level3/'
CAR_PICTURE_PATH = 'car.jpg'
SIGNED_CAR_PATH = 'signed.jpg'
RESUME_PATH = 'resume.pdf'
CODE_PATH = 'downloader.py'
FILE_PATH = Path('./')

def bobby_request(url):
    with session.get(url) as resp_get:
        soup = BeautifulSoup(repr(resp_get.content), "html5lib")
        submit_data = {
            n['name']: n['value'] for n in soup.findAll('input') if n.get('value', False)
        }
        submit_data['username'] = "Robert'); DROP TABLE Students;--"
        form_method = soup.find('form')['action']
        return submit_data, form_method

def angels_request(url, data):
    with session.post(url + '?' + '&'.join( '{0}={1}'.format(key,value) for (key,value) in data.items() )) as resp_post:
        return resp_post.headers['X-Payload-URL']

def car_request(payload_url, data):
    with session.get(payload_url, data= data) as resp_get:
        return resp_get.headers['X-Post-Back-To'], resp_get.content

def sign_payload(my_name, statefulhash, image):
    stream = BytesIO(image)
    image = Image.open(stream)
    draw = ImageDraw.Draw(image)
    (x, y) = (25, 25)
    color = 'rgb(49,90,200)'
    message = '{0}\n{1}'.format(my_name, statefulhash)
    draw.text((x, y), message, fill=color)
    image.save(FILE_PATH / SIGNED_CAR_PATH, "JPEG")


def final_upload(upload_url):
    with open(FILE_PATH / SIGNED_CAR_PATH, 'rb') as cf,\
         open(FILE_PATH / RESUME_PATH, 'rb') as rf,\
         open(FILE_PATH / CODE_PATH, 'rb') as cdf:
            files = {
                'image': cf,
                'resume': rf,
                'code':  cdf,
            }
            data = {
                'name': 'Alejandro Díaz Roque',
                'email': 'corolariodiaz@gmail.com',
                'aboutme': "I'm a software engineer, with knowledge of Computer Science and Math. I made projects in which I applied ideas of Language Theory, like a Compiler and a Context Free Grammar Annalyzer. I got knowledge of backend web technologies like docker, python and zmq. And I also have experience working with frontend web technologies as vue js, vuex, nuxt and react"    
            }
            with session.post(upload_url, files = files, data= data) as resp_post,\
                 open('final_content.html', 'w') as final_content:
                print(resp_post.text)
                final_content.write(resp_post.text)
                

def main():
    submit_data, form_method= bobby_request(url = PROVEYOURWORTH_URL)
    payload_url= angels_request(url= PROVEYOURWORTH_URL + '/' + form_method,
                                                data = submit_data)
    upload_url, image= car_request(payload_url= payload_url,
                data= submit_data)
    sign_payload(my_name= 'Alejandro Díaz Roque',
                 statefulhash= submit_data['statefulhash'],
                 image = image) 
    final_upload(upload_url)

if __name__ == '__main__':
    session =  requests.Session()
    main()