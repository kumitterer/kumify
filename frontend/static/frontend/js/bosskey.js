$(document).bind("keydown", function(e) {
    if(e.which == 66 && event.ctrlKey){
        $("#wrapper").toggle();
        return false;
    }
});