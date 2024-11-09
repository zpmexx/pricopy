$(document).ready(function () {

    function rozwMenu() {

        if ($(window).outerWidth() > 1194) {
            $('nav.side-navbar').toggleClass('shrink');
            $('.page').toggleClass('active');
        } else {
            $('nav.side-navbar').toggleClass('show-sm');
            $('.page').toggleClass('active-sm');
        }

    }

    // ------------------------------------------------------- //
    // Side Navbar Functionality
    // ------------------------------------------------------ //
    $("#main-nav").on("click", function (e) {
        e.preventDefault();
        rozwMenu();
    });
    $("#main-nav2").on("click", function (e) {
        e.preventDefault();
        rozwMenu();
    });

    $("#myInput").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $("#myTable tr").filter(function() {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
         });
    });
	
});