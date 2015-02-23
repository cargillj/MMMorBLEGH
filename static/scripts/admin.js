//makes sure all fields contain text
function validateForm(){
	var name=document.forms["add_restaurant"]["name"].value;
	var nationality=document.forms["add_restaurant"]["nationality"].value;
	var cost=document.forms["add_restaurant"]["cost"].value;
	var desc=document.forms["add_restaurant"]["random_description"].value;
	if( name==null || name=="",
		nationality==null || nationality=="",
		cost==null || cost=="",
		desc==null || desc==""){
		alert("Please fill out all fields");
		return false;
	}
}