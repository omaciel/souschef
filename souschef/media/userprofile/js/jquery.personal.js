$(function(){
	$("input[type='text']").addClass("text");
	$("#id_firstname").focus();
	$("#id_birthdate,#id_gender").addClass("hidden");
	$("#id_gender").before('\
    <p style="overflow: hidden;">\
      <a class="male" href="#">Male</a>\
      <a class="female" href="#">Female</a>\
    </p>\
	');

	// Gender select
	if ($("#id_gender").val() == "M") {
			$("a.male").addClass("item_selected");
			$("a.female").addClass("item_not_selected");
	} else if ($("#id_gender").val() == "F") {
			$("a.female").addClass("item_selected");
			$("a.male").addClass("item_not_selected");
	}

	$("a.male").click(function() {
		if ($("#id_gender").val() == "M") {
			$("#id_gender").val("");	
		} else {
			$("#id_gender").val("M");	
			$(this).removeClass("item_not_selected");
			$(this).addClass("item_selected");
			$("a.female").removeClass("item_selected");
			$("a.female").addClass("item_not_selected");
		}
		return false;
	});

	$("a.female").click(function() {
		if ($("#id_gender").val() == "F") {
			$("#id_gender").val("");	
		} else {
			$("#id_gender").val("F");	
			$(this).removeClass("item_not_selected");
			$(this).addClass("item_selected");
			$("a.male").removeClass("item_selected");
			$("a.male").addClass("item_not_selected");
		}
		return false;
	});

});
