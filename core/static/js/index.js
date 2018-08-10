$(function() {
    $("#agentRandom").click(function() {
        $("#agentName").val(Math.floor(Math.random() * 10000) + 1);
        $("#agentBatch").val(Math.floor(Math.random() * 10000) + 1);
        $("#agentOwner").val(Math.floor(Math.random() * 100) + 1);
        $("#agentLocality").val(10* Math.floor(Math.random() * 15) + 20);
        $("#agentX").val(Math.floor(Math.random() * 2000) + 1);
        $("#agentY").val(Math.floor(Math.random() * 2000) + 1);
        var arr = [];
        var frNum = Math.floor(Math.random() * 10);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 100) + 1);
        }
        $("#agentFriendsH").val(arr.join('-'));
        arr = [];
        var frNum = Math.floor(Math.random() * 10);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 100) + 1);
        }
        $("#agentFriendsM").val(arr.join('-'));
        arr = [];
        var frNum = Math.floor(Math.random() * 10);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 100) + 1);
        }
        $("#agentFriendsL").val(arr.join('-'));

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
            processData: false,
            contentType: false,
            cache: false,
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


    $("button#deleteAll").click(function() {
        $.ajax({
            type: "POST",
            url: "/deleteAll",
            data: "",
            success: function(msg) {
                if (msg["status"] == 1) {
                    $('#clearModal').modal('hide'); 
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

    $("#simulation1Step").click(function() {
        $.ajax({
            type: "POST",
            url: "/startSimulation",
            data: "numberOfSteps=1",
            success: function(msg) {
                if (msg["status"] == 1) {
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

    $("button#btnStartSimulation").click(function() {
        $.ajax({
            type: "POST",
            url: "/startSimulation",
            data: $('#formStartSimulation').serialize(),
            success: function(msg) {
                if (msg["status"] == 1) {
                    $('#simulationModal').modal('hide');
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

    $("#simulationLogModal").on('shown.bs.modal', function() {
	console.log("logs opened");
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
    container: document.getElementById('cy'),
    minZoom: 0.01,
    maxZoom: 200
});

initCy();
var selectedNode = "";
var selectedEdge = "";

cy.on('select', 'node', function(evt) {
    selectedNode = evt.target.id();
    var tmplate = " <button type=\"button\" id=\"nodeDetails\" class=\"btn btn-secondary btn-sm\">Details</button>" +
		" <button type=\"button\" id=\"nodeDelete\" class=\"btn btn-danger btn-sm\">Delete</button>";

    $(".footer .container").html(tmplate);
    $("#nodeDetails").click(function(){
         $('#detailNodeModal').modal('show');
    });
    $("#nodeDelete").click(function(){
         $('#deleteNodeModal').modal('show');
    });
});

cy.on('unselect', 'node', function(evt) {
    selectedNode = "";
    $("#nodeDetails").unbind( "click" );
    $("#nodeDelete").unbind( "click" );
    $(".footer .container").html("");
});

cy.on('select', 'edge', function(evt) {
    selectedEdge = evt.target.id();
    var tmplate = " <button type=\"button\" id=\"edgeDetails\" class=\"btn btn-secondary btn-sm\">Details</button>";

    $(".footer .container").html(tmplate);
    $("#edgeDetails").click(function(){
         $('#detailEdgeModal').modal('show');
    });
});

cy.on('unselect', 'edge', function(evt) {
    selectedEdge = "";
    $("#edgeDetails").unbind( "click" );
    $(".footer .container").html("");
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
            shape: 'ellipse',
            label: 'data(id)'
        }
    },{
        selector: 'edge',
        style: {
           label: 'data(strength)',
           width: 'data(strength)'
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

