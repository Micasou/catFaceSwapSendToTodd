#! /usr/bin/env python

from sh import curl  # install `sh` with `pip install sh`
import json
import sys

def upload():
    try:
        resp = curl(
            "https://api.imgur.com/3/image",
            H="Authorization: Client-ID ca77119dcc8c6d8",  # Get your client ID from imgur.com
            X="POST",
            F='image=@%s' % sys.argv[1]
        )
        objresp = json.loads(resp.stdout)

        if objresp.get('success', False):
            return objresp['data']['link']
        else:
            return 'Error: ', objresp['data']['error']
    except Exception as e:
        print 'Error: ', e
