def Mail_Parser(mail):
    email = mail.split(':')[0]
    password = mail.split(':')[1]
    nickname = email.split('@')[0]
    return email, password, nickname
