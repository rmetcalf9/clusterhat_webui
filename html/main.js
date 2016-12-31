"use strict";

//Javascript file for client side operations for the cluster hat page

function doc_load() {
        $(document).on('click.main', "a[href$='#main_refresh']", refresh);
        $(document).on('click.main', "a[href$='#main_action_on']", action_on);
        $(document).on('click.main', "a[href$='#main_action_off']", action_off);
        $(document).on('click.main', "a[href$='#main_action_on_all']", action_on_all);
        $(document).on('click.main', "a[href$='#main_action_off_all']", action_off_all);
 
	refresh(); //run an initial refresh
}

function action_on(event) {
	var device = $(this).closest("tr").data("device");
	action(device, "on");
	event.preventDefault();
}
function action_off(event) {
        var device = $(this).closest("tr").data("device");
	action(device,"off");
	event.preventDefault();
}
function action_on_all(event) {
	action("all","on");
	event.preventDefault();
};
function action_off_all(event) {
        action("all","off");
        event.preventDefault();
};

function action(device, mode) {
	if (device=="all") {
		$("#main_postable tr").find(".command_cell").text("sent")
	} else {
		$("#main_postable tr[data-device='" + device + "']").find(".command_cell").text("sent")
	};

        var jqxhr = $.get("", {mode: mode, device: device} )
        .done(function(data) {
                //console.log(data);
		var res = "";
		if (data.resp.status=="OK") {
			res = mode + " response OK";
		} else {
			res = "Command Error " + data.resp.status;
		};
		if (device=="all") {
			$("#main_postable tr").find(".status_cell").text(res)
		} else {
			$("#main_postable tr[data-device='" + device + "']").find(".status_cell").text(res)
		};
        }, "xml")
        .fail(
                function(xhRequest, ErrorText, thrownError)  {
                        alert("Action Failed " + xhRequest + " "  + ErrorText+ " " + thrownError);
                }
        )
        ;

	//console.log("Action change " + device + " to " + mode + " todo");
};


//Called on document load and when refresh is clicked
function refresh(event) {

	var jqxhr = $.get("/get_cur_status", {} )
	.done(function(data) {
		//console.log(data);

	        $("#main_postable tr.datarow").remove();
		$.each(data.resp, 
			function(idx, obj) {
				//console.log(obj);
				var new_status = "on";
				if (obj.status.toUpperCase()=="ON") new_status="off";
				$("#main_postable tr:last").after("<tr class='datarow' data-device='" + obj.device + "'><td>" + obj.device + "</td><td>" + obj.host + "</td><td class=\"status_cell\">" + obj.status + "</td><td class=\"command_cell\"><a href=\"#main_action_" + new_status + "\">Turn " + new_status + "</a></td></tr>");
			}
		)

	}, "xml")
	.fail(
		function(xhRequest, ErrorText, thrownError)  {
			alert("Refresh Failed " + xhRequest + " "  + ErrorText+ " " + thrownError);
		}
	)
	;


	if (typeof(event) != "undefined") {
		event.preventDefault();	
	}
}

