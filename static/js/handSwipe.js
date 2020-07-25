//moved from main htmls script

// adding swipe detection
document.addEventListener('touchstart', handleTouchStart, false);
document.addEventListener('touchmove', handleTouchMove, false);

var xDown = null;
var yDown = null;

function handleTouchStart(evt) {
    xDown = evt.touches[0].clientX;
    yDown = evt.touches[0].clientY;
};

function handleTouchMove(evt) {
    if ( ! xDown || ! yDown ) {
        return;
    }

    var xUp = evt.touches[0].clientX;
    var yUp = evt.touches[0].clientY;

    var xDiff = xDown - xUp;
    var yDiff = yDown - yUp;

    if ( Math.abs( xDiff ) > Math.abs( yDiff ) ) {/*most significant*/
        if ( xDiff > 0 ) {
            /* left swipe */
            $("#clock").fadeOut('slow');
            $("#date").fadeOut('slow');
            $("#blurbackground").fadeIn('fast','linear', function(){
                    document.getElementById("btnNext").click();
             });
       } else {
            /* right swipe */
            $("#clock").fadeOut('slow');
            $("#date").fadeOut('slow');
            $("#blurbackground").fadeIn('fast','linear', function(){
                    document.getElementById("btnPrev").click();
             });
        }
    } else {
        if ( yDiff > 0 ) {
            /* up swipe */
            showCalendar();
        } else {
            /* down swipe */
            hideCalendar();
        }
    }
    /* reset values */
    xDown = null;
    yDown = null;
}

// end swipe detection