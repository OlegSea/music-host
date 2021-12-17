import sqlite3
import miniaudio
import fs
from api import startAPI
import asyncio
import websockets
import re
from multiprocessing import Process

music_folder = '/home/olegsea/Music'

should_break = False

async def handler(websocket):
    async for message in websocket:
        global should_break
        if re.search('^play (.*)$', message):
            should_break = True
            song = music_folder + re.findall('^play (.*)$', message)[0]

            raw_data = miniaudio.decode_file(song)
            for i in range(0, len(raw_data.samples), raw_data.sample_rate):
                if i == 0:
                    should_break = False
                if should_break:
                    break
                await websocket.send(bytes(raw_data.samples[i:i+raw_data.sample_rate]))


async def main():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future() 


if __name__ == "__main__":
    con = sqlite3.connect('data/music.db')
    cur = con.cursor()

    fs.scanDir(con, cur, music_folder)

    api = Process(target=startAPI)
    api.start()
    asyncio.run(main())

    