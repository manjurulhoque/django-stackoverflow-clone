$(document).ready(function () {
    // $('.topic').upvote();
    // const total = {{ vote_count }};

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
                    window.location.reload();
                } else {
                    alert('error');
                }
            }
        });
    });
    const is_downvoted = $('a.downvote').hasClass('downvoted') ? 1 : 0;
    $('.downvote').on('click', function (e) {
        e.preventDefault();
        console.log('Clicked downvote');
        const question_id = document.querySelector(".hidden").value;
        console.log(question_id);
        // console.log(id);
        $.ajax({
            type: "POST",
            url: '/questions/downvote/',
            dataType: 'JSON',
            data: { upvote: 0, question_id: question_id, downvote: 1, is_downvoted: is_downvoted },
            success: function (data) {

                console.log(data);

                if (data.status == 'ok') {
                    // alert(data);
                    window.location.reload();
                } else {
                    alert('error');
                }
            }
        });
    });

    document.getElementById('id_password').type = 'password';
});