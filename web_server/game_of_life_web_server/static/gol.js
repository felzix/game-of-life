var boardState = null;
var lastBoardIteration = -1;
var lastBoardUpdateMS = Date.now() - 2000;
var lastDrawTimeMS = lastBoardUpdateMS;


function updateBoardState() {
    $.ajax({
        url: "/gol/state",
        success: function (result) {
            console.log(result);
            // If result iteration is > than last seen iteration then the board state has updated.
            // If the result iteration is < the last seen iteration then the board state has reset.
            if (result["iteration"] != lastBoardIteration) {
                lastBoardIteration = result["iteration"];
                boardState = result["tiles"];
                lastBoardUpdateMS = Date.now();
            }
        }
    })
}


function drawTile(canvas, tile_size, x, y, state) {
    context = canvas.getContext("2d");
    var x_ = x * tile_size;
    var y_ = y * tile_size;
    if (state) {
        context.fillStyle = "#000000";
    } else {
        context.fillStyle = "#FFFFFF";
    }

    context.fillRect(x_, y_, x_ + tile_size, y_ + tile_size);
}


function drawBoard(width, height, tile_size) {
    if (boardState == null) {
        return;
    }
    if (lastBoardUpdateMS > lastDrawTimeMS) {
        var canvas = document.getElementById("gol_canvas");
        for (y = 0; y < height; y++) {
            for (x = 0; x < width; x++) {
                var state = boardState[y][x];
                drawTile(canvas, tile_size, x, y, state);
            }
        }
        lastDrawTimeMS = Date.now();
    }
}


function getMousePos(event) {
    var canvas = document.getElementById("gol_canvas");
    var rect = canvas.getBoundingClientRect();
    return {
      x: event.clientX - rect.left,
      y: event.clientY - rect.top
    };
}


function toggleTile(event, tile_size) {
    var pos = getMousePos(event);
    var x = Math.floor(pos.x / tile_size);
    var y = Math.floor(pos.y / tile_size);
    if (boardState[y][x]) {
        $.ajax({
            url: "/gol/state?x="+x+"&y="+y, // jquery mistakenly believes DELETE doesn't do params
            type: "DELETE",
            success: function () {
                updateBoardState();
            }
        })
    } else {
        $.ajax({
            url: "/gol/state",
            type: "PUT",
            data: {"x": x,
                   "y": y},
            success: function () {
                updateBoardState();
            }
        })
    }
}


function startGol() {
    $.ajax({
        url: "/gol/running",
        type: "PUT",
        data: {"new_running_state": "True"},
        success: function () {}
    })
}


function stopGol() {
    $.ajax({
        url: "/gol/running",
        type: "PUT",
        data: {"new_running_state": "False"},  //note that "False" is just a string != "True"
        success: function () {}
    })
}
