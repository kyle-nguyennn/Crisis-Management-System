$(document).ready(function () {
    // response = $.get(
    //     "https://api.data.gov.sg/v1/environment/psi",
    //     {'api-key': 'ZGT0v1m1vG3Jj5yhLRH0Zz9Awh6TviEd'},
    //     function (data) {
    //         //$('#psi').text(data[0][0]);
    //     },
    //     json);

});
function submitNewCase() {
    console.log("Submitting new case");
    var formData = JSON.stringify($("#newCaseForm").serializeArray());
    $.ajax({
        type: "POST",
        url: "/new_case/",
        data: formData,
        success: function (data, status, xhttp) {
            alert(data);
            console.log("sumitted successfully")
        },
        dataType: "application/json",
        async: true
    });
}

$(document).ready(function () {
    console.log("out");

});
