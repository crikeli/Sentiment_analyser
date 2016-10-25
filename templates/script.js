var current_data;

// Writing the function that dictates the color of the text based on the sentiment.
function sentiment_to_color(sentiment){
   if(sentiment == 'Positive') return 'green';
   else if(sentiment == 'Negative') return 'red';
  //  For neutral tweets
   else return 'orange';
}

// Tweets are loaded by this function and here, the connection with the python script occurs where we specified the url.
function load_tweets(querystring){
  // Each query is an ajax call(no page refresh occurs)
   $.ajax({
       url: 'tweets',
       data: {'query': querystring, 'retweets_only': 'false', 'with_sentiment': 'true'},
      //  All the data is in a json format
       dataType: 'json',
       type: 'GET',
       success: function(data) {
           current_data = data['data'];
           var tweets = data['data'];
          //  checking whether or not tweets are retrieved.
          //  console.log(tweets)
           var container = $('#tweets');
           var contents = '';
           for(i = 0; i < tweets.length; i++)
             contents += '<p style="color:'+ sentiment_to_color(tweets[i].sentiment) +'">' + tweets[i].text + tweets[i].text.length +'</p>';
           container.html(contents);
          //  console.log("We UP IN DIS")
           $('#query').val(querystring);
           $('#loading').html("Number of tweets retrieved about "+ querystring +": " + data['count']);
       }
   });
}

// What happens once the document is loaded.
$(document).ready(function(){
   load_tweets('Election 2016');
 });

// What happens upon clicking search
$('#search').click(function(){
   $('#loading').html('Loading...');
   $('#tweets').html('');
   load_tweets($('#query').val());
});
