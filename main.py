import sqlite3
import json
import fs
from api import startAPI
import asyncio
import tornado.httpserver
import tornado.websocket
import tornado.ioloop
import tornado.web
from datetime import timedelta
from multiprocessing import Process, Manager


music_folder = "/e/Files/Music"

# initialState = {
#     "currentSong": "",
#     "currentSample": 0,
#     "currentSamples": [],
#     "currentLength": 0,
#     "currentSampleRate": 0,
# }

# clients = []


# class WebSocketHandler(tornado.websocket.WebSocketHandler):
#     def check_origin(self, origin):
#         print("origin: " + origin)
#         return True

#     # the client connected
#     def open(self):
#         print("New client connected")
#         clients.append(self)
#         currentUsers[self.request.remote_ip] = initialState
#     # the client sent the message
#     def on_message(self, message):
#         print("message: " + message)
#         self.write_message(message)

#     # client disconnected
#     def on_close(self):
#         print("Client disconnected")
#         clients.remove(self)


# def send_message_to_clients():
#     with open(temp_file, 'r') as f:
#         currentUsers = json.load(f)
#     try:
#         for client in clients:
#             data = currentUsers[client.request.remote_ip]
#             print(currentUsers)
#             if data["currentSample"] < data["currentLength"]:
#                 client.write_message(
#                     bytes(
#                         data["currentSamples"][
#                             data["currentSample"] : data["currentSample"]
#                             + data["currentSampleRate"]
#                         ]
#                     )
#                 )
#                 data["currentSample"] += data["currentSampleRate"]
#                 with open(temp_file, 'w') as f:
#                     json.dump(currentUsers, f)
#     finally:
#         tornado.ioloop.IOLoop.instance().add_timeout(
#             timedelta(milliseconds=50), send_message_to_clients
#         )


# socket = tornado.web.Application(
#     [
#         (r"/wss", WebSocketHandler),
#     ]
# )


if __name__ == "__main__":
    con = sqlite3.connect("data/music.db")
    cur = con.cursor()

    fs.scanDir(con, cur, music_folder)

    api = Process(target=startAPI)
    api.start()
    while True:
        pass
    # socket.listen(8001)
    # tornado.ioloop.IOLoop.instance().add_timeout(
    #     timedelta(milliseconds=50), send_message_to_clients
    # )
    # tornado.ioloop.IOLoop.instance().start()
