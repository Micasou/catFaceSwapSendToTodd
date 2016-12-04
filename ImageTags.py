#run by using $python ImageTags.py <URL>
from clarifai.rest import ClarifaiApp
import sys
import json
import sys
from sh import curl  # install `sh` with `pip install sh`

def imgurHandle():
    try:
        resp = curl(
            "https://api.imgur.com/3/image",
            H="Authorization: Client-ID ca77119dcc8c6d8",  # Get your client ID from imgur.com
            X="POST",
            F='image=@%s' % sys.argv[1]
        )
        objresp = json.loads(resp.stdout)

        #if objresp.get('success', False):
            #print objresp['data']['link']
        #else:
            #print 'Error: ', objresp['data']['error']
        return objresp['data']['link']
    except Exception as e:
        print 'Error: ', e

def getWords(url):
    subDict = None
    words = []
    app = ClarifaiApp()
    imageURL = url
    d = app.tag_urls([imageURL])

    #output list, value
    count = 0

    for key, value in d.iteritems():
        if key == 'outputs':
            subDict = value
            break

    for i in subDict:
        for key, value in i.iteritems():
            if key == 'data':
                subDict = value
                break

    for key, value in subDict.iteritems():
        if key == 'concepts':
            subDict = value
            break

    for i in subDict:
        for key, value in i.iteritems():
            if key == 'name':
                words.append(value)
                if(len(words) % 4 == 0):
                    words.append('\n')
                break

    return(" ".join(words))

# url = sys.argv[1]
# firstFive = url[0:4]
#
# if(firstFive != "http"):
#     getWords(imgurHandle())
#     #getWords(sys.stdin.read())
# else:
#     getWords(sys.argv[1])
