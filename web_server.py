import os
import json
import random

from flask import Flask, send_from_directory
from flask_sock import Sock

app = Flask(__name__)
sock = Sock(app)

rooms = {}

CODE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
COLORS = ["red", "green", "yellow", "blue"]


def gen_code():
    while True:
        code = "".join(random.choice(CODE_CHARS) for _ in range(4))
        if code not in rooms:
            return code


def send(ws, data):
    ws.send(json.dumps(data))


def broadcast(room, data, except_ws=None):
    for client in rooms[room]["clients"]:
        if client != except_ws:
            send(client, data)


@app.route("/")
def home():
    return send_from_directory("public", "index.html")


@sock.route("/ludo")
def ludo(ws):

    room_code = None
    uid = None

    while True:
        try:
            data = json.loads(ws.receive())

            if data["type"] == "create":

                room_code = gen_code()
                uid = data["uid"]

                rooms[room_code] = {
                    "host": uid,
                    "players": [
                        {
                            "uid": uid,
                            "name": data.get("name", "Player"),
                            "color": "red"
                        }
                    ],
                    "clients": [ws]
                }

                send(ws, {
                    "type": "created",
                    "code": room_code
                })


            elif data["type"] == "join":

                room_code = data["code"]
                uid = data["uid"]

                if room_code not in rooms:
                    send(ws,{
                        "type":"error",
                        "message":"Room not found"
                    })
                    continue


                room = rooms[room_code]

                color = COLORS[len(room["players"])]

                room["players"].append({
                    "uid":uid,
                    "name":data.get("name","Player"),
                    "color":color
                })

                room["clients"].append(ws)


                send(ws,{
                    "type":"joined",
                    "players":room["players"]
                })


                broadcast(
                    room_code,
                    {
                        "type":"update",
                        "players":room["players"]
                    },
                    ws
                )


            elif data["type"] == "state":

                broadcast(
                    room_code,
                    {
                        "type":"state",
                        "data":data["data"]
                    },
                    ws
                )


        except Exception as e:
            print(e)
            break


PORT = int(os.environ.get("PORT",5000))

app.run(
    host="0.0.0.0",
    port=PORT
)