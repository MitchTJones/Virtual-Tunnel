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
<<<<<<< Updated upstream
=======
    $('.pageTurn').click(function() {
        let tgtId = $(this).data('target'), tgt = $('#'+tgtId);
        let curId = body.data('currentpage'), cur = $('#'+curId);
        if (tgtId == curId)
            return;
        console.log('Current: ' + curId + ' | Target: ' + tgtId);
        cur.addClass('hidden');
        tgt.removeClass('hidden');
        body.data('currentpage', tgtId);
    });
    $('.tool').click(function() {
        var jq = $(this);
        if (jq.hasClass('active'))
            tool = $(this).data('tool');
        else
            tool = "none";
    });
    $(window).on('resize', function() {
        var current = map;
        var jq = $(this);
        canvas.width = jq.width();
        canvas.height = jq.height();
        drawFromPlots(current);
    });
    /*$('.savePostBtn').click(function() {
        html2canvas($(canvas), {
            onrendered: function(canvas) {
                var source = canvas.toDataURL("img/png");
                console.log(source);
                $("#newimg").attr('src', imgsrc); 
                //$("#img").show();
                var datasrc = canvas.toDataURL();
                $.ajax({
                    type: "POST",
                    url: '{{ url_for("savePost") }}',
                    data: { imgBase64: datasrc }
                }).done(function(o) { console.log("saved"); });
            }
        });
    });*/
>>>>>>> Stashed changes
});

function pick(c) {
    $('#colorPicker .control').css('color', c);
    let hex = $.fn.bcPicker.toHex(c);
    ctx.fillStyle = hex;
    ctx.strokeStyle = hex;
    $('#color').html(hex);
}