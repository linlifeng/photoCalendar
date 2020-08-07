// moved from calendar.js
//function showUpload(date)
//{
//    $('#adminbox').load("/uploadbox/" + date).fadeIn();
//}

function showEditDiary(date)
{
    $('#diary_display').load("/write_diary/" + date).fadeIn();
}

function showDiary(date)
{
    $('#diary_display').load("/diary/" + date).fadeIn();
}

function hideDiary()
{
    $('#diary_display').fadeOut();
}
// moved from main html

function useLightBox(){
        lightbox.option({
        'resizeDuration': 200,
        'wrapAround': true
    })
}

function useSwipeBox(){
        ;( function( $ ) {
            $( '.swipebox' ).swipebox();
        } )( jQuery );
}


// section2 moved from main html
function startTime() {
    var today = new Date();
    var d = today.getDate();
    var D = today.getDay();
    var y = today.getFullYear();
    var mo = today.getMonth() + 1;
    var h = today.getHours();
    var m = today.getMinutes();
    var s = today.getSeconds();
    m = checkTime(m);
    s = checkTime(s);
    document.getElementById('clock').innerHTML =
    h + ":" + m;
    document.getElementById('date').innerHTML =
    y + '.' + mo + '.' + d;

    var t = setTimeout(startTime, 500);
}
function checkTime(i) {
    if (i < 10) {i = "0" + i};  // add zero in front of numbers < 10
    return i;
}


function showCalendar(){
    $("#blurbackground").fadeIn('fast','linear', function(){
            $("#calendarTable").animate({top:"0px"},'fast');
     });
    $("#divCalendar").fadeIn('fast');
    $("#btnNext").fadeIn('medium');
    $("#btnPrev").fadeIn('medium');
    //hideSearchResult();
}
function hideCalendar(){
    startTime();
    $("#calendarTable").animate({top:"100%"},'fast', function(){
            $("#blurbackground").fadeOut('fast');
            $('#curtain').fadeIn('fast');
    });
    $("#btnNext").fadeOut('slow');
    $("#btnPrev").fadeOut('slow');
    $("#clock").fadeIn('slow');
    $("#date").fadeIn('slow');
}


// Get element by id
function getId(id) {
    return document.getElementById(id);
}



function hideInfo(){
    $('#infoBox').fadeOut();
}
function hideAdminBox(){
    $('#adminbox').fadeOut();
}

function showSearchResult(){
    $('#search_result').fadeIn();
}
function hideSearchResult(){
    $('#search_result').fadeOut();
}
function toggleSearch(){
    $('#search_input').fadeToggle('slow');
}

$("#search_input").focus(function(){
    showSearchResult();
});


$("#curtain").click(function(){
    hideSearchResult();
});