import smtplib 
from email.message import EmailMessage 

def enviar(email_destino,asunto,mensajemail):
    email_origen="lauraangelicafong@gmail.com"
    password="M9ZJFOVmhqW5vRTG" #tu contraseña aqui sin espacios 
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

if __name__ == "__main__":
    enviar("f_laura@outlook.com","Prueba","Hola mundo")