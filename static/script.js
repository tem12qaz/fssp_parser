
document.querySelector("#find").onclick = function () {
    document.getElementById('input_div').hidden = true;
    document.getElementById('wait_div').hidden = false;
    var fio = document.user_data.fio.value;
    var date = document.user_data.date.value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://141.144.244.252/ugUV876gbvuybhBVfcjh9t6tv', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        'fio': fio, 'date': date
    }));

    xhr.onreadystatechange = function() {//Вызывает функцию при смене состояния.
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            if (xhr.responseText == 'false') {
                document.getElementById('wait_div').hidden = true;
                document.getElementById('input_div').hidden = false;
            }
            else {
                document.getElementById('wait_div').hidden = true;
                document.getElementById('captcha').setAttribute('src', xhr.responseText);
                document.getElementById('captcha_div').hidden = false;
            }
        }
    }
}

document.querySelector("#captcha_find").onclick = function () {
    document.getElementById('captcha_div').hidden = true;
    document.getElementById('wait_div').hidden = false;
    var captcha = document.captcha_data.captcha.value;
    var xhr = new XMLHttpRequest();
    xhr.open("POST", 'http://141.144.244.252/jvvc67Vfcd6gy8vFJjv678v56f', true);
    xhr.setRequestHeader('Content-Type', 'application/json');
    xhr.send(JSON.stringify({
        'captcha': captcha
    }));

    xhr.onreadystatechange = function() {//Вызывает функцию при смене состояния
        if(xhr.readyState == XMLHttpRequest.DONE && xhr.status == 200) {
            console.log(xhr.responseText);
            if (xhr.responseText != 'true'){
                document.getElementById('captcha').setAttribute('src', xhr.responseText)
                document.getElementById('captcha_div').hidden = false;
                document.getElementById('wait_div').hidden = true;
            }
            else {
//                document.getElementById('captcha_div').hidden = true;
                document.getElementById('input_div').hidden = false;
                document.getElementById('wait_div').hidden = true;
            }
        }
    }
}
