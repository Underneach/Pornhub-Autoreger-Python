import httpx
import time


def Capcha_Solver(captcha_key):
    with httpx.Client() as client:
        response = client.post(
            'http://api.captcha.guru/in.php',
            headers={'Content-Type': 'application/json'},
            json={
                "key": f"{captcha_key}",
                "method": "userrecaptcha",
                "googlekey": "6LectvslAAAAAC51V1_hA5yWoPnhCvYbJaulh5Us",
                "pageurl": "https://rt.pornhub.com/signup/",
                "version": "v3",
                "json": 1
            }
        )
        request_id = response.json()['request']

        while True:
            response = client.get(
                'http://api.captcha.guru/res.php',
                params={
                    "key": f"{captcha_key}",
                    "action": "get",
                    "id": f"{request_id}",
                    "json": 1
                }
            )
            if response.json()['request'] == 'CAPCHA_NOT_READY':
                time.sleep(5)
            else:
                return response.json()['request']
