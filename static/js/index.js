$(document).ready(function(){
	var result;
    $("button").click(function(){
        $('#bt').attr("disabled", true);
        var id = $('.getId').text();
        $.ajax({
            url: "/draws"+id+"/enrollments/add",
            type: "GET",
            dataType:'application/json',
            success: function(result, status, xhr) {
                console.log(result);
                console.log(status);
                var val = $("#btp").text();
                if(val === "enroll")
                    document.getElementById("demo").innerHTML = "unenroll";
                else
                    document.getElementById("demo").innerHTML = "enroll";
                $('#demo').attr("disabled", false);
                $("#displaySu").html("Succes");
            },
            error: function(xhr, status, error) {
                console.log(status);
                
                $("#displayEr").html("error");
            } 
        });
    });
});
