import urllib
def getIP(context):
    peer = context.peer()
    decoded_peer = urllib.parse.unquote(peer)
    
    if decoded_peer.startswith('ipv6:'):
        ip = decoded_peer.split('[')[1].split(']')[0] 
    elif decoded_peer.startswith('ipv4:'):
        ip = decoded_peer.split(':')[1]
    else:
        ip = 'unknown'
    port = decoded_peer.split(':')[-1]
    return ip, port