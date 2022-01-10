from flask import Flask, request, make_response
from flask_restful import Resource, Api, reqparse
from gevent.pywsgi import WSGIServer
import sqlite3
import miniaudio
import asyncio
import json

music_folder = "/e/Files/Music"

initialState = {
    "currentSong": "",
    "currentSample": 0,
    "currentSamples": [],
    "currentLength": 0,
    "currentSampleRate": 0,
}

# def newSong(songName):
#     song = music_folder + songName
#     raw_data = miniaudio.decode_file(song)
    # currentUsers[ip] = initialState
    # currentUsers[ip]["currentLength"] = len(raw_data.samples)
    # currentUsers[ip]["currentSamples"] = raw_data.samples
    # currentUsers[ip]["currentSampleRate"] = raw_data.sample_rate
    # currentUsers[ip]["currentSample"] = 0
    # currentUsers[ip]["currentSong"] = song
    

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
        return defaultGet('songs', ['song_id', 'song_name', 'artist_name', 'album_name', 'genre', 'date', 'song_file_name'])

    def post(self):
        songName = request.data.decode('UTF-8')
        song = music_folder + songName
        raw_data = miniaudio.decode_file(song)
        response = make_response(bytes(raw_data.samples))
        response.headers.set('Content-Type', 'application/octet-stream')
        return response


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

@app.route('/api/songs/<string:song>')
def song(song):
    newSong(song)

def startAPI():
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()