import imaplib
import email
import re
import time


def get_confirmation_link(email_nickname, email_password):
    IMAP_SERVER = 'imap.rambler.ru'
    regular_string = r'https://rt\.pornhub\.com/user/confirm\?token=\S+'

    # Connect to the email server
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(email_nickname, email_password)

    # Select the mailbox
    mail.select('INBOX')

    # Search for the last email
    result, data = mail.search(None, 'ALL')

    # Check for empty inbox
    while len(data[0].split()) == 0:
        print(f"[*] {email_nickname} : Waiting for email")
        time.sleep(5)

    last_email_id = data[0].split()[-1]
    result, data = mail.fetch(last_email_id, '(RFC822)')

    # Extract the text from the email
    raw_email = data[0][1]
    email_message = email.message_from_bytes(raw_email)
    text = ""

    if email_message.is_multipart():
        for part in email_message.walk():
            if part.get_content_type() == 'text/plain':
                text = part.get_payload(decode=True).decode('utf-8')
    else:
        text = email_message.get_payload(decode=True).decode('utf-8')

    mail.close()
    mail.logout()

    # Search for the confirmation link in the email text
    match = re.search(regular_string, text)
    link = match.group(0) if match else None

    return link


def run(email_nickname, email_password):
    try:
        confirmation_link = get_confirmation_link(email_nickname, email_password)
        return confirmation_link

    except Exception as e:
        print(f"{email_nickname} : Error while getting the email : {e}")
