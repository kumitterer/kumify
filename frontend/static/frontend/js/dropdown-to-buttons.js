var selectName = $('.dtb').attr('name');

// add a hidden element with the same name as the select
var hidden = $('<input type="hidden" name="' + selectName + '">');
hidden.val($('.dtb').val());
hidden.insertAfter($('.dtb'));

var checked = false;

$(".dtb option").unwrap().each(function() {
    var btn = $('<div data-style="background-color: ' + $(this).attr("data-color") + ' !important; border-color: ' + $(this).attr("data-color") + ' !important;" data-value="' + $(this).attr("value") + '" class="dtb-btn btn-secondary"><i class="' + $(this).attr("data-icon") + '"></i> ' + $(this).text() + '</div>');
    if($(this).is(':checked') && !checked) { 
        btn.removeClass("btn-secondary"); 
        btn.addClass('btn-primary'); 
        checked = true;
    };
    $(this).replaceWith(btn);
});

$(document).on('click', '.dtb-btn', function() {
    $('.dtb-btn').removeClass('btn-primary');
    $('.dtb-btn').addClass('btn-secondary');
    $('.dtb-btn').attr('style', "");
    $(this).removeClass('btn-secondary');
    $(this).addClass('btn-primary');
    $(this).attr('style', $(this).attr('data-style'));
    $('input[name="'+selectName+'"]').val($(this).attr("data-value"));
});