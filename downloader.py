import os
import requests
from bs4 import BeautifulSoup
from bottle import route, run, template

PROVEYOURWORTH_URL= 'https://www.proveyourworth.net/level3/'
CAR_PICTURE_PATH= 'car.jpg'
RESUME_PATH= 'resume.pdf'
CODE_PATH= 'downloader.py'
TEMPLATE = ''

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
        cookies= cookies) as resp_post,\
        open('angels_content.html', 'wb') as ac,\
        open('angels_headers.json', 'w') as ah:
        ac.write(resp_post.content)
        ah.write(repr(resp_post.headers))
        return resp_post.headers['X-Payload-URL']

def car_request(payload_url, data, cookies):
    with requests.get(payload_url, data= data, cookies = cookies) as resp_get,\
         open(CAR_PICTURE_PATH, 'wb') as car_picture,\
         open('car_headers.json', 'w') as ch:
        car_picture.write(resp_get.content)
        ch.write(repr(resp_get.headers))
        return resp_get.headers['X-Post-Back-To'], {'PHPSESSID': resp_get.cookies.get('PHPSESSID')}
        

def final_upload(upload_url, statefulhash, cookies):
    global TEMPLATE
    with open(CAR_PICTURE_PATH, 'rb') as cf,\
         open(RESUME_PATH, 'rb') as rf,\
         open(CODE_PATH, 'rb') as cdf:
            files = {
                'image': ('bmw_for_life.jpg', cf, 'multipart/form-data'),
                'code': ('downloader.py', cdf, 'multipart/form-data'),
                'resume': ('resume.pdf', rf, 'multipart/form-data'),
            }
            data = {
                
                'statefulhash': statefulhash,
                'name': 'Alejandro Diaz Roque',
                'email': 'corolariodiaz@gmail.com',
                'aboutme': "I'm a software engineer, with knowledge of Computer Science and Math. I made projects in I applied ideas of Language Theory, like a Compiler and a Context Free Grammar Annalyzer. I got knowledge of backend web technologies like docker, python and zmq. And I also have experience working with frontend web technologies as vue js, vuex, nuxt and react",
                
            }
            
            with requests.post(upload_url,
                               data= data,
                               files = files,
                               cookies= cookies) as resp_post:
                
                TEMPLATE= template(repr(resp_post.content) + '\n' + repr(resp_post.headers) + '\n' + repr (resp_post.cookies))

@route('/')
def index():
    return TEMPLATE

def main():
    cookies, submit_data, form_method = bobby_request(url = PROVEYOURWORTH_URL)
    payload_url= angels_request(url= PROVEYOURWORTH_URL + '/' + form_method,
                                                data = submit_data,
                                                cookies= cookies)
    
    upload_url, new_cookies= car_request(payload_url= payload_url,
                data= submit_data,
                cookies= cookies)
    final_upload(upload_url, 
                 statefulhash= submit_data['statefulhash'],
                 cookies= new_cookies)
    run(host='https://application-work.herokuapp.com', port=9000)
    
if __name__ == '__main__':
    main()
