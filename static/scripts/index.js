
//slides out the filter menu
$(function() {
    $('#filter_button').click(function(){
      	$('#filter_menu').slideToggle();
    });
});

/*determines a random restaurant based on the restaurants
in grid_a*/
function randomRestaurant(){
	var count = $("#grid_a").children().length;
	if(count > 0){
		var choice = Math.round((Math.random() * 100) % (count)-1);
		var restaurant = $("#grid_a .restaurant .name:eq("+choice+")").text();
		var desc = $("#grid_a .restaurant:eq("+choice+")").attr("title");
	}

	else {
		desc = "Perhaps you're too picky";
		restaurant = "No Restaurants";
	}
	$("#popup_title").text(restaurant);
	$("#popup_desc").text(desc);
	$("#popup").slideToggle();
}

//characteristics of ui elements
$(document).ready(function(){ 
	//on click restaurants go to the opposite side
	$(".restaurant").click(function() {
		var grid = $(this).parent().attr('id');
		if(grid == "grid_a"){
			$("#grid_b").append(this);
		}
		else {
			$("#grid_a").append(this);
		}
	});

	//restaurants that are swiped right go to blegh
	$(".restaurant").on("swiperight", function(){
		var grid = $(this).parent().attr('id');
		if(grid != "grid_b"){
			$(this).slideToggle();
			$(this).finish();
			$("#grid_b").append(this);
			$(this).slideToggle();
		}
	});

	//restaurants that are swiped left go to mmm
	$(".restaurant").on("swipeleft", function(){
		var grid = $(this).parent().attr('id');
		if(grid != "grid_a"){
			$(this).slideToggle();
			$(this).finish();
			$("#grid_a").append(this);
			$(this).slideToggle();
		}
	});
});