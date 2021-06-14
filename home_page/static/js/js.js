"use strict";

window.onload = function() {
    // popup
    let popup = document.querySelector(".window");
    let flash = document.querySelector(".open-window");
    let close = document.querySelector(".close-window");

    flash.onclick = function () {
        // popup.style.display = "block";
        // popup.classList.toggle('active')
        let x = popup;
        if (x.style.display === "block") {
            x.style.display = "none";
        } else {
            x.style.display = "block";
        }
    }

    close.onclick = function () {
        popup.style.display = "none";
    }

    // nav
    let icon = document.querySelector(".icon");
    let y = document.querySelector(".hamburger")

    // icon.onclick = function() {
    //     if (y.style.display === "block") {
    //         alert("none")
    //         y.style.display = "none";
    //     } else {
    //         alert("block")
    //         y.style.display = "block";
    //     }
    //     // y.style.display = "block";
    // }
    //     icon.addEventListener("click", alert(123));
    function menuOpen() {
        let hamburgerBtn = document.querySelector(".icon");
        let mobileMenu = document.querySelector(".hamburger")


        hamburgerBtn.addEventListener("click", ()=> {
            if(mobileMenu.style.display === "block") {
                mobileMenu.style.display = "none";
            } else {
                mobileMenu.style.display = "block";
            }
        })
    }

    menuOpen();
}

