from re import match
from urllib import parse
from ipaddress import ip_address

def build_url(scheme, host, port, path=''):
    try:
        port = int(port)
        if not (port > 1 or port < 0x10000):
            return False
        
        if not scheme.startswith('http') or len(scheme) > 9:
            return False
        
        host_pattern = r'^((\d{1,3}\.){3}\d{1,3}|([a-zA-Z0-9\-]+\.)+[a-zA-Z\.]{2,})$'
        if not match(host_pattern,host):
            return False
        
        if not path[0] == '/':
            path = '/' + path

        url = (scheme + host + ':' + str(port) + path).lower()
        parsed_url = parse.urlparse(url)
        parsed_host = parsed_url.netloc.split(':')[0]
        if (match(r'^((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])$', parsed_host) and ip_address(parsed_host).is_private) or (parsed_host == 'app.com'):
            return False
        
        return url
        
    except Exception as e:
        print(e,flush=True)
        return False