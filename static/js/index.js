$(document).ready(function(){

    $("button").click(function(){
        $('#bt').attr("disabled", true);
        var id = $('.getId').text();
        var val = $("#btp").text();
        var disition = "";
        if(val === "Enroll"){
            disition = "add";
        }
        else{
            disition ="remove";
        }
        $.ajax({
            type: "GET",
            url: "/draws/"+id+"/enrollments/"+disition,
            success: function(data) {
                console.log(data);
                $('#bt').attr("disabled", false);
                if(disition === "add"){
                    $("#btp").html("<button id =\"bt\" class = \"btn btn-outline-success\">Unenroll</button>");
                }
                else{
                    $("#btp").html("<button id=\"bt\" class = \"btn btn-outline-success\">Enroll</button>");
                }
                var h1 = document.getElementById("hidden1");
                h1.style.display = 'block' ;
            },
            error: function(status) {
                console.log(status);
                var h2 = document.getElementById("hidden2");
                h2.style.display = 'block' ;
            }, 
        });
    });
 });


// $.ajax({
//     type:"GET",
//     url:"https://api.meetup.com/2/cities",
//     success: function(data) {
//       $('.text').text(JSON.stringify(data));
//     },
//     dataType: 'jsonp',
//   });

// $('#bt').attr("disabled", true);
        // $.ajax({
        //     type:"GET",
        //     url:"https://api.meetup.com/2/cities",
        //     success: function(data) {
        //         $("#displaySu").html("Succes");
        //         console.log(data);
        //         $('#demo').attr("disabled", false);
        //     },
        //     dataType: 'jsonp',
        //     error: function(){
        //         console.log("error");
        //         $('#demo').attr("disabled", false);
        //     }