const password = document.getElementById('pwrd1'); //password==pswrd1
const password2 = document.getElementById('pwrd2'); //""
const parrafo = document.getElementById('warnings');//""
const regexMayus = /[A-Z]/g;// expresion regular de un texto que contiene letras en mayuscula
const regexMinus = /[a-z]/g;// expresion regular de un texto que contiene letras en minuscula
const regexNum = /[0-9]/g; // expresion regular de un texto que contiene numeros
const regexSimbol = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/g;// expresion regular de un texto que contiene caracteres especiales

//funcion que escucha eventos ocurridos en el formulario form cuando se presiona submit
form.addEventListener('submit', (e) => { //se le manda el parametro e a la funcion flecha 
    e.preventDefault(); // el parametro evita que se envie automaticamete la info del formulario al presionar submit y espera que se ejecuten las validaciones 
    let warning = ""; //se declara como variable  warning
    let flag = false; // se declara la variable flag false y cuando no pasa validacion cambia de estado a true
    parrafo.innerHTML = ""; //inicializamos

    if (password.value.length < 8 ) {
        warning += '😕 Password must be at least 8 characters long <br>';
        flag = true;
    }
    if (!password.value.match(regexMayus)) {
        warning += '😕 Password must contain at least one uppercase letter <br>';
        flag = true;
    }
    if (!password.value.match(regexMinus)) {
        warning += '😕 Password must contain at least one lowercase letter <br>';
        flag = true;
    }
    if (!password.value.match(regexNum)) {
        warning += '😕 Password must contain at least one number <br>';
        flag = true;
    }
    if (!password.value.match(regexSimbol)) {
        warning += '😕 Password must contain at least one special character <br>';
        flag = true;
    }
    if (password.value != password2.value) {
        warning += '😕 Passwords do not match <br>';
        flag = true;
    }
    if(flag){
        parrafo.innerHTML = warning;
    }else{
        form.submit();// se envia el formulario en caso que haya pasado las validaciones
        parrafo.innerHTML = "Sending...🚀";
    }
});