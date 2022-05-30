# smtp-client

## Usage:

Перед тем, как запустить надо настроить конфигурационный файл (config.cfg).

```
[Message]
Mail = destination_mail12mail.ru; destination2@mail.ru
Title = Title of mail
Attachments = attachments/001.gif, attachments/2.gif
MessageFile = msg.txt 

[UserData]
Mail = my_mail@yandex.ru
Password = my_password

[Connection]
SmtpAddress = smtp.yandex.ru
Port = 465
Timeout = 1000
```

Поля UserData['Mail'] и Connection['SmtpAddress'] должны быть согласованы.

## Запуск скрипта

```
python main.py
```
