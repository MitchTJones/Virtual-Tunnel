let canvas, ctx;

$(document).ready(() => {
    canvas = document.querySelector("#canvas");
    let canvasDims = canvas.parentElement.getBoundingClientRect();
    canvas.width = canvasDims.width;
    canvas.height = canvasDims.height;
    ctx = canvas.getContext("2d");
    let bc = $('#colorPicker');
    bc.bcPicker();
    pick('rgb(0,0,0)');
    $('body').on('click', '.bcPicker-picker', () => {
        bc.toggleColorPalette($(this));
    });
    $('.bcPicker-color').click(function() {
        var jq = $(this);
        pick(jq.css('background-color'));
        jq.parent().toggle('fast');
    });
    $('.toggle').click(function() {
        var jq = $(this);
        if (jq.hasClass('active'))
            jq.removeClass('active');
        else
            jq.addClass('active');
    });
});

function pick(c) {
    $('#colorPicker .control').css('color', c);
    let hex = $.fn.bcPicker.toHex(c);
    ctx.fillStyle = hex;
    ctx.strokeStyle = hex;
    $('#color').html(hex);
}