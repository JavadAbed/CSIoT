$(function() {
    $("#agentRandom").click(function() {
        $("#newNodeModal #agentName").val(Math.floor(Math.random() * 10000) + 1);
        $("#newNodeModal #agentBatch").val(Math.floor(Math.random() * 10000) + 1);
        $("#newNodeModal #agentOwner").val(Math.floor(Math.random() * 100) + 1);
        $("#newNodeModal #agentLocality").val(10* Math.floor(Math.random() * 15) + 20);
        $("#newNodeModal #agentX").val(Math.floor(Math.random() * 2000) + 1);
        $("#newNodeModal #agentY").val(Math.floor(Math.random() * 2000) + 1);
        var arr = [];
        var frNum = Math.floor(Math.random() * 10);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 100) + 1);
        }
        $("#newNodeModal #agentFriendsH").val(arr.join('-'));
        arr = [];
        var frNum = Math.floor(Math.random() * 10);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 100) + 1);
        }
        $("#newNodeModal #agentFriendsM").val(arr.join('-'));
        arr = [];
        var frNum = Math.floor(Math.random() * 10);
        for (var i = 0; i < frNum; i++) {
            arr.push(Math.floor(Math.random() * 100) + 1);
        }
        $("#newNodeModal #agentFriendsL").val(arr.join('-'));

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

    $("#simulationLogModal").on('show.bs.modal', function(e) {
        $.ajax({
            type: "GET",
            url: "/lastMessages",
            success: function(msg) {
                if (msg["status"] == 1) {
                    console.log(msg);
                    $("#messagesTable").bootstrapTable({
			data: msg.data
                    });
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
                    redrawAgents(msg.data.graph);
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
                    redrawAgents(msg.data.graph);
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
cy.on('select', 'node', function(evt) {
    selectedNode = evt.target.id();
    var tmplate = " <button type=\"button\" id=\"nodeDetails\" class=\"btn btn-secondary btn-sm\" data-id=" + selectedNode +" data-toggle=\"modal\" data-target=\"#detailNodeModal\" >Details</button>" +
		" <button type=\"button\" id=\"nodeDelete\" class=\"btn btn-danger btn-sm\" data-id=" + selectedNode +" data-toggle=\"modal\" data-target=\"#deleteNodeModal\" >Delete</button>";

    $(".footer .container").html(tmplate);
});

cy.on('unselect', 'node', function(evt) {
    $(".footer .container").html("");
});

cy.on('select', 'edge', function(evt) {
    selectedEdge = evt.target.id();
    var tmplate = " <button type=\"button\" id=\"edgeDetails\" class=\"btn btn-secondary btn-sm\" data-id=" + selectedEdge +" data-toggle=\"modal\" data-target=\"#detailEdgeModal\" >Details</button>";

    $(".footer .container").html(tmplate);
});

cy.on('unselect', 'edge', function(evt) {
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
            label: 'data(id)',
	   width: 25,
	  height: 25
        }
    },{
        selector: 'edge',
        style: {
           label: 'data(strength)',
           width: 'data(strength)'
        }
    },
      {
        selector: 'node:active',
        style: {
		"padding":  function( ele ){return ele.data('locality') -13},
            "background-opacity": 0.3,
	"background-color": "red",
          "overlay-color": "black",
	  "overlay-opacity": 0,
         "ghost": "yes"

        }
      }
    ]).update();
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




    function deleteSth(action,object,modalId){
        $.ajax({
            type: "POST",
            url: action,
            data: "id="+id,
            success: function(msg) {
                if (msg["status"] == 1) {
                    $(modalId).modal('hide');
                    redrawAgents(msg.data);
                } else {
                    alert(msg["message"]);
                }
            },
            error: function() {
                alert("failure");
            }
        });


    }

