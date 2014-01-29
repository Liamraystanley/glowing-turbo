#!/usr/bin/python

import json
from hashlib import sha256
from urllib2 import urlopen
from urllib import quote
import skin

# https://github.com/alecgorge/jsonapi/wiki/Analyzing-the-jsonapi-request-and-response-format
# http://alecgorge.github.io/jsonapi/

def jsonapi(params, methodData):
    """Pull data from Bukkit/Spigot Plugin, JSONAPI, to be further used later on"""
    if len(methodData) == 1:
        method_format = methodData.keys()[0]
    else:
        method_format = json.dumps(methodData.keys())
    
    key = sha256(params['username'] + method_format + params['password'] + params['salt']).hexdigest()
    
    methods, args = [], []

    for methodName, methodArgs in methodData.iteritems():
        methods.append(methodName)
        args.append(methodArgs)

    if len(methods) == 1:
        methods = methods[0]
        uri = 'http://{host}:{port}/api/call?method={methods}&args={args}&key={key}'
    else:
        methods = quote(json.dumps(methods))
        uri = 'http://{host}:{port}/api/call-multiple?method={methods}&args={args}&key={key}'

    uri = uri.format(
        host=params['host'],
        port=str(params['port']),
        methods=methods,
        args=quote(json.dumps(args)),
        key=key
    )

    try:
        data = json.loads(urlopen(uri).read())
        print data
        returnData = {}
        if data['result'] != 'success':
            return False
        if data['success'] == None:
            return True
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