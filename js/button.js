

$('.container-overlay').on('click', function(e) {
    console.log('clicked')

// check if click was on the overlay and not on its children
    if (e.target == this) {
    $('.container-overlay').fadeOut(150);
}
});

