/* Adapted from Yusuf Sezer's javascript-canvas-painting - https://github.com/yusufsefasezer/javascript-canvas-painting */

"use strict";
var btnClear = null,
    btnSave = null,
    inputColor = null,
    inputSize = null,
    isDrawing = false,
    lineWidth = 3;

function initialize() {
    btnClear = document.querySelector("#clear");
    btnSave = document.querySelector("#save");
    inputColor = document.querySelector("#color");
    inputSize = document.querySelector("#size");

    window.onmouseup = function () {
        isDrawing = false;
        ctx.beginPath();
    };

    canvas.onmousedown = function (e) {
        isDrawing = true;
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
        }
    }

    btnClear.onclick = function () {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
    }

    btnSave.onclick = function () {
        canvas.toBlob(function (blob) {
            var link = document.createElement("a");
            link.download = "draw.png";
            link.href = URL.createObjectURL(blob);
            link.dispatchEvent(new MouseEvent('click'));
        }, 'image/png', 1);
    }

    inputColor.onchange = function () {
        ctx.fillStyle = this.value;
        ctx.strokeStyle = this.value;
    }

    inputSize.onchange = function () {
        lineWidth = this.value;
    }
}

window.onload = initialize;