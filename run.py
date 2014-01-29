import os, flask
import json, xmltodict, urllib2
from HTMLParser import HTMLParser as h
import utils, time
from random import randint as gen
import settings

app = flask.Flask(__name__)
app.secret_key = str(gen(0,1000000000000))

params = settings.params

methods = {
    #'getLatestChatsWithLimit': [10],
    #'getMotd': [], # MOTD
    'getPlugins': [],
    'getPlayerNames': [], # Player list
    'getOfflinePlayerNames': [], # Offline users
    'getPlayerCount': [], # Online player count
    'getPlayerLimit': [], # Max players
    'getServerVersion': [], # Get MC version (has the spigot tag on it)
    'system.getDiskFreeSpace': [], # Amount of free HDD
    'system.getDiskSize': [], # Total HDD space
    'system.getJavaMemoryTotal': [], # RAM Allocated
    'system.getJavaMemoryUsage': [] # RAM used
}

@app.route('/')
@app.route('/<page>')
def index_handler(page="index"):
    page = page.lower()
    data = utils.jsonapi(params, methods)
    #try:
    # Get HDD data for chart
    data['hdduse'] = utils.percentage(data['system.getDiskFreeSpace'], data['system.getDiskSize'])
    data['hddfree'] = 100-data['hdduse']
    # Get RAM data for chart
    data['usedram'] = utils.percentage(data['system.getJavaMemoryUsage'], data['system.getJavaMemoryTotal'])
    data['unusedram'] = 100-data['usedram']
    # Get RAM data for chart
    data['online'] = utils.percentage(data['getPlayerCount'], data['getPlayerLimit'])
    data['offline'] = 100-data['online']

    # Try to load skins.db
    if not os.path.isfile('skins.db'):
        # Never made the DB before...
        skindb = {}
    else:
        with open('skins.db','r') as f:
            skindb = json.loads(f.read())
    full_players = list(set(data['getPlayerNames'] + data['getOfflinePlayerNames']))
    for player in data['getPlayerNames']:
        if player not in skindb:
            # Never generated before...
            utils.gen_skin(player,16)
            skindb[player] = time.time()
            print 'Generating skin for %s' % player
        else:
            # Assume their name is in the DB.. check times!
            diff = int(time.time()) - int(skindb[player])
            if diff > 43200:
                utils.gen_skin(player,16)
                skindb[player] = time.time()
    with open('skins.db', 'w') as f:
        f.write(json.dumps(skindb,indent=4))
    # Here, we pull news posts from the forums. This is derp but it'll work...
    posts, uri = [], 'http://forum.wonderfulplanet.net/index.php?forums/news/index.rss'
    forum = xmltodict.parse(urllib2.urlopen(uri).read())['rss']['channel']
    for item in forum['item']:
        content = h().unescape(item['content:encoded'])
        if '...<br />' in content:
            content = content.split('...<br />',1)[0]
            content += ' [<a href="%s">Read more</a>]' % h().unescape(item['link'])
        posts.append({
                      'title': h().unescape(item['title']),
                      'author': h().unescape(item['author']),
                      'date': h().unescape(item['pubDate']),
                      'link': h().unescape(item['link']),
                      'content': content
                 })
    #except:
    #    return flask.abort(404)

    page += '.html'
    if os.path.isfile('templates/' + page):
        return flask.render_template(page, data=data, posts=posts)
    return flask.abort(404)


@app.route('/classic')
def classic():
    try:
        server = urllib2.urlopen('http://server2.liamstanley.net/play.txt').read()
    except:
        flask.abort(404)
    return flask.render_template('classic.html', server=server)


@app.route('/api')
def api_handler():
    data = {
        'method': flask.request.method,
        'path': flask.request.path,
        'ip': flask.request.remote_addr,
        'api-base': dir(flask.request),
        'args': flask.request.args,
        'view-args': flask.request.view_args,
        'server': utils.jsonapi(params, methods)
    }
    return flask.jsonify(data), 200

@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template('404.html'), 404


@app.after_request
def add_header(response):
    """
        Add headers to both force latest IE rendering engine or Chrome Frame,
        and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=60'
    return response

# Debug should normally be false, so we don't display hazardous information!
app.debug = True
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5007)
