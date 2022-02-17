const date = new Date();
document.querySelector('.year').innerHTML = date.getFullYear();

// Fadeout messages
setTimeout(function () {
    $('#message').fadeOut('slow');
}, 10000);