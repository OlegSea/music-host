import sqlite3
import json
from sys import argv
import fs
from api import startAPI
import asyncio
import websockets
from websockets.exceptions import ConnectionClosedError, ConnectionClosed
import re
import miniupnpc
import miniaudio
from multiprocessing import Process

music_folder = argv[1]


async def handler(websocket):
    try:
        async for message in websocket:
            if re.search('^play (.*)$', message):
                song = music_folder + re.findall('^play (.*)$', message)[0]

                raw_data = miniaudio.decode_file(song)
                for i in range(0, len(raw_data.samples), raw_data.sample_rate):
                        await websocket.send(bytes(raw_data.samples[i:i+raw_data.sample_rate]))
            elif re.search('^seek (\d*) (.*)$', message):
                results = re.findall('^seek (\d*) (.*)$', message)
                seconds = results[0][0]
                song = music_folder + results[0][1]

                raw_data = miniaudio.decode_file(song)
                for i in range(int(seconds) * raw_data.sample_rate * raw_data.nchannels, len(raw_data.samples), raw_data.sample_rate):
                    try:
                        await websocket.send(bytes(raw_data.samples[i:i+raw_data.sample_rate]))
                    except ConnectionClosedError:
                        break
    except ConnectionClosedError:
        pass
    except ConnectionClosed:
        pass


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future() 


if __name__ == "__main__":
    con = sqlite3.connect("data/music.db")
    cur = con.cursor()

    upnp = miniupnpc.UPnP()

    upnp.discoverdelay = 10
    upnp.discover()

    upnp.selectigd()

    upnp.addportmapping(8001, 'TCP', upnp.lanaddr, 8001, 'WS', '')
    upnp.addportmapping(8001, 'UDP', upnp.lanaddr, 8001, 'WS', '')
    upnp.addportmapping(5000, 'TCP', upnp.lanaddr, 5000, 'API', '')
    upnp.addportmapping(3000, 'TCP', upnp.lanaddr, 3000, 'Website', '')

    fs.scanDir(con, cur, music_folder)

    api = Process(target=startAPI)
    api.start()
    asyncio.run(main())

