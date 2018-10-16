function receive_patient() {
    $.get('api/receive_incoming_patient', function (data) {
        console.log(data)
        for (var patient in data){
            var patient_id = data[patient]["id"];
            var name = data[patient]["first_name"];
            var lname = data[patient]["last_name"];
            current_html = $('#board').html();
            var para = document.createElement("div");
            $(para).append('<a href="/doctor/'+ patient_id +'"><div class="card-container" id="'+patient_id+'"><div class="card">'+ name + " " + lname + '</div></div></a>');
            current_html += $(para).html();
            $('#board').html(current_html);
        }
    })
}