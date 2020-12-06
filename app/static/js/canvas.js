/* Adapted from Yusuf Sezer's javascript-canvas-painting - https://github.com/yusufsefasezer/javascript-canvas-painting */

"use strict";
var btnClear = null,
    btnSave = null,
    inputColor = null,
    inputSize = null,
    isDrawing = false,
    lineWidth = 3;

let map = [];
let currentStroke = null;

function Stroke(col, pl, w) {
    this.color = col;
    this.plots = pl;
    this.width = w;
}

function initialize() {
    btnClear = document.querySelector("#clear");
    btnSave = document.querySelector("#save");
    inputColor = document.querySelector("#color");
    inputSize = document.querySelector("#size");

    window.onmouseup = function () {
        isDrawing = false;
        if (currentStroke != null)
            map.push(new Stroke(ctx.strokeStyle, currentStroke, ctx.lineWidth));
        currentStroke = null;
        ctx.beginPath();
    };

    canvas.onmousedown = function (e) {
        isDrawing = true;
        currentStroke = [];
    };

    canvas.onmousemove = function (e) {
        if (isDrawing) {
            ctx.lineTo(e.offsetX, e.offsetY);
            ctx.lineWidth = lineWidth * 2;
            ctx.lineCap = "round";
            ctx.lineJoin = "round";
            ctx.stroke();
            ctx.beginPath();
            ctx.arc(e.offsetX, e.offsetY, lineWidth, 0, 2 * Math.PI, true);
            ctx.fill();
            ctx.beginPath();
            ctx.moveTo(e.offsetX, e.offsetY);
            currentStroke.push({x: (e.offsetX << 0), y: (e.offsetY << 0)});
        }
    };

    btnClear.onclick = function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    };

    btnSave.onclick = function () {
        canvas.toBlob(function (blob) {
            var link = document.createElement("a");
            link.download = "draw.png";
            link.href = URL.createObjectURL(blob);
            link.dispatchEvent(new MouseEvent('click'));
        }, 'image/png', 1);
    };

    inputColor.onchange = function () {
        ctx.fillStyle = this.value;
        ctx.strokeStyle = this.value;
    };

    inputSize.onchange = function () {
        lineWidth = this.value;
    };
}

function drawFromPlots(m) {
    for (var i = 0; i < m.length; i++) {
        let o = m[i];
        ctx.fillStyle = o.color;
        ctx.strokeStyle = o.color;
        let p = o.plots;
        console.log(p);
        ctx.lineWidth = o.width;
        ctx.beginPath();
        ctx.moveTo(p[0].x, p[0].y);
        for (var n = 1; n < p.length; n++) {
            let j = p[n]
            ctx.lineTo(j.x, j.y);
        }
        ctx.stroke();
    }
}

window.onload = initialize;