import os


def Input():

    while True:
        threads = input('\nВведите количетсво потоков: ')
        if threads:
            break
        else:
            print('Введите количетсво аккаунтов: ')

    while True:
        mail_file_path = input('\nВведите путь к файлу с почтами,аккаунты будут созданы на все почты: ')
        if os.path.exists(mail_file_path):
            break
        else:
            print('Файл не найден, введите путь еще раз: ')
    while True:
        captcha_key = input('\nВведите ключ от Captcha Guru: ')
        if captcha_key:
            break
        else:
            print('Введите ключ от Captcha Guru: ')

    return int(threads), mail_file_path, captcha_key
