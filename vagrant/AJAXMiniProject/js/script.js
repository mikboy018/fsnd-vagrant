
function loadData() {

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview
    var gMapsUrl ='http://maps.googleapis.com/maps/api/streetview?size=600x400&location='

    // Pull data from the street and city input boxes, concatenate
    var streetStr = $('#street').val();
    var cityStr = $('#city').val();
    var address = streetStr + ',' + cityStr;

    // Update greeting
    $greeting.text('So, you want to live at ' + address + '?');

    // Update background image with streetview image based on address
    $body.append('<img class="bgimg" src="' + gMapsUrl + address +'">');
    
    return false;
};

$('#form-container').submit(loadData);
