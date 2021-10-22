var openSidenav = false;

$(document).ready(function() {
    $("#menu-btn").click(openNav);
    $(".closebtn").click(closeNav);
    
    $('html').click(function (e) {
        if (openSidenav && !$(e.target).is('#mySidenav')) {
            closeNav()
        } 
    });
});

function openNav(e) {
    document.getElementById("mySidenav").style.width = "250px";
    openSidenav = true;
    e.stopPropagation()
}

function closeNav() {
    document.getElementById("mySidenav").style.width = "0";
    openSidenav = false;
}
