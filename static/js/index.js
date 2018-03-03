$(document).ready(function () {

    $("td").on('click', '.enroll', function (e) {
        var b = $(this);
        b.prop("disabled", true);
        $.ajax({
            type: "GET",
            url: "/projects/" + b.attr("project_id") + "/enrollments/add",
            success: function (data) {

                console.log(data);
                b.attr("disabled", false);

                b.removeClass("enroll");
                b.removeClass("btn-primary");
                b.addClass("unenroll");
                b.addClass("btn-warning");

                b.text('Unenroll');

            },
            error: function (status) {
                var h2 = document.getElementById("hidden2");
                h2.style.display = 'block';
                console.log("Error in enrolling " + b.attr("project_id") + "-" + status.status);
            }
        });
    });

    $("td").on('click', '.unenroll', function (e) {
        var b = $(this);
        b.prop("disabled", true);
        $.ajax({
            type: "GET",
            url: "/projects/" + b.attr("project_id") + "/enrollments/remove",
            success: function (data) {

                console.log(data);
                b.attr("disabled", false);

                b.removeClass("unenroll");
                b.removeClass("btn-warning");
                b.addClass("enroll");
                b.addClass("btn-primary");

                b.text('Enroll');
            },
            error: function (status) {
                var h2 = document.getElementById("hidden2");
                h2.style.display = 'block';
                console.log("Error in unenrolling " + b.attr("project_id") + "-" + status.status);
            }
        });
    });

$("tbody").on('click', '.clickable-cell', function (e){
        window.location = $(this).data("href");
    });


});
