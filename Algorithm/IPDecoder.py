import urllib
def getIP(context):
    peer = context.peer()
    decoded_peer = urllib.parse.unquote(peer)
    ip = client_ip = decoded_peer.split('[')[1].split(']')[0]
    port = decoded_peer.split(']')[1].split(':')[1]
    print(f"ip: {ip} port: {port}")
    return ip, port