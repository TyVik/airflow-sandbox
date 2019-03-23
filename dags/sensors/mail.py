import imaplib


def mailbox():
    mail = imaplib.IMAP4_SSL('imap.mail.ru')
    mail.login('tyvik@mail.ru', '')
    mail.select("inbox")
    return mail
