from clarifai.rest import ClarifaiApp
import sys

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

    print(" ".join(words))

getWords(sys.argv[1])
