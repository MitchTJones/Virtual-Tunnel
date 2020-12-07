let canvas, ctx;
canvas = document.querySelector("#canvas");
let canvasDims = canvas.parentElement.getBoundingClientRect();
canvas.width = canvasDims.width;
canvas.height = canvasDims.height;
ctx = canvas.getContext("2d");
let view = false;
$(document).ready(() => {
    let body = $('.body');
    let accountButton = $('#accountButton');
    let sidebar = $('.sidebar');
    let sidebarClose = $('#sidebarClose');
    let sidebarError = $('.sidebarError');
    let sidebarFlash = $('.sidebarFlash');
    accountButton.click(function() {toggleSidebar(sidebar)});
    sidebarClose.click(function() {toggleSidebar(sidebar)});
    if(sidebarError.children().length > 0 || sidebarFlash.children().length > 0)
        sidebar.addClass('open');
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
    $('#strokePicker').click(function() {
        lineWidth = $(this).val()/5;
    });
    $('.toggle').click(function() {
        var jq = $(this);
        if (jq.hasClass('active'))
            jq.removeClass('active');
        else
            jq.addClass('active');
    });
    $('.pageTurn').click(function() {
        let tgtId = $(this).data('target'), tgt = $('#'+tgtId);
        let curId = body.data('currentpage'), cur = $('#'+curId);
        if (tgtId == curId)
            return;
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
    $('.modalButton').click(function() {
        var jq = $(this), tgt = $('#'+jq.data('target'));
        tgt.removeClass('hidden');
    });
    $('#showInfo').click(function() {
        var jq = $(this);
        $(view ? '#viewInfo' : '#enterInfo').removeClass('hidden');
    });
    $('.modal').click(function(e) {
        if(e.target !== e.currentTarget) return;
        $(this).addClass('hidden').children().click(function(e) { return false; });
    });
    $('.closeParents').click(function() {
        $(this).parents('.modal').addClass('hidden');
    });
    $('.org').click(function() {
        var jq = $(this);
        if (jq.hasClass('active')) {
            jq.removeClass('active');
            return;
        }
        $('.org').removeClass('active');
        jq.addClass('active');
        $('#org').val('');
    });
    $(window).on('resize', function() {
        var jq = $(this);
        canvas.width = jq.width();
        canvas.height = jq.height();
    });
});

function toggleSidebar(sidebar) {
    sidebar.animate({width:'toggle'},500);
    if (sidebar.hasClass('open'))
        sidebar.removeClass('open');
    else
        sidebar.addClass('open');
}

function pick(c) {
    $('#colorPicker .control').css('color', c);
    let hex = $.fn.bcPicker.toHex(c);
    ctx.fillStyle = hex;
    ctx.strokeStyle = hex;
    $('#color').html(hex);
}