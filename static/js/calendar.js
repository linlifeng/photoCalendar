function UrlExists(url)
{
    var http = new XMLHttpRequest();
    http.open('HEAD', url, false);
    http.send();
    return http.status!=404;
}




// Author: AlÃª Monteiro
// Created: 2013-03-06
// E-mail: lu.ale.monteiro@gmail.com

// P.S. I'm from Brazil, so the names of the weeks and months are in Portuguese.

var Calendar = function(divId) {

    //Store div id
    this.divId = divId;

    // Days of week, starting on Sunday
    this.DaysOfWeek = [
        '日',
        '一',
        '二',
        '三',
        '四',
        '五',
        '六'
    ];

    // Months, stating on January
    this.Months = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月' ];

    // Set the current month, year
    var d = new Date();

    this.CurrentMonth = d.getMonth();
    this.CurrentYear = d.getFullYear();

};

// Goes to next month
Calendar.prototype.nextMonth = function() {
    if ( this.CurrentMonth == 11 ) {
        this.CurrentMonth = 0;
        this.CurrentYear = this.CurrentYear + 1;
    }
    else {
        this.CurrentMonth = this.CurrentMonth + 1;
    }
    this.showCurrent();
};

// Goes to previous month
Calendar.prototype.previousMonth = function() {
    if ( this.CurrentMonth == 0 ) {
        this.CurrentMonth = 11;
        this.CurrentYear = this.CurrentYear - 1;
    }
    else {
        this.CurrentMonth = this.CurrentMonth - 1;
    }
    this.showCurrent();
};

// Show current month
Calendar.prototype.showCurrent = function() {
    this.showMonth(this.CurrentYear, this.CurrentMonth);
};

// Show month (year, month)
Calendar.prototype.showMonth = function(y, m) {

    var d = new Date()
        // First day of the week in the selected month
        , firstDayOfMonth = new Date(y, m, 1).getDay()
        // Last day of the selected month
        , lastDateOfMonth =  new Date(y, m+1, 0).getDate()
        // Last day of the previous month
        , lastDayOfLastMonth = m == 0 ? new Date(y-1, 11, 0).getDate() : new Date(y, m, 0).getDate();


//------------------ okay start drawing the calendar

    var html = '<table id="calendarTable">';

    // Write selected month and year
    html += '<tr><td colspan="7" id="monthHeader" onclick="hideCalendar()">' +  y + '.' + String(parseInt(m) + 1) + '</td></tr>';

    // Write the header of the days of the week
    html += '<tr>';
    for(var i=0; i < this.DaysOfWeek.length;i++) {
        if(isMobile == true){
        html += '<td class="dayHeader" style="font-size: 2em">' + this.DaysOfWeek[i] + '</td>';
        }
        else{
        html += '<td class="dayHeader">' + this.DaysOfWeek[i] + '</td>';
        }
    }
    html += '</tr>';

    // Write the days
    var i=1;
    do {

        var dow = new Date(y, m, i).getDay();

        // If Sunday, start new row
        if ( dow == 0 ) {
            html += '<tr>';
        }
        // If not Sunday but first day of the month
        // it will write the last days from the previous month
        else if ( i == 1 ) {
            html += '<tr>';
            var k = lastDayOfLastMonth - firstDayOfMonth+1;
            for(var j=0; j < firstDayOfMonth; j++) {
                html += '<td class="not-current">' + k + '</td>';
                k++;
            }
        }

        // Write the current day in the loop
        //html += '<td>' + i + '</td>';

        function zeroPad(num, places) {
              var zero = places - num.toString().length + 1;
              return Array(+(zero > 0 && zero)).join("0") + num;
            }
        var expandedm = zeroPad(parseInt(m)+1,2);
        var expandedi = zeroPad(parseInt(i),2);

        if(isMobile == true){
            html += '<td style="background-image: url(./static/photos/thumb-'
                     + expandedm+expandedi+y
                     +  '.jpg)"><a class="swipebox" href="./static/photos/'
                     + expandedm+expandedi+y
                     + '.jpg">'
                     + i
                     + '</a></td>';
        }
        else{
            // use this for the photo only. Disabling to test the diary function
//            if(UrlExists('./static/photos/' + expandedm+expandedi+y + '.jpg')){
//                html += '<td style="background-image: url(./static/photos/thumb-'
//                        + expandedm+expandedi+y
//                        +  '.jpg)"><a href="./static/photos/'
//                        + expandedm+expandedi+y
//                        + '.jpg" data-lightbox="' + m + '" data-title="">' // data-lightbox would put images from the same month in the same group
//                        + i
//                        + '</a></td>';
            // use below to load diary
            if(UrlExists('./static/diary/' + expandedm+expandedi+y + '.json')){
                html += '<td class="filled_date" onclick="showDiary(\''
                 +  expandedm + expandedi + y
                 + '\')"><a>' + i + '</a></td>';
            }
            else{
//                html += '<td class="empty_date" onclick="showUpload(\''
//                 + y + '-' + expandedm + '-' + expandedi
//                 + '\')"><a>' + i + '</a></td>';
                html += '<td class="empty_date" onclick="showEditDiary(\''
                 + expandedm + expandedi + y
                 + '\')"><a>' + i + '</a></td>';
            }
        }
        // If Saturday, closes the row
        if ( dow == 6 ) {
            html += '</tr>';
        }
        // If not Saturday, but last day of the selected month
        // it will write the next few days from the next month
        else if ( i == lastDateOfMonth ) {
            var k=1;
            for(dow; dow < 6; dow++) {
                html += '<td class="not-current">' + k + '</td>';
                k++;
            }
        }

        i++;
    }while(i <= lastDateOfMonth);

    // Closes table
    html += '</table>';

    // Write HTML to the div
    document.getElementById(this.divId).innerHTML = html;
};

// On Load of the window
window.onload = function() {
    // Start calendar
    var c = new Calendar("divCalendar");
    c.showCurrent();

    // Bind next and previous button clicks
    getId('btnNext').onclick = function() {
        c.nextMonth();
    };
    getId('btnPrev').onclick = function() {
        c.previousMonth();
    };
    hideCalendar();
}


