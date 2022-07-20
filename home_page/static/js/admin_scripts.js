
let el_id= "#content > h1"

// Set the date we're counting down to
var countDownDate = new Date("Jul 23, 2022 15:37:25").getTime();

// Update the count down every 1 second
var x = setInterval(function() {

  // Get today's date and time
  var now = new Date().getTime();

  // Find the distance between now and the count down date
  var distance = countDownDate - now;

  // Time calculations for days, hours, minutes and seconds
  var days = Math.floor(distance / (1000 * 60 * 60 * 24));
  var hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
  var minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
  var seconds = Math.floor((distance % (1000 * 60)) / 1000);

  // Display the result in the element with id="demo"
  let time_str = "🔥 " + days + "d " + hours + "h " + minutes + "m " + seconds + "s ";

  document.querySelector(el_id).innerHTML = time_str
  // document.querySelector(el_id).append(time_str);

  // document.getElementById(el_id).innerHTML = days + "d " + hours + "h "

  // If the count down is finished, write some text
  if (distance < 0) {
    clearInterval(x);
    document.querySelector(el_id).innerHTML = "EXPIRED";
  }
}, 1000);