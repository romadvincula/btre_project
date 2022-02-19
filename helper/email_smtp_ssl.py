import smtplib, ssl

def send_email(
    sender_email,
    password,
    receiver_email,
    message,
    port=465,
    smtp_server="smtp.gmail.com"
):
    error=""
    context=ssl.create_default_context()

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        try:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
        except Exception as e:
            error=e

    if error:
        return False, error
    else:
        return True, None