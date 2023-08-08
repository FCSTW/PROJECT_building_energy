// The main form for estimation will be checked before submitting.

function formValidation() {

	// ====================================================================================================
	//
	// Check if all numbers elevator-attr-*-elevator_bottom_floor is smaller than elevator-attr-*-elevator_top_floor for given elevatorIndex
	//
	// ====================================================================================================
	
	for (var elevatorIndex = 0; elevatorIndex < elevatorCount; elevatorIndex++) {

		// Continue if the element does not exist
		if (document.getElementsByName("elevator-attr-" + elevatorIndex + "-elevator_bottom_floor").length == 0) {
			continue;
		}

		var elevatorBottomFloor = parseInt(document.getElementsByName("elevator-attr-" + elevatorIndex + "-elevator_bottom_floor")[0].value);
		var elevatorTopFloor = parseInt(document.getElementsByName("elevator-attr-" + elevatorIndex + "-elevator_top_floor")[0].value);
	
		if (elevatorBottomFloor >= elevatorTopFloor) {
			alert("電梯最低樓層必須小於電梯最高樓層。");
			return false;
		}
	}

	// ====================================================================================================
	//
	// Check if ec value is valid
	//
	// ====================================================================================================

	// Get the value of ec_input_type select box
	let buildingEc = document.getElementsByName('ec_input_type')[0].value;

	// Check if the ec value is valid
	if (ecValueValidation(buildingEc) == false) {
		return false;
	}
	// Allow the form to be submitted if all checks are passed
	return true;
}

function ecValueValidation(select_ec) {
	
	// ====================================================================================================
	//
	// Check if the ec value is valid
	//
	// ====================================================================================================
	
	// Variable declaration
	let ecMonthlyValuesAnnualRatio = 0;
	let ecMonthlyValuesRatio = 0;

	// Determine the type of ec input
	if (select_ec == 'direct') {
		return true;
	}

	if (select_ec == 'monthly') {

		// Get all input that the name starts with ec_monthly_
		let ecMonthlyInputs = document.querySelectorAll('input[name^="ec_monthly_"]');

		// Concatenate all values into a array
		let ecMonthlyValues = [];
		for (var i = 0; i < ecMonthlyInputs.length; i++) {
			ecMonthlyValues.push(ecMonthlyInputs[i].value);
		}

		// Calculate the annual mean (average every 12 elements)
		let ecMonthlyValuesAnnualMean = [];
		for (var i = 0; i < ecMonthlyValues.length; i += 12) {
			ecMonthlyValuesAnnualMean.push(ecMonthlyValues.slice(i, i + 12).reduce((a, b) => parseInt(a) + parseInt(b), 0) / 12);
		}

		ecMonthlyValuesAnnualRatio = Math.min(...ecMonthlyValuesAnnualMean) / Math.max(...ecMonthlyValuesAnnualMean);
		ecMonthlyValuesRatio = Math.min(...ecMonthlyValues) / Math.max(...ecMonthlyValues);

	} else if (select_ec == 'bimonthly') {
		
		// Get all input that the name starts with ec_bimonthly_
		let ecBimonthlyInputs = document.querySelectorAll('input[name^="ec_bimonthly_"]');

		// Concatenate all values into a array
		let ecBimonthlyValues = [];
		for (var i = 0; i < ecBimonthlyInputs.length; i++) {
			ecBimonthlyValues.push(ecBimonthlyInputs[i].value);
		}

		// Calculate the annual mean (average every 6 elements)
		let ecBimonthlyValuesAnnualMean = [];
		for (var i = 0; i < ecBimonthlyValues.length; i += 6) {
			ecBimonthlyValuesAnnualMean.push(ecBimonthlyValues.slice(i, i + 6).reduce((a, b) => parseInt(a) + parseInt(b), 0) / 6);
		}

		ecMonthlyValuesAnnualRatio = Math.min(...ecBimonthlyValuesAnnualMean) / Math.max(...ecBimonthlyValuesAnnualMean);
		ecMonthlyValuesRatio = Math.min(...ecBimonthlyValues) / Math.max(...ecBimonthlyValues);
	}

	// ====================================================================================================
	// Create message string
	let message = '';

	// Check if the ratio of minimum and maximum in ecMonthlyValuesAnnualMean is less than 0.8
	if (ecMonthlyValuesAnnualRatio < 0.8) {
		message = message + `<div>年平均電費最小值與最大值之比必須大於 80%（目前為${Math.round(ecMonthlyValuesAnnualRatio * 100).toFixed(2)}%）</div>`;
	}

	// Check if the ratio of minimum and maximum in ecMonthlyValues is less than 0.5
	if (ecMonthlyValuesRatio < 0.5) {
		message = message + `<div>月電費最小值與最大值之比必須大於 50%。（目前為${Math.round(ecMonthlyValuesRatio * 100).toFixed(2)}%）</div>`;
	}

	// Update the alert message in building-ec-message div
	document.getElementById('building-ec-message').innerHTML = `
		${message}
	`;

	// Return boolean
	if (message == '') {
		return true;
	} else {
		return false;
	}
}