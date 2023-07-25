import httpx
import time


with httpx.Client() as client:
    response = client.post(
        'http://api.captcha.guru/in.php',
        headers={'Content-Type': 'application/json'},
        json={
            "key": "",
            "method": "userrecaptcha",
            "googlekey": "6LfyQRoUAAAAAApqS-inJxUwCOtvOHwKxJuZCsuv",
            "pageurl": "https://rt.pornhub.com/signup/",
            "version": "v2",
            "json": 1
        }
    )
    request_id = response.json()['request']

    while True:
        response = client.get(
            'http://api.captcha.guru/res.php',
            params={
                "key": "",
                "action": "get",
                "id": f"{request_id}",
                "json": 1
            }
        )
        if response.json()['request'] == 'CAPCHA_NOT_READY':
            print(response.json()['request'])
            time.sleep(5)
        else:
            print(response.json()['request'])
            break
