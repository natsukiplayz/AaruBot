import json
import random

from aiohttp import web


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


async def ludo_socket(request):

    ws = web.WebSocketResponse()
    await ws.prepare(request)

    room_code = None
    user_id = None

    async for msg in ws:

        if msg.type != web.WSMsgType.TEXT:
            continue

        data = json.loads(msg.data)

        # CREATE ROOM
        if data["type"] == "create":

            room_code = generate_code()
            user_id = data.get("uid")

            rooms[room_code] = {
                "players": [
                    {
                        "uid": user_id,
                        "name": data.get("name", "Player"),
                        "color": "red"
                    }
                ],
                "clients": [ws],
                "game": None
            }

            await ws.send_json({
                "type": "created",
                "code": room_code
            })


        # JOIN ROOM
        elif data["type"] == "join":

            room_code = data["code"]

            if room_code not in rooms:
                await ws.send_json({
                    "type": "error",
                    "message": "Room not found"
                })
                continue


            room = rooms[room_code]

            color = COLORS[
                len(room["players"])
                % len(COLORS)
            ]

            room["players"].append({
                "uid": data.get("uid"),
                "name": data.get("name","Player"),
                "color": color
            })

            room["clients"].append(ws)

            await ws.send_json({
                "type":"joined",
                "players":room["players"]
            })


            await broadcast(
                room_code,
                {
                    "type":"lobby-update",
                    "players":room["players"]
                }
            )


        # GAME STATE UPDATE
        elif data["type"] == "state":

            room_code = data["code"]

            if room_code in rooms:

                rooms[room_code]["game"] = data["state"]

                await broadcast(
                    room_code,
                    {
                        "type":"state",
                        "state":data["state"]
                    },
                    sender=ws
                )


    return ws



async def broadcast(code, data, sender=None):

    room = rooms.get(code)

    if not room:
        return


    for client in room["clients"]:

        if client != sender:
            await client.send_json(data)



def setup_ludo(app):

    app.router.add_get(
        "/ludo",
        ludo_socket
    )