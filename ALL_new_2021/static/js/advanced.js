// --- init codes ---
$( document ).ready(function() {
    interval_gateway_stat = setInterval(update_status, 10000);
    update_status();
});


// ---------------- command buttons functions ----------------------
function commands(command){
    $.ajax({
        url: '/command',
        type: "POST",
        data: { 'command': command },
        success: function(response) {
            if (response === "Done!")
            {
                toastr.success(response);
            }
            else
            {
                toastr.error(response);
            }
        },
        error: function(){
                toastr.error("ERROR: No connection!");
            }
    });
}


// ------------------- status button function  ---------------------
function status(command){
    $.ajax({
        url: '/status',
        type: "POST",
        data: { 'field': command },
        success: function(response) {
            if (response === "Active")
            {
                toastr.success(response);
            }
            else
            {
                toastr.warning(response);
            }
        },
        error: function(){
                toastr.error("ERROR: No connection!");
            }
    });
}


// ------------------ update dashboard fields ----------------------
function update_status(){
    $.ajax({
            url: '/status',
            type: "POST",
            data: { 'field': 'sms_number' },
            success: function(response) {
                $("#sms_number")[0].placeholder = response;
            },
            error: function(){
                $("#sms_number")[0].placeholder = '09120000000';
            }
        });
    $.ajax({
            url: '/status',
            type: "POST",
            data: { 'field': 'sim_apn' },
            success: function(response) {
                $("#sim_apn")[0].placeholder = response;
            },
            error: function(){
                $("#sim_apn")[0].placeholder = 'mtn...';
            }
        });
    $.ajax({
            url: '/status',
            type: "POST",
            data: { 'field': 'lte_module' },
            success: function(response) {
                if (response === "0")
                {
                    $('input#module1')[0].checked = true;
                    $('input#module2')[0].checked = false;
                }
                else
                {
                    $('input#module1')[0].checked = false;
                    $('input#module2')[0].checked = true;
                }
            },
            error: function(){
                toastr.error("ERROR: No connection to the board!");
            }
        });
    $.ajax({
            url: '/status',
            type: "POST",
            data: { 'field': 'ssh_tunnel_ip' },
            success: function(response) {
                $("#ssh_tunnel_ip")[0].placeholder = response;
            },
            error: function(){
                $("#ssh_tunnel_ip")[0].placeholder = '0.0.0.0';
            }
        });
    $.ajax({
            url: '/status',
            type: "POST",
            data: { 'field': 'ssh_tunnel_server_side_dash_port' },
            success: function(response) {
                $("#ssh_tunnel_server_side_dash_port")[0].placeholder = response;
            },
            error: function(){
                $("#ssh_tunnel_server_side_dash_port")[0].placeholder = 80;
            }
        });

    $.ajax({
        url: '/status',
        type: "POST",
        data: { 'field': 'ssh_tunnel_server_side_ssh_port' },
        success: function(response) {
            $("#ssh_tunnel_server_side_ssh_port")[0].placeholder = response;
        },
        error: function(){
            $("#ssh_tunnel_server_side_ssh_port")[0].placeholder = 80;
        }
    });

    $.ajax({
            url: '/status',
            type: "POST",
            data: { 'field': 'ssh_tunnel_port' },
            success: function(response) {
                $("#ssh_tunnel_port")[0].placeholder = response;
            },
            error: function(){
                $("#ssh_tunnel_port")[0].placeholder = 0;
            }
        });
}



//  --------------- send LTE data -----------------------
function lte(){
    var num = $('input#sms_number')[0].value;
    var apn0 = $('input#sim_apn')[0].value;
    // gobi or quectel module select
    var check1 = $('input#module1')[0].checked;
    var check2 = $('input#module2')[0].checked;
    if (num === "")
    {

    }
    else
    {
        $.ajax({
        url: '/command',
        type: "POST",
        data: { 'command': 'sms_number', 
                'num': num },
        success: function(response) {
            if (response === "Done!")
            {
                toastr.success(response);
            }
            else
            {
                toastr.error(response);
            }
        },
        error: function(){
                toastr.error("ERROR: No connection!");
            }
    });
    }
    if (apn0 === "")
    {
        
    }
    else
    {
        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'sim_apn', 
                    'apn': apn0 },
            success: function(response) {
                if (response === "Done!")
                {
                    toastr.success(response);
                }
                else
                {
                    toastr.error(response);
                }
            },
            error: function(){
                    toastr.error("ERROR: No connection!");
                }
        });
    }
    if (check1 === true)
    {
        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'lte_module',
                    'module': '0'},
            success: function(response) {
                    toastr.success(response);
            },
            error: function(){
                    toastr.error("ERROR: No connection!");
            }
        });
    }
    else
    {
        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'lte_module',
                    'module': '1'}, 
            success: function(response) {
                    toastr.success(response);
            },
            error: function(){
                    toastr.error("ERROR: No connection!");
            }
        });
    }


}



// --------------- ssh tunnel setting save -----------------
function ssh_tunnel_save(){
    var ssh_tunnel_ip = $('input#ssh_tunnel_ip')[0].value;
    var ssh_tunnel_server_side_dash_port = $('input#ssh_tunnel_server_side_dash_port')[0].value;
    var ssh_tunnel_server_side_ssh_port = $('input#ssh_tunnel_server_side_ssh_port')[0].value;
    var ssh_tunnel_port = $('input#ssh_tunnel_port')[0].value;
    if (ssh_tunnel_ip === "")
    {

    }
    else
    {
        $.ajax({
        url: '/command',
        type: "POST",
        data: { 'command': 'ssh_tunnel_ip', 
                'ip': ssh_tunnel_ip },
        success: function(response) {
            if (response === "Done!")
            {
                toastr.success(response);
            }
            else
            {
                toastr.error(response);
            }
        },
        error: function(){
                toastr.error("ERROR: No connection!");
            }
    });
    }
    if (ssh_tunnel_server_side_dash_port === "")
    {
        
    }
    else
    {
        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'ssh_tunnel_server_side_dash_port', 
                    'port': ssh_tunnel_server_side_dash_port },
            success: function(response) {
                if (response === "Done!")
                {
                    toastr.success(response);
                }
                else
                {
                    toastr.error(response);
                }
            },
            error: function(){
                    toastr.error("ERROR: No connection!");
                }
        });
    }
    if (ssh_tunnel_server_side_ssh_port === "")
    {
        
    }
    else
    {
        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'ssh_tunnel_server_side_ssh_port', 
                    'port': ssh_tunnel_server_side_ssh_port },
            success: function(response) {
                if (response === "Done!")
                {
                    toastr.success(response);
                }
                else
                {
                    toastr.error(response);
                }
            },
            error: function(){
                    toastr.error("ERROR: No connection!");
                }
        });
    }
    if (ssh_tunnel_port === "")
    {
        
    }
    else
    {
        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'ssh_tunnel_port',
                    'port': ssh_tunnel_port}, 
            success: function(response) {
                    toastr.success(response);
            },
            error: function(){
                    toastr.error("ERROR: No connection!");
            }
        });
    }
}

function upload_firmware()
{
    var form_data = new FormData($('form#uploadform')[0]);
    $.ajax({
      type: 'POST',
      url: '/uploadajax',
      data: form_data,
      contentType: false,
      processData: false,
      dataType: 'json'
    }).done(function(data, textStatus, jqXHR){
      console.log(data);
      console.log(textStatus);
      console.log(jqXHR);
      console.log('Success!');
    }).fail(function(data){
      alert('error!');
      });
}