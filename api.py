from flask import Flask
from flask_restful import Resource, Api, reqparse
from gevent.pywsgi import WSGIServer
import sqlite3
import asyncio


def defaultGet(db, cargs):
    con = sqlite3.connect('data/music.db')
    cur = con.cursor()

    parser = reqparse.RequestParser()
    for i in cargs:
        parser.add_argument(i)
    args = parser.parse_args()
    existing_args = {}
    for key, value in args.items():
        if value and value.strip():
            existing_args[key] = value

    rq = f'SELECT * from {db}'

    if existing_args != {}:
        rq += ' where'
        count = 1
        for key, value in existing_args.items():
            rq += f" {key} = '{value}'"
            if len(existing_args) > 1 and count < len(existing_args):
                rq += ' and'
            count += 1

    rq_result = cur.execute(rq).fetchall()
    con.close()

    result = []
    for i in rq_result:
        data = {}
        for j in range(len(cargs)):
            data[cargs[j]] = i[j]
        result.append(data)

    return result


class Songs(Resource):
    def get(self):
        return defaultGet('songs', ['song_id', 'song_name', 'artist_name', 'album_name', 'genre', 'date', 'song_file_name', 'sample_rate', 'length'])


class Artists(Resource):
    def get(self):
        return defaultGet('artists', ['artist_id', 'artist_name'])


class Albums(Resource):
    def get(self):
        return defaultGet('albums', ['album_id', 'album_name', 'artist_name']) 


app = Flask(__name__)
api = Api(app)

api.add_resource(Songs, '/api/songs')
api.add_resource(Artists, '/api/artists')
api.add_resource(Albums, '/api/albums')

def startAPI():
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()