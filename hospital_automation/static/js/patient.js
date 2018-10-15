function receive_patient() {
    $.get('api/receive_incoming_patient', function (data) {
        var i;
        for (var patient in data){
            var patient_id = data[patient]["id"];
            var name = data[patient]["first_name"];
            var lname = data[patient]["last_name"];
            var para = document.createElement("h2");
            var node = document.createTextNode(name);
            para.appendChild(node);
            var element = document.getElementById("patient_name");
            element.appendChild(para);

        }
    })
}