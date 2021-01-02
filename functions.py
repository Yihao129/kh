from urllib.parse import unquote


def decodeMsg(msg):
    msg["msg"] = unquote(unquote(msg["msg"]))
    return msg