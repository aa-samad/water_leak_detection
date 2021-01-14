// --- variables ---
var interval_setting;
var corr;
var time_not_freq = true;


// --- init codes ---
$( document ).ready(function()
{
    interval_setting = setInterval(update_status, 5000);
    corr = false;
    update_status();
});


// --- functions ---

function update_status()
{
    if (interval_setting)
    {
        // get pipe material
        $.ajax({
            url: '/status',
            type: "POST",
            data: { 'field': 'setting' },
            success: function(response_total) {
                if ('mat' in response_total) {
                    response = response_total['mat'];
                    if (response === 'steel') {
                        $('input#material1')[0].checked = true;
                    }
                    else if (response === 'lead') {
                        $('input#material2')[0].checked = true;
                    }
                    else if (response === 'cast_iron') {
                        $('input#material3')[0].checked = true;
                    }
                    else if (response === 'iron') {
                        $('input#material4')[0].checked = true;
                    }
                    else if (response === 'pvc') {
                        $('input#material5')[0].checked = true;
                    }
                    else if (response === 'unknown') {
                        $('input#material6')[0].checked = true;
                    }
                    else {
                        console.log("wrong material!");
                    }
                }
                if ('dia' in response_total) {
                    response = response_total['dia'];
                    $("#diameter")[0].placeholder = response;
                    $("label[for='diameter']").addClass("active");
                }
                if ('vel_type' in response_total) {
                    response = response_total['vel_type'];
                    if (response === 'auto')
                    {
                        $('input#vel1')[0].checked = true;
                    }
                    else if (response === 'manual')
                    {
                        $('input#vel2')[0].checked = true;
                    }
                    else
                    {
                        console.log("wrong velocity mode!");
                    }
                }
                if ('vel' in response_total) {
                    response = response_total['vel'];
                    $("#vel_num")[0].placeholder = response;
                    $("label[for='vel_num']").addClass("active");
                }

                if ('len' in response_total) {
                    response = response_total['len'];
                    $("#len")[0].placeholder = response;
                    $("label[for='len']").addClass("active");
                }
            },
            error: function(){
                toastr.error("connection to device is lost");
            }
        });
    }
    if (corr)
    {
        // update image
        var newImage = $('img#corr_pic')[0];
        if (time_not_freq)
        {
            newImage.src = "static/img/corr.png#" + new Date().getTime();
        }
        else
        {
            newImage.src = "static/img/spect.png#" + new Date().getTime();
        }
        // leak status
        $.ajax({
            url: '/status',
            type: "POST",
            data: { 'field': 'leak' },
            success: function(response_total) {
                if ('leak_exist' in response_total)
                {
                    response = response_total['leak_exist'];
                    var tag0 = $("#leak_exist");
                    if (response === "YES")
                    {
                        tag0.addClass('red-text');
                        tag0.removeClass('green-text');
                        $("#leak_exist").html(response);
                    }
                    else if (response === "NO")
                    {
                        tag0.addClass('green-text');
                        tag0.removeClass('red-text');
                        $("#leak_exist").html(response);
                    }
                    else
                    {
                        toastr.error(response);
                        $("#leak_exist").html("-");
                    }
                }
                if ('sen1_dist' in response_total)
                {
                    response = response_total['sen1_dist'];
                    $("#sen1_dist").html(response);
                }
                if ('sen2_dist' in response_total)
                {
                    response = response_total['sen2_dist'];
                    $("#sen2_dist").html(response);
                }
            },
            error: function(){
                $("#sen2_dist").html("-");
                $("#sen1_dist").html("0");
                $("#leak_exist").html("0");
                toastr.error("connection to device is lost");
            }
        });
    }
}

function command(text0)
{
    if (text0 === 'corr')
    {
        /// --- material config ---
        var materials = $('input.group1');
        var mat_names = ["steel", "lead", "cast_iron", "iron", "pvc", "unknown"];
        var mat;
        var mat_name;
        for (var i = 0; i < materials.length; i++){
           mat = materials[i].checked;
           if (mat === true)
           {
               mat_name = mat_names[i];
           }
        }
        /// --- diameter config ---
        var dia = $('input#diameter')[0].value;
        /// --- velocity config ---
        var vel_type = "auto";
        var vel = 0;
        var vel1 = $('input#vel1')[0].checked;
        if (vel1 === false) // it is on auto
        {
            vel_type = "manual";
            vel = $('input#vel_num')[0].value;
        }
        /// --- length config ---
        var len = $('input#len')[0].value;

        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'corr',
                    'mat': mat_name,
                    'dia': dia,
                    'vel_type': vel_type,
                    'vel': vel,
                    'len': len
                    },
            success: function(response)
            {
                console.log(response);
                if (response === "Done!")
                {
                    toastr.success("Started!");
                    tags = $(".stopped");
                    tags.removeClass("stopped");
                    tags.addClass("started");
                }
                else
                {
                    toastr.error(response);
                }
            }
        });
        $("#overall_status").html("Sampling & Correlation");
        corr = true;
    }
    else if (text0 === 'stop')
    {
        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'stop_corr' },
            success: function(response) {
                console.log(response);
                if (response === "Done!")
                {
                    toastr.success(response);
                    tags = $(".started");
                    tags.addClass("stopped");
                    tags.removeClass("started");
                }
                else
                {
                    toastr.error(response);
                }
            },
            error: function()
            {
                toastr.error("ERROR: No connection!");
            }
        });
        corr = false;
        $("#overall_status").html("Idle");
    }
    else if (text0 === 'reset')
    {
        $.ajax({
            url: '/command',
            type: "POST",
            data: { 'command': 'reset' },
            success: function(response) {
                console.log(response);
                if (response === "Done!")
                {
                    toastr.info("Device will reset in 5 sec ...");
                    $("#overall_status").html("Idle");
                    corr = false;
                    tags = $(".started");
                    tags.addClass("stopped");
                    tags.removeClass("started");
                }
                else
                {
                    toastr.error(response);
                }
            },
            error: function()
            {
                toastr.error("ERROR: No connection!");
            }
        });
    }
    else if (text0 === 'switch')
    {
        var newImage = $('img#corr_pic')[0];
        if (time_not_freq)
        {
            time_not_freq = false;
            newImage.src = "static/img/spect.png#" + new Date().getTime();
        }
        else
        {
            time_not_freq = true;
            newImage.src = "static/img/corr.png#" + new Date().getTime();
        }
    }
}
