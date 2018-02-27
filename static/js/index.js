$(document).ready(function(){

    $("button").click(function(){

        var val = $(this).val();
        var id = $( "button" ).index( this );

        $('#bt'+id).attr("disabled", true);

        var disition = "";
        if(val == "Enroll"){
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
                $('#bt'+id).attr("disabled", false);
                if(disition === "add"){
                    $("#btp"+id)
                        .html("<button id =\"bt\" class = \"btn btn-outline-success\" value = \"Unenroll\">Unenroll</button>");
                }
                else{
                    $("#btp"+id)
                        .html("<button id=\"bt\" class = \"btn btn-outline-success\" value = \"Enroll\">Enroll</button>");
                }

                var h1 = document.getElementById("hidden1");
                h1.style.display = 'block' ;

            },
            error: function(status) {

                var h2 = document.getElementById("hidden2");
                h2.style.display = 'block' ;

            }, 
        });
    });
 });
