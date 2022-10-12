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
        t_doc=request.form["sl_t_doc"]
        n_doc=request.form["n_doc"]
        nombre=request.form["txtnombregistro"] 
        apellido=request.form["txtapellidoregistro"]
        n_tel=request.form["n_tel"]
        correo=request.form["txtemailregistro"]
        direccion=request.form["txtdireccionregistro"]
        cargo=request.form["txtcargoregistro"]
        f_nac=request.form["sl_f_nac"]
        genero=request.form["sl_genero"]
        passw=request.form["txtpassregistro1"] 
        
        t_doc=t_doc.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        n_doc=n_doc.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        nombre=nombre.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        apellido=apellido.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        n_tel=n_tel.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        correo=correo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        direccion=direccion.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        cargo=cargo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        f_nac=f_nac.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        genero=genero.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        passw=passw.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","").replace("select","").replace("insert","").replace("delete","").replace("update","").replace("where","").replace("Select","").replace("Insert","").replace("Delete","").replace("Update","").replace("Where","")
        
        passw2=passw.encode() 
        passw2=hashlib.sha384(passw2).hexdigest() 
        codigo=datetime.now() 
        codigo2=str(codigo) 
        codigo2=codigo2.replace("-","")#""
        codigo2=codigo2.replace(":","")#""
        codigo2=codigo2.replace(" ","")#""
        codigo2=codigo2.replace(".","")#""
        
        link = "http://localhost:5000/ActivarUsuario?codigo="+codigo2 
        mensajemail="Sr@ "+nombre+" "+apellido+", usted se ha registrado en nuestra plataforma de mensajería empresarial; \n\n ingrese en el siguiente enlace para activar su cuenta :\n\n"+link+ "\n\nMuchas Gracias"
        asunto="Equipo 14 te ha enviado codigo de activacion de la plataforma de mensajería"
       
        try:
            respuesta=controlDB.regis_usuaro(nombre,correo, passw2,codigo2) 
        except Exception as e:
            mensaje=f"Error al registrar usuario, verifique que el correo o el nombre de usuario no se encuentren registrados."
            return render_template("Mensaje.html",data=mensaje) 
        try:
            envioemail.enviar(correo,asunto,mensajemail)
        except Exception as e:
            mensaje=f"Error al enviar correo de activacion. {e}"
            return render_template("Mensaje.html",data=mensaje)
        mensaje="El usuario "+nombre+" "+apellido+" se ha registrado satisfactoriamente, revise el correo para terminar el proceso de registro."#mensaje que se muestra al ususario en a registrarse correctamente
        return render_template("Mensaje.html",data=mensaje)         
    if request.method=="GET":
        return render_template("registro.html")
   
@app.route("/ActivarUsuario",methods=["GET"])
def ActivarUsuario():
    if request.method=="GET":
        codigo = request.args.get('codigo')
        respuesta=controlDB.activarU(codigo) 
        
        if len(respuesta)==0: 
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
        mensajemail="Has recibido un mensaje nuevo de "+Remitente+", por favor revise en nuestra plataforma.\n\n Muchas gracias por utilizar MSN TEAM CORP."
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
       
@app.route("/ResContrasena",methods=["GET","POST"])
def ResContrasena():
    if request.method=="POST":
        correo=request.form["in_Mail"]
        correo=correo.replace("SELECT","").replace("INSERT","").replace("DELETE","").replace("UPDATE","").replace("WHERE","")
       
        codigo=datetime.now()
        codigo2=str(codigo)
        codigo2=codigo2.replace("-","")
        codigo2=codigo2.replace(":","")
        codigo2=codigo2.replace(" ","")
        codigo2=codigo2.replace(".","")
        PassNew1=codigo2.encode()
        PassNew1=hashlib.sha384(PassNew1).hexdigest()
        
        respuesta=controlDB.ResContrasena(correo)
                
        if len(respuesta)==0:
            email_usuario=""
            remitente=""
            mensaje="ERROR el correo ingresado no está registado con ningún usuario o no se encuentra activo."
            return render_template("Mensaje.html",data=mensaje)
        else:
            controlDB.ActualizarContraseña(PassNew1,correo)
            mensaje="Señor@ usuario se le ha enviado una clave temporal a su correo "+correo+" por favor ingrese MSN TEAM CORP. y cambie la contraseña"
            asunto="Recuperación Contraseña plataforma MSN TEAM CORP."
            mensajemail="Señor@ usuario su clave temporal es "+codigo2+", por favor ingrese a su perfil y cambie su contraseña.\n\n Muchas gracias por utilizar MSN TEAM CORP."
            envioemail.enviar(correo,asunto,mensajemail)
            
            return render_template("Mensaje.html",data=mensaje)
    return render_template("ResContraseña.html")                  