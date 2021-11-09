// Empty JS for your own code to be here
function myFunc(vars) {
    url = '/api/device/'+vars;
    return url
}

function repeatedly_get(){
    fetch_from_server();
    setTimeout(repeatedly_get, 5000);
}

function fetch_from_server(){
    var req = new XMLHttpRequest();
    req.open('GET', urls);
    req.onreadystatechange = function () {
        if (req.readyState === 4) {
//        console.log(req.responseText);
        process_data(req.responseText);
        }
    };
    req.send();
}
function process_data(v){
    var data = JSON.parse(v);
    document.getElementById('Hostname').innerHTML = data["Hostname"];
    document.getElementById('Uptime').innerHTML = data["Uptime"]+" hrs";
    var interfaces = data["interfaces"];
    var cnt = 1;

    for ( let x in interfaces){
        interface = data["interfaces"][x];
        document.getElementById('interface_name_'+cnt).innerHTML = interface["interface_name"];
        if (interface["interface_status"] == 1){
            document.getElementById('interface_status_'+cnt).style.backgroundColor = "green" ;
        } 
        else {
            document.getElementById('interface_status_'+cnt).style.backgroundColor = "red" ;
        }
        
        document.getElementById('interface_speed_'+cnt).innerHTML = interface["interface_speed"]/1000000 + "M";
        document.getElementById('in_byte_'+cnt).innerHTML = interface["in_byte"];
        document.getElementById('out_byte_'+cnt).innerHTML = interface["out_byte"];
        document.getElementById('in_packet_'+cnt).innerHTML = interface["in_packet"];
        document.getElementById('out_packet_'+cnt).innerHTML = interface["out_packet"];
        cnt += 1;
    }
}

