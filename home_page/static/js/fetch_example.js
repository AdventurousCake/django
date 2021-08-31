const request = new Request('http://localhost/ping:9090')
fetch(request)
    .then(response => {
        if (response.status === 200) {
            let x =  response.json();
            console.log(x)
        } else {
            throw new Error('Что-то пошло не так на API сервере.');
        }
    })
    .then(response => {
        console.debug(response);
        // ...
    }).catch(error => {
    console.error(error);
});