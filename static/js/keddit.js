"use strict";

$(function() {
    //alert("ready!");

    // Make API route on the server side
    // - take inputs
    // - validation
    // - return success/failure
    // - update db

    // Click handler
    // - register to all upvotes and downvotes
    // - $(".upbutton").click( ... )

    // $.post(url, data, success_func, error_func)
    // or $.ajax(url, method: "POST", data, success_func, error_func)

    // logic in click handler, success_func and error_func

    // one or many will have to modify the page (DOM)
});

// let $votecount = $(".votecount");

// function upvote(results){
//     $votecount.html("TEST");
// }

// $(".votecount").on('click', upvote);

function showVote(evt) {
    evt.preventDefault();

    // Get values for post_id and community to use in our url
    let post_id = $("#post_id").val();
    let community_name = $("#community_name").val();
    let url = "/k/" + community_name + "/posts/" +post_id+ "/upvote";

    // Debug
    console.log(url);
    console.log(community_name);
    console.log(post_id);

    $.get(url, function(data){
        // Debug (JSON.stringify)
        var response = JSON.stringify(data);
        console.log(response);
        
        console.log(data['vote_count']);

        let $votecount = $(".votecount");
        $votecount.html(data['vote_count']);
  });

}

$(".up").on('click', showVote);


