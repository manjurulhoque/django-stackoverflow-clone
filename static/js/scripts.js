$(document).ready(function () {
    // $('.topic').upvote();

    $('#topic').upvote();

    $('.up').on('click', function (e) {
        e.preventDefault();
        var value = $('#value').val();
        var id = document.querySelector(".hidden").value;
        const vote_id = document.getElementById('count').innerText;
        console.log(vote_id);
        // console.log(id);
        $.ajax({
            type: "POST",
            url: '/questions/upvote/',
            dataType: 'JSON',
            data: {value: 1},
            success: function (data) {

                console.log(data);

                if (data.status == 'ok') {
                    // alert(data);
                    // window.location.reload();
                } else {
                    alert('error');
                }
            }
        });
    });
});