from flask import Flask, render_template, request 
import hashlib
import controlDB
from datetime import datetime
import random
import envioemail
app = Flask(__name__)

email_usuario=""
Remitente=""

@app.route("/")
def hello_world():
    return render_template("Inicio.html")

@app.route("/VerificarUsuario",methods=["GET","POST"])
def VerificarUsuario():
    if request.method=="POST":
        correo=request.form["txtemaillogin"]
        passw=request.form["txtpass"]
        correo=correo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        passw2=passw.encode()
        passw2=hashlib.sha384(passw2).hexdigest() #96 caracteres
        
        respuesta=controlDB.validar_usuaro(correo,passw2)
                
        global email_usuario
        global Remitente
        if len(respuesta)==0:
            email_usuario=""
            remitente=""
            mensaje="ERROR DE AUtenticacion!!! verifique su usuario y contraseña y/o Verifique si su usario se encuentra activo."
            return render_template("Mensaje.html",data=mensaje)
        else:
            email_usuario=correo
            Remitente=respuesta[0][1]
            respuesta2=controlDB.listadoUsuarios(correo)
            
            return render_template("CrearMensajes.html",data=respuesta2,usuario=respuesta)
            
        
@app.route("/RegistrarUsuario",methods=["GET","POST"])
def RegistrarUsuario():
    if request.method=="POST":
        nombre=request.form["txtnombregistro"] #el servidor está tratando de leer un valor que fue posteado bajo el name txtnombregistro en registro.html
        correo=request.form["txtemailregistro"]#""
        passw=request.form["txtpassregistro"] #""
        passw2=passw.encode() #toma la contraseña del registro de usuario y la convierta en base64(para almacenarla de forma segura)
        passw2=hashlib.sha384(passw2).hexdigest() #96 caracteres  #Encripción de la contraseña           
        codigo=datetime.now() #retorna fecha y hora del instante en que se registra
        codigo2=str(codigo) #se convierte la hora en un codigo str
        codigo2=codigo2.replace("-","")#""
        codigo2=codigo2.replace(":","")#""
        codigo2=codigo2.replace(" ","")#""
        codigo2=codigo2.replace(".","")#""
        
        link = "http://localhost:5000/ActivarUsuario?codigo="+codigo2 #enlace que se envia al correo
        mensajemail="Sr@ "+nombre+", usted se ha registrado en nuestra plataforma de mensajería empresarial; \n\n ingrese en el siguiente enlace para activar su cuenta :\n\n"+link+ "\n\nMuchas Gracias"
        asunto="Equipo 14 te ha enviado codigo de activacion de la plataforma de mensajería"
       
        try:#encapsula el error, evita que se reviente el programa por errores por si falla no se reviente el codigo sino que muestre el mensaje error al registrar usuario..
            respuesta=controlDB.regis_usuaro(nombre,correo, passw2,codigo2) #Esta es la respuesta que da la base de datos acerca de la info de registro.Ej: por si ya esta regisrado el ususario, falle base de datos etc
        except Exception as e:
            mensaje=f"Error al registrar usuario, verifique que el correo o el nombre de usuario no se encuentren registrados."#este mensaje es el que se muestra cuando no se pudo ejecutar el programa, es uno de los posibles errores
            return render_template("Mensaje.html",data=mensaje) #la respuesta del navegador para mostrar el mensaje
        try:
            envioemail.enviar(correo,asunto,mensajemail)#en caso tal que se presente un problema en el servidor, 
        except Exception as e:
            mensaje=f"Error al enviar correo de activacion. {e}"
            return render_template("Mensaje.html",data=mensaje)
        mensaje="El usuarios "+nombre+" Registrado Satisfactoriamente, revise el correo para terminar el proceso de registro"#mensaje que se muestra al ususario en a registrarse correctamente
        return render_template("Mensaje.html",data=mensaje)
         
    if request.method=="GET":
        return render_template("registro.html")

    
@app.route("/ActivarUsuario",methods=["GET"])
def ActivarUsuario():
    if request.method=="GET":
        codigo = request.args.get('codigo')#extrae codigo que se envia en la URL o enlace
        respuesta=controlDB.activarU(codigo) #activacion del usuario con el codigo
        
        if len(respuesta)==0: #si la respuesta no se activa o viene vacia 0 no se activa el codigo
            mensaje="Codigo incorrecto"
            return render_template("Mensaje.html",data=mensaje)
        else:
            mensaje="Usuario Activado Satisfactoriamente"
            return render_template("Mensaje.html",data=mensaje)
        
        
@app.route("/enviarCorreo",methods=["GET","POST"])
def enviarCorreo():
    if request.method=="POST":
        asunto=request.form["Asunto"]
        email_destino=request.form["CorreoDestino"]
        Mensaje=request.form["Mensaje"]
        mensajemail="Has recibido un mensaje nuevo de "+Remitente+", por favor revise en nuestra plataforma.\n\n Muchas gracias por utilizar nuestro servico de mensajería empresarial."
        asunto=asunto.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        email_destino=email_destino.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        Mensaje=Mensaje.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        controlDB.reg_mensaje(asunto,Mensaje,email_usuario,email_destino)
        envioemail.enviar(email_destino,asunto,mensajemail)
        print(email_usuario)
        print(Remitente)
        return "Email enviado satisfactoriamente"
    
    
    
    
@app.route("/HistorialMSNEnviados",methods=["GET","POST"])
def HistorialMSNEnviados():
    resultado=controlDB.vermsnenviados(email_usuario)
    return render_template("MSN.html",data=resultado)

@app.route("/HistorialMSNRecibidos",methods=["GET","POST"])
def HistorialMSNRecibidos():
    resultado=controlDB.vermsnrecibidos(email_usuario)
    return render_template("MSN.html",data=resultado)


@app.route("/ActContraseña",methods=["GET","POST"])
def ActContraseña():
    if request.method=="POST":
        PassNew=request.form["Pass"]
        PassNew=PassNew.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
        PassNew1=PassNew.encode()
        PassNew1=hashlib.sha384(PassNew1).hexdigest()
        respuesta=controlDB.ActualizarContraseña(PassNew1,email_usuario)
        return "Actualización de Contraseña Sastisfactoria"
        
                   