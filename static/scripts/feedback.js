//makes sure the feedback field contains text
function validateForm(){
	var name=document.forms["feedback_form"]["name"].value;
	var feedback=document.forms["feedback_form"]["feedback"].value;
	if(feedback==null || feedback==""){
		alert("Please fill out the feedback field");
		return false;
	}
}