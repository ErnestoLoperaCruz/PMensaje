 const password = document.getElementById('pwrd1');
const password2 = document.getElementById('pwrd2');
const parrafo = document.getElementById('warnings');
const regexMayus = /[A-Z]/g;
const regexMinus = /[a-z]/g;
const regexNum = /[0-9]/g;
const regexSimbol = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/g;

form.addEventListener('submit', (e) => {
    e.preventDefault();
    let warning = "";
    let flag = false;
    parrafo.innerHTML = "";

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
        form.submit();
        parrafo.innerHTML = "Sending...🚀";
    }
});