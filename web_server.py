
import os
import json
import random

from flask import Flask, send_from_directory
from flask_sock import Sock

app = Flask(
    __name__,
    static_folder="public",
    static_url_path=""
)

sock = Sock(app)

rooms = {}

CODE_CHARS = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
COLORS = [
    "red",
    "green",
    "yellow",
    "blue"
]


def generate_code():
    while True:
        code = "".join(
            random.choice(CODE_CHARS)
            for _ in range(4)
        )

        if code not in rooms:
            return code


def send(ws, data):
    try:
        ws.send(json.dumps(data))
    except:
        pass


def broadcast(room_code, data, except_ws=None):

    if room_code not in rooms:
        return

    room = rooms[room_code]

    dead = []

    for client in room["clients"]:

        if client == except_ws:
            continue

        try:
            client.send(json.dumps(data))
        except:
            dead.append(client)

    for client in dead:
        if client in room["clients"]:
            room["clients"].remove(client)


@app.route("/")
def index():
    return send_from_directory(
        "public",
        "index.html"
    )


@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(
        "public",
        path
    )


@sock.route("/ludo")
def websocket(ws):

    room_code = None
    uid = None

    while True:

        try:

            raw = ws.receive()

            if raw is None:
                break

            data = json.loads(raw)

            msg = data.get("type")

            # -------------------
            # CREATE ROOM
            # -------------------

            if msg == "create":

                room_code = generate_code()

                uid = data["uid"]

                rooms[room_code] = {

                    "host": uid,

                    "players": [
                        {
                            "uid": uid,
                            "name": data.get(
                                "name",
                                "Player"
                            ),
                            "color": "red"
                        }
                    ],

                    "clients": [ws],

                    "game": None

                }

                send(
                    ws,
                    {
                        "type": "created",
                        "code": room_code
                    }
                )
            # -------------------
            # JOIN ROOM
            # -------------------

            elif msg == "join":

                room_code = data["code"].upper()
                uid = data["uid"]

                if room_code not in rooms:

                    send(
                        ws,
                        {
                            "type": "error",
                            "message": "Room not found"
                        }
                    )

                    continue

                room = rooms[room_code]

                if len(room["players"]) >= 4:

                    send(
                        ws,
                        {
                            "type": "error",
                            "message": "Room is full"
                        }
                    )

                    continue

                color = COLORS[len(room["players"])]

                room["players"].append(
                    {
                        "uid": uid,
                        "name": data.get(
                            "name",
                            "Player"
                        ),
                        "color": color
                    }
                )

                room["clients"].append(ws)

                send(
                    ws,
                    {
                        "type": "joined",
                        "code": room_code,
                        "host": room["host"],
                        "yourColor": color,
                        "players": room["players"]
                    }
                )

                broadcast(
                    room_code,
                    {
                        "type": "lobby-update",
                        "host": room["host"],
                        "players": room["players"]
                    },
                    except_ws=ws
                )

            # -------------------
            # START GAME
            # -------------------

            elif msg == "start":

                room_code = data["code"]

                if room_code not in rooms:
                    continue

                room = rooms[room_code]

                room["game"] = data["game"]

                broadcast(
                    room_code,
                    {
                        "type": "game-started",
                        "players": room["players"],
                        "game": room["game"]
                    }
                )

            # -------------------
            # GAME STATE UPDATE
            # -------------------

            elif msg == "state":

                room_code = data["code"]

                if room_code not in rooms:
                    continue

                room = rooms[room_code]

                room["game"] = data["state"]

                broadcast(
                    room_code,
                    {
                        "type": "state",
                        "state": room["game"]
                    },
                    except_ws=ws
                )
        except Exception as e:
            print(e)
            break

    # -------------------
    # DISCONNECT
    # -------------------

    if room_code and room_code in rooms:

        room = rooms[room_code]

        if ws in room["clients"]:
            room["clients"].remove(ws)

        room["players"] = [
            p for p in room["players"]
            if p["uid"] != uid
        ]

        # Delete empty room
        if len(room["players"]) == 0:

            del rooms[room_code]

        else:

            # Host left -> make first player host
            if room["host"] == uid:
                room["host"] = room["players"][0]["uid"]

            broadcast(
                room_code,
                {
                    "type": "lobby-update",
                    "host": room["host"],
                    "players": room["players"]
                }
            )


# -------------------
# RUN SERVER
# -------------------

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        threaded=True
    )