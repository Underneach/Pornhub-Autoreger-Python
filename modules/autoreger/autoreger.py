import concurrent.futures
import json
import httpx
import random
import string

from modules.autoreger.headers import headers_start, headers_signup, headers_reg
from modules.autoreger.mail_parser import Mail_Parser
from modules.autoreger.parse_token import Parse_Token
from modules.autoreger.capcha_solver import Capcha_Solver
from modules.autoreger.get_link import get_confirmation_link


def Autoreger(threads, mail_list, captcha_key):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for mail in mail_list:
            future = executor.submit(Registration, mail, captcha_key)
            futures.append(future)

        concurrent.futures.wait(futures)


def Registration(mail, captcha_key):
    email, email_password, email_nickname = Mail_Parser(mail)
    nickname = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    password = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(16))
    print(f"[+] {email} : Начинаю регистрацию")

    with httpx.Client(http2=True, follow_redirects=True, max_redirects=10) as client:
        try:
            respone_start = client.get(
                'https://rt.pornhub.com/',
                headers=headers_start
            )

            token = Parse_Token(respone_start.text)
            print(f"[+] {email} : Получен Токен : {token}")

            client.get(
                'https://rt.pornhub.com/signup',
                headers=headers_start
            )

            respone_nick = client.post(
                f'https://rt.pornhub.com/user/create_account_check?token={token}',
                headers=headers_signup,
                data={'check_what': 'username',
                      'username': nickname})
            print(f'[+] {email} : Username : {nickname} : {json.loads(respone_nick.text)["username"]}')

            response_pass = client.post(
                f'https://rt.pornhub.com/user/create_account_check?token={token}',
                headers=headers_signup,
                data={'check_what': 'password',
                      'password': password})
            print(f'[+] {email} : Password : {password} : {json.loads(response_pass.text)["password"]}')

            response_mail = client.post(
                f'https://rt.pornhub.com/user/create_account_check?token={token}',
                headers=headers_signup,
                data={'check_what': 'email',
                      'email': email})
            print(f'[+] {email} : Mail : {json.loads(response_mail.text)["email"]}')

            print(f'[+] {email} : Решение капчи')
            captcha_token = Capcha_Solver(captcha_key)
            print(f'[+] {email} : Captcha : Succefull')

            response_reg = client.post('https://rt.pornhub.com/signup',
                                       headers=headers_reg,
                                       data={'token': token,
                                             'redirect': '',
                                             'taste_profile': '',
                                             'g-recaptcha-response': captcha_token,
                                             'captcha_type': 'score',
                                             'signup_modal': 'true',
                                             'email': email,
                                             'username': nickname,
                                             'password': password})
            print(f'[+] {email} : Аккаунт создан')

            link = get_confirmation_link(email, email_password)

            print(f'[+] {email} : Подтверждение аккаунта')
            client.get(link, headers=headers_start)

        except Exception as e:
            print(f'Ошибка при регистрации аккаунта {email} | {e}')
