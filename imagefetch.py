from urllib.parse import urlencode
from urllib.request import Request, urlopen
import base64


#base_url = 'http://localhost:5001/colours-of-wine/us-central1'
base_url = 'https://us-central1-colours-of-wine.cloudfunctions.net'
url = base_url + '/expertGenerateImage?cookie='
post_fields = {'foo': 'bar'}

def generate_wine_external_api(desc, cookie):
    request = Request(url + cookie, desc.encode('utf-8'))
    with urlopen(request) as response:
        return base64.b64decode(response.read())
