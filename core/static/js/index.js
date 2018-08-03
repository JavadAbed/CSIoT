$(function() {
    $("#agentRandom").click(function() {
        $("#agentName").val(Math.floor(Math.random() * 10000) + 1);
        $("#agentBatch").val(Math.floor(Math.random() * 100) + 1);
        $("#agentOwner").val(Math.floor(Math.random() * 20) + 1);
        $("#agentFamily").val(Math.floor(Math.random() * 10) + 1);
        $("#agentX").val(Math.random().toFixed(6));
        $("#agentY").val(Math.random().toFixed(6));
        var arr = [];
        var frNum = Math.floor(Math.random() * 5);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 20) + 1);
        }
        $("#agentFriends").val(arr.join('-'));
        arr = [];
        var frNum = Math.floor(Math.random() * 5);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 20) + 1);
        }
        $("#agentNeeds").val(arr.join('-'));
        arr = [];
        var frNum = Math.floor(Math.random() * 5);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 20) + 1);
        }
        $("#agentNeeds").val(arr.join('-'));
        arr = [];
        var frNum = Math.floor(Math.random() * 5);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 20) + 1);
        }
        $("#agentOffers").val(arr.join('-'));



    });

    $("button#agentNewSubmit").click(function() {
        $.ajax({
            type: "POST",
            url: "/newAgent",
            data: $('#newAgent').serialize(),
            success: function(msg) {
                if (msg["status"] == 1) {
                    console.log(msg);
                    // update graph
                    $('#newAgent')[0].reset();
                    $('#newNodeModal').modal('hide');
                    redrawAgents(msg.data);
                } else {
                    alert(msg["message"]);
                }
            },
            error: function() {
                alert("failure");
            }
        });
    });

    $("#agentUploadSubmit").click(function() {
        var updata = new FormData();
        updata.append('file', $('#fileCSV')[0].files[0]);
        $.ajax({
            type: "POST",
            url: "/uploadAgent",
            data: updata,
            success: function(msg) {
                if (msg["status"] == 1) {
                    console.log(msg);
                    // update graph
                    $('#newAgent')[0].reset();
                    $('#newNodeModal').modal('hide');
                } else {
                    alert(msg["message"]);
                }
            },
            error: function() {
                alert("failure");
            }
        });
    });


    $("#refreshGraph").click(function() {
        initCy();
    });

    $("#layoutGraphCircle").click(function() {
        curr_layout = "circle";
        redrawAgentsCache();
    });

    $("#layoutGraphPredef").click(function() {
        curr_layout = "preset";
        initCy();

    });

    $("#layoutGraphGrid").click(function() {
        curr_layout = "grid";
        redrawAgentsCache();
    });
    $("#layoutGraphRandom").click(function() {
        curr_layout = "random";
        redrawAgentsCache();
    });




});
var curr_layout = "preset";
var cy = window.cy = cytoscape({
    container: document.getElementById('cy')
});

initCy();

cy.on('tap', 'node', function(evt) {
    console.log('tap ' + evt.target.id());
    evt.target.connectedEdges().style({
        'line-color': 'black'
    });
});


function redrawAgentsCache() {
    redrawAgents(cy.elements());
}

function redrawAgents(newNodes) {
    cy.elements().remove();
    cy.add(newNodes);
    var layout = cy.layout({
        name: curr_layout
    });
    layout.run();
    cy.style().fromJson([{
        selector: 'node',
        style: {
            shape: 'data(shape)',
            label: 'data(agentName)'
        }
    }]).update();
}

function initCy() {

    $.ajax({
        url: '/agents',
        type: 'GET',
        dataType: 'json',
        success: function(msg) {
            if (msg["status"] == 1) {
                console.log(msg);
                // update graph
                redrawAgents(msg.data)

            } else {
                alert(msg["message"]);
            }
        },
        error: function() {
            alert("failure");
        }
    });
}

