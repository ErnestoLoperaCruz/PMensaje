import sqlite3

def validar_usuaro(usuario,password):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+usuario+"' and password='"+password+"' and estado='1'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def vermsnenviados(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora,u.nombres from usuarios u, mensajeria m where u.correo=m.id_usu_recibe and m.id_usu_envia='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado

def vermsnrecibidos(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select m.asunto,m.mensaje,m.fecha,m.hora,u.nombres from usuarios u, mensajeria m where u.correo=m.id_usu_envia and m.id_usu_recibe='"+correo+"' order by fecha desc, hora desc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado


def listadoUsuarios(correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo<>'"+correo+"' and estado='1' order by nombres asc"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado


def regis_usuaro(t_doc,n_doc,nombre,apellido,n_tel,correo,direccion,cargo,f_nac,genero,passw2,codigo2):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into usuarios(t_doc,n_doc,nombres,apellidos,n_tel,correo,direccion,cargo,f_nac,genero,password,codigoactivacion,estado) values ('"+t_doc+"','"+n_doc+"','"+nombre+"','"+apellido+"','"+n_tel+"','"+correo+"','"+direccion+"','"+cargo+"','"+f_nac+"','"+genero+"','"+passw2+"','"+codigo2+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "Usuario Registrado Sastisfactoriamente"
    #try:
        #db=sqlite3.connect("mensajes.s3db")
        #db.row_factory=sqlite3.Row
        #cursor=db.cursor()
        #consulta="insert into usuarios (nombres,correo,password,estado,codigoactivacion) values ('"+nombre+"','"+correo+"','"+password+"','0','"+codigo+"')"
        #cursor.execute(consulta)
        #db.commit()
        #return "Usuario Registrado Sastisfactoriamente"
    #except:
        #return "Error, el correo "+correo+" y/o el usuario "+nombre+" ingresados ya se encuentran registrados en nuestra plataforma"

def activarU(codigo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set estado='1' where codigoactivacion='"+codigo+"'"
    print(consulta)
    cursor.execute(consulta)
    db.commit()
    
    consulta="select *from usuarios where estado='1' and  codigoactivacion='"+codigo+"'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado
    
def reg_mensaje(asunto,mensaje,origen,destino):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="insert into mensajeria (asunto,mensaje,fecha,hora,id_usu_envia,id_usu_recibe,estado) values ('"+asunto+"','"+mensaje+"',DATE('now'),TIME('now'),'"+origen+"','"+destino+"','0')"
    cursor.execute(consulta)
    db.commit()
    return "1"

def ActualizarContraseña(passnew,origen):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="update usuarios set password='"+passnew+"'where correo='"+origen+"'"
    print(consulta)
    cursor.execute(consulta)
    db.commit()


def ResContrasena (correo):
    db=sqlite3.connect("mensajes.s3db")
    db.row_factory=sqlite3.Row
    cursor=db.cursor()
    consulta="select *from usuarios where correo='"+correo+"' and estado='1'"
    cursor.execute(consulta)
    resultado=cursor.fetchall()
    return resultado
    