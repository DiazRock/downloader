import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw, ImageFont

PROVEYOURWORTH_URL= 'https://www.proveyourworth.net/level3/'
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
    with requests.post(url, 
        data= data, 
        cookies= cookies) as resp_post:
        return resp_post.headers['X-Payload-URL']

def car_request(payload_url, data, cookies):
    with requests.get(payload_url, data= data, cookies = cookies) as resp_get,\
         open(CAR_PICTURE_PATH, 'wb') as car_picture:
        car_picture.write(resp_get.content)
        return resp_get.headers['X-Post-Back-To'], {'PHPSESSID': resp_get.cookies.get('PHPSESSID')}

def sign_payload(my_name, statefulhash):
    with Image.open(CAR_PICTURE_PATH) as car_picture:
        draw = ImageDraw.Draw(car_picture)
        font = ImageFont.truetype('Roboto-Bold.ttf', size=30)
        (x, y) = (25, 25)
        color = 'rgb(49,90,200)'
        message = '{0}\n{1}'.format(my_name, statefulhash)
        draw.text((x, y), message, fill=color, font=font)
        car_picture.save(SIGNED_CAR_PATH)

def final_upload(upload_url, cookies):
    with Image.open(SIGNED_CAR_PATH) as cf,\
         open(RESUME_PATH, 'rb') as rf,\
         open(CODE_PATH, 'rb') as cdf:
            data = {
                'image': cf.tobytes(),
                'resume': rf.read(),
                'code':  cdf.read(),
                'name': 'Alejandro Díaz Roque',
                'email': 'corolariodiaz@gmail.com',
                'aboutme': "I'm a software engineer, with knowledge of Computer Science and Math. I made projects in which I applied ideas of Language Theory, like a Compiler and a Context Free Grammar Annalyzer. I got knowledge of backend web technologies like docker, python and zmq. And I also have experience working with frontend web technologies as vue js, vuex, nuxt and react"    
            }
            with requests.post(upload_url, data= data, cookies= cookies) as resp_post,\
                 open('final_content.html', 'wb') as final_content:
                print(resp_post.content)
                final_content.write(resp_post.content)
                

def main():
    cookies, submit_data, form_method = bobby_request(url = PROVEYOURWORTH_URL)
    payload_url= angels_request(url= PROVEYOURWORTH_URL + '/' + form_method,
                                                data = submit_data,
                                                cookies= cookies)
    upload_url, new_cookies= car_request(payload_url= payload_url,
                data= submit_data,
                cookies= cookies)
    sign_payload(my_name= 'Alejandro Díaz Roque', 
                 statefulhash= submit_data['statefulhash']) 
    final_upload(upload_url,
                 cookies= new_cookies)
if __name__ == '__main__':
    main()