from modules.user_input import Input
from modules.parse_mail_list import Parse_Mail_List
from modules.autoreger.autoreger import Autoreger


def main():
    threads, mail_file_path, captcha_key = Input()
    mail_list = Parse_Mail_List(mail_file_path)
    Autoreger(threads, mail_list, captcha_key)


if __name__ == '__main__':
    main()
