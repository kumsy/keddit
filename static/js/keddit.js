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

/*********************************************
// Show UPVOTE from the POST PAGE HTML
***********************************************/
function showUpvote(evt) {
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
$(".up").on('click', showUpvote);

/*********************************************
// Show DOWNVOTE from the POST PAGE HTML
***********************************************/
function showDownvote(evt) {
    evt.preventDefault();

    // Get values for post_id and community to use in our url
    let post_id = $("#post_id").val();
    let community_name = $("#community_name").val();
    let url = "/k/" + community_name + "/posts/" +post_id+ "/downvote";

    console.log(url);
    console.log(community_name);
    console.log(post_id);

    $.get(url, function(data){
        // We are getting what our url route returns which is a json object
        var response = JSON.stringify(data);
        console.log(response);
        console.log(data['vote_count']);

        $(".votecount").html(data.vote_count);
  });

}
$(".down").on('click', showDownvote);

/*********************************************
// UPVOTE COMMENTS from comment page
***********************************************/
function upvoteComment(evt) {
    evt.preventDefault();

    // Get values for post_id and community to use in our url
    let post_id = $("#post_id").val();
    let community_name = $("#community_name").val();
    let comment_id = $("#comment_id").val();
    let url = "/k/" + community_name + "/post/" +post_id+ "/comment/" + comment_id + "/upvote";

    // Debug
    console.log(url);
    console.log(community_name);
    console.log(post_id);
    console.log(comment_id);

    $.get(url, function(data){
        // We are getting what our url route returns which is a json object
        var response = JSON.stringify(data);
        console.log(response);
        console.log(data.vote_count_comment);
        $(".votecount_comment").html(data.vote_count_comment);
  });

}
$(".up_comment").on('click', upvoteComment);

/*********************************************
// DOWNVOTE COMMENTS from comment page
***********************************************/
function downvoteComment(evt) {
    evt.preventDefault();

    // Get values for post_id and community to use in our url
    let post_id = $("#post_id").val();
    let community_name = $("#community_name").val();
    let comment_id = $("#comment_id").val();
    let url = "/k/" + community_name + "/post/" +post_id+ "/comment/" + comment_id + "/downvote";

    // Debug
    console.log(url);
    console.log(community_name);
    console.log(post_id);
    console.log(comment_id);

    $.get(url, function(data){
        // We are getting what our url route returns which is a json object
        var response = JSON.stringify(data);
        console.log(response);
        console.log(data.vote_count_comment);
        $(".votecount_comment").html(data.vote_count_comment);
  });

}
$(".down_comment").on('click', downvoteComment);

/*********************************************
// Show upvote from the community PAGE HTML
***********************************************/
function upvotePostList(evt) {
    evt.preventDefault();
    debugger
    // Get values for post_id and community to use in our url
    // Getting the element that was clicked on, it's dataset and it's property id from it's dataset
    let post_id = evt.target.dataset.id;
            

    let community_name = $("#community_name").val();
    let url = "/k/" + community_name + "/posts/" +post_id+ "/upvote";

    console.log(url);
    console.log(community_name);
    console.log(post_id);

    $.get(url, function(data){
        // We are getting what our url route returns which is a json object
        var response = JSON.stringify(data);
        console.log(response);
        console.log(data['vote_count']);

        let postID = (data.post_id)

        $(".votecount#votecount" + postID).html(data.vote_count);
  });

}
$(".up_post_list").on('click', upvotePostList);

/*********************************************
// Show downvote from the community PAGE HTML
***********************************************/
function downvotePostList(evt) {
    evt.preventDefault();
    debugger
    // Get values for post_id and community to use in our url
    // Getting the element that was clicked on, it's dataset and it's property id from it's dataset
    let post_id = evt.target.dataset.id;
            

    let community_name = $("#community_name").val();
    let url = "/k/" + community_name + "/posts/" +post_id+ "/downvote";

    console.log(url);
    console.log(community_name);
    console.log(post_id);

    $.get(url, function(data){
        // We are getting what our url route returns which is a json object
        var response = JSON.stringify(data);
        console.log(response);
        console.log(data['vote_count']);

        let postID = (data.post_id);

        $(".votecount#votecount" + postID).html(data.vote_count);
  });

}
$(".down_post_list").on('click', downvotePostList);


/*********************************************
// Show downvote from the community PAGE HTML
***********************************************/
function upvoteCommentList(evt) {
    evt.preventDefault();
    debugger
    // Get values for post_id and community to use in our url
    // Getting the element that was clicked on, it's dataset and it's property id from it's dataset
    let comment_id = evt.target.dataset.id;
    let post_id = $("#post_id").val();
            

    let community_name = $("#community_name").val();
    let url = "/k/" + community_name + "/post/" +post_id+ "/comment/" + comment_id +"/upvote";

    console.log(url);
    console.log(community_name);
    console.log(comment_id);

    $.get(url, function(data){
        // We are getting what our url route returns which is a json object
        var response = JSON.stringify(data);
        console.log(response);
        console.log(data['vote_count']);

        let commentID = (data.comment_id);

        $(".votecount_comment#votecount_comment" + commentID).html(data.vote_count_comment);
        

  });

}
$(".up_comment_list").on('click', upvoteCommentList);



/*********************************************
// Show downvote from the community PAGE HTML
***********************************************/
function downvoteCommentList(evt) {
    evt.preventDefault();
    debugger
    // Get values for post_id and community to use in our url
    // Getting the element that was clicked on, it's dataset and it's property id from it's dataset
    let comment_id = evt.target.dataset.id;
    let post_id = $("#post_id").val();
            

    let community_name = $("#community_name").val();
    let url = "/k/" + community_name + "/post/" +post_id+ "/comment/" + comment_id +"/downvote";

    console.log(url);
    console.log(community_name);
    console.log(comment_id);

    $.get(url, function(data){
        // We are getting what our url route returns which is a json object
        var response = JSON.stringify(data);
        console.log(response);
        console.log(data['vote_count']);

        let commentID = (data.comment_id)

        $(".votecount_comment#votecount_comment" + commentID).html(data.vote_count_comment);
  });

}
$(".down_comment_list").on('click', downvoteCommentList);



/*********************************************
// GIPHY SEARCH
***********************************************/
function showGiphy(evt) {
    evt.preventDefault();

    console.log('showGiphy')

    // Get values for post_id and community to use in our url
    
    let community_name = $("#community_name").val();
    let giphy_query = $('#giphyQuery').val();
    let url = "/giphy/" + giphy_query;

    // Debug
    console.log(url);
    console.log(community_name);


    $.get(url, function(data){
        // Debug (JSON.stringify)
        var response = JSON.stringify(data);
        console.log(response);

        // console.log(data['vote_count']);

        // let $votecount = $(".votecount");
        // $votecount.html(data['vote_count']);
  });

}

$("#giphySearch").on('click', showGiphy);

