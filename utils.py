#!/usr/bin/python

import json
from hashlib import sha256
from urllib2 import urlopen
from urllib import quote
import skin

# https://github.com/alecgorge/jsonapi/wiki/Analyzing-the-jsonapi-request-and-response-format
# http://alecgorge.github.io/jsonapi/

def jsonapi(params, methodData):
    key = sha256(params['username'] + json.dumps(methodData.keys()) + params['password'] + params['salt']).hexdigest()
    methods, args = [], []

    for methodName, methodArgs in methodData.iteritems():
        methods.append(methodName)
        args.append(methodArgs)

    uri = 'http://{host}:{port}/api/call-multiple?method={methods}&args={args}&key={key}'.format(
           host=params['host'],
           port=str(params['port']),
           methods=quote(json.dumps(methods)),
           args=quote(json.dumps(args)),
           key=key
    )

    try:
        data = json.loads(urlopen(uri).read())
        returnData = {}
        if data['result'] != 'success':
            return False
        for response in data['success']:
            returnData[response['source']] = response['success']
    except:
        return False
    return returnData

def percentage(part, whole):
    try:
        return 100 * float(part)/float(whole)
    except:
        return 0


def gen_skin(player, dim=16):
    skin.dim = dim
    try:
        skin.generateAvatar(skin.loadSkinFromURL('https://s3.amazonaws.com/MinecraftSkins/%s.png' % player)).save('static/skins/%s.png' % player,'PNG')
    except:
        skin.generateAvatar(skin.loadSkinFromURL('https://minecraft.net/images/char.png')).save('static/skins/%s.png' % player,'PNG')