import requests,re
from bs4 import BeautifulSoup
from requests.structures import CaseInsensitiveDict
import json

header = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'

def url_extracter1(url):
	api_url = "https://httpstatus-backend-production.herokuapp.com/api"
	headers = CaseInsensitiveDict()
	headers["Content-Type"] = "application/json"
	headers['User-agent'] = header
	data ={
	    "additionalSubdomains": [
	        "www"
	    ],
	    "canonicalDomain": False,
	    "escapeCharacters": False,
	    "followRedirect": True,
	    "headerName": "",
	    "headerValue": "",
	    "passWord": "",
	    "strictSSL": True,
	    "throttleRequests": 100,
	    "urls": [
	        url
	    ],
	    "userAgent": "browser",
	    "userName": ""
	}

	data = json.dumps(data)
	try:
		resp = requests.post(api_url, headers=headers, data=data)
		if resp.ok:
			json_data = resp.json()
			data = json_data[0]['redirectURLChain'][-1]
			return data
		else:
			return None
	except:
		return None

def url_extracter2(url):

	post_url = 'https://wheregoes.com/trace/'


	data = {
		"url": url,
		"ua": "Wheregoes.com+Redirect+Checker/1.0"
	}

	headers= {'User-agent': header}

	try:

		resp = requests.post(url=post_url, data=data, headers=headers)

		if resp.ok:

			soup = BeautifulSoup(resp.text, 'html.parser')

			div = soup.findAll('div', attrs = {'class':'cell url'})[-1]
			return div.find('a').string
		else:
			return None
	except:
		return None



def find_details(url):
	headers= {'User-agent': header}
	try:
		resp = requests.head(url, allow_redirects=True, headers=headers)
		if resp.ok:
			if 'html' not in resp.headers['Content-Type']:
				check1 = resp.headers.get('Content-Disposition')
				if check1:
					filename = re.findall('filename=(.+)',check1)
					if len(filename) == 0:
						return None
					return filename[0].replace('"',''),resp.url,resp.headers['Content-Length'],resp.headers['Content-Type']
				else:
					filename = url.split('/')[-1]
					filename = filename.split('#')[0]
					filename = filename.split('?')[0]
					filename = filename.split('&')[0]
					return filename,resp.url,resp.headers['Content-Length'],resp.headers['Content-Type']
			return None
		return None
	except:
		return None

def file_details(url):
	headers= {'User-agent': header}
	try:
		details = find_details(url)
		if details:
			return details
	except:
		return None
	check = url_extracter1(url)
	if check:
		details = find_details(url)
		if details:
			return details
		else:
			check = url_extracter2(url)
			if check:
				details = find_details(url)
				if details:
					return details
				else:
					return None
			else:
				return None
	else:
		check = url_extracter2(url)
		if check:
			details = find_details(url)
			if details:
				return details
			else:
				return None
		else:
			return None


def file_type(content_type):
    if 'image' in content_type:
        return 'image'
    elif 'video' in content_type:
        return 'video'
    elif 'audio' in content_type:
        return 'audio'
    elif 'pdf' in content_type:
        return 'pdf'
    elif 'zip' in content_type:
        return 'zip'
    else:
        return 'file'
