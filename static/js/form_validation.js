// The main form for estimation will be checked before submitting.

function formValidation() {

	// Check if all numbers elevator-attr-*-elevator_bottom_floor is smaller than elevator-attr-*-elevator_top_floor for given elevatorIndex

	for (var elevatorIndex = 0; elevatorIndex < elevatorCount; elevatorIndex++) {

		window.alert("elevatorIndex = " + elevatorIndex)
		// Continue if the element does not exist
		if (document.getElementsByName("elevator-attr-" + elevatorIndex + "-elevator_bottom_floor").length == 0) {
			window.alert("No elevator-attr-" + elevatorIndex + "-elevator_bottom_floor")
			continue;
		}

		var elevatorBottomFloor = document.getElementsByName("elevator-attr-" + elevatorIndex + "-elevator_bottom_floor")[0].value;
		var elevatorTopFloor = document.getElementsByName("elevator-attr-" + elevatorIndex + "-elevator_top_floor")[0].value;
	
		if (elevatorBottomFloor >= elevatorTopFloor) {
			window.alert("電梯最低樓層必須小於電梯最高樓層。");
			return false;
		}
	}

	// Allow the form to be submitted if all checks are passed
	return true;
}