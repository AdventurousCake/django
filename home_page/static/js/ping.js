// !!! update from index
"use strict";

window.onload = function () {
    let item = document.querySelector("#ping")
    let data1 = document.querySelector("#ping-data")

    item.onclick = () => {
        fetch("http://127.0.0.1:8000/ping/").then(function(response) {
        // data.innerHTML = response.json()
        // first parse response then use value
            // {% url "ping" %}
        return response.text();
    }).then(function(data) {
        console.log(data);
        // let x = data1
        data1.innerHTML = data
    })
    }
}

// window.onload = function() {
//     let item = document.querySelector("#ping")
//     let data = document.querySelector("#ping-data")
//
//     function ping(){
//     fetch("http://127.0.0.1:8080").then(function(response) {
//         item.innerHTML = response.json()
//         return response.json();
//     }).then(function(data) {
//         console.log(data);
//     })
//
//     // const request = new Request('localhost:8080')
//     // fetch(request)
//     //     .then(response => {
//     //         if (response.status === 200) {
//     //             item.innerHTML = response.toString()
//     //             return response.json();
//     //         } else {
//     //             throw new Error('Что-то пошло не так на API сервере.');
//     //         }
//     //     })
//     //     .then(response => {
//     //         console.debug(response);
//     //         // ...
//     //     }).catch(error => {
//     //     console.error(error);
//     // });
//
//     }
//     setInterval(ping, 5000)
// }