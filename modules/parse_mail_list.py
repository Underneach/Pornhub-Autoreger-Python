mail_list = []


def Parse_Mail_List(mail_file_path):
    with open(mail_file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        line = line.strip()  # Удалить лишние пробелы и символы новой строки
        mail_list.append(line)  # Добавить обработанную строку
        return mail_list
