import smtplib 
from email.message import EmailMessage 

def enviar(email_destino,asunto,mensajemail):
    try:
        email_origen="Equipo14NCR2109uninorte@outlook.com"
        password="rjvXsZCIQbLT5hRy" #tu contraseña aqui sin espacios 
        email = EmailMessage()
        email["From"] = email_origen
        email["To"] = email_destino
        email["Subject"] = asunto
        email.set_content(mensajemail)

        # Send Email
        smtp = smtplib.SMTP("smtp-relay.sendinblue.com", port=587)
        smtp.starttls()
        smtp.login(email_origen, password)
        smtp.sendmail(email_origen, email_destino, email.as_string())
        smtp.quit()
        return "se te ha enviado las instrucciones para activar la cuenta."
    except:
        return "Error, no fue posible enviarte el correo de activación en este momento, comunicate con soporte de MSN TEAM CORP."

