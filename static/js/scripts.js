$(document).ready(function () {
    // $('.topic').upvote();

    $('#topic').upvote();
    console.log($('a.up').hasClass('upvoted'));
    const is_upvoted = $('a.up').hasClass('upvoted') ? 1 : 0;
    $('.up').on('click', function (e) {
        e.preventDefault();
        const value = $('#value').val();
        const question_id = document.querySelector(".hidden").value;
        const vote_id = document.getElementById('count').innerText;
        console.log(vote_id);
        // console.log(id);
        $.ajax({
            type: "POST",
            url: '/questions/upvote/',
            dataType: 'JSON',
            data: {upvote: 1, question_id: question_id, downvote: 0, is_upvoted: is_upvoted},
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