// Initialization
let elevatorCount = 0;
let escalatorCount = 0;

// ====================================================================================================
//
// Add a new row to the elevator table
//
// ====================================================================================================

function addElevator() {
	// Select the div
	const Div = document.getElementById('elevators');
	
	// Create a new row
	const newRow = document.createElement('div');
	newRow.id = `elevator-${elevatorCount}`;
	newRow.innerHTML = `
		<div style="width: 100%; margin: 1em 0 1em 0;">
			<div style="width: 35%; float: left;">
				<label class="form-label-2">電梯最低樓層</label>
				<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_bottom_floor" aria-label="elevator-attr-${elevatorCount}-elevator_bottom_floor">

				<label class="form-label-2">電梯最高樓層</label>
				<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_top_floor" aria-label="elevator-attr-${elevatorCount}-elevator_top_floor">

				<label class="form-label-2">電梯樓層修正量</label>
				<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_floor_offset" aria-label="elevator-attr-${elevatorCount}-elevator_floor_offset">

				<label class="form-label-2">電梯經過耗能分區</label>
				<select class="form-input-2" multiple name="elevator-attr-${elevatorCount}-elevator_es" aria-label="elevator-attr-${elevatorCount}-elevator_es" size="10">
	` + es_option + `
				</select>
			</div>
			<div style="width: 35%; float: left;">

				<label class="form-label-2">電梯效率</label>
				<select class="form-input-2" name="elevator-attr-${elevatorCount}-coef_eff" aria-label="elevator-attr-${elevatorCount}-coef_eff">
					<option disabled selected>選擇電梯種類</option>
					<option value="1.0">1. 普通電梯（1.0）</option>
					<option value="0.7">2. 變頻電梯（0.7）</option>
					<option value="0.5">3. 變頻電力回收電梯（0.5）</option>
				</select>
				
				<label class="form-label-2">電梯額定人數</label>
				<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_people_per_elevator" aria-label="elevator-attr-${elevatorCount}-coef_people_per_elevator" placeholder="人/臺">

				<label class="form-label-2">電梯額定載重</label>
				<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_load_per_elevator" aria-label="elevator-attr-${elevatorCount}-coef_load_per_elevator" placeholder="kg/臺">

				<label class="form-label-2">電梯額定速度</label>
				<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_speed" aria-label="elevator-attr-${elevatorCount}-coef_speed" placeholder="m/min">

			</div>
			<div style="width: 20%; float: right;">
				<button class="form-button-dynamic-delete" type="button" onclick="removeElevator(${elevatorCount})">刪除</button>
			</div>
		</div>
		<hr style="clear: both;">
	`;
	Div.appendChild(newRow);
	elevatorCount++;
}

// ====================================================================================================
//
// Remove a row from the elevator table
//
// ====================================================================================================

function removeElevator(elevatorIndex) {
	const Div = document.getElementById('elevators');
	const removedRow = document.querySelector(`#elevator-${elevatorIndex}`);
	Div.removeChild(removedRow);
}

// ====================================================================================================
//
// Clear all rows from the elevator table
//
// ====================================================================================================

function clearElevators() {
	const Div = document.getElementById('elevators');
	Div.innerHTML = '';
	elevatorCount = 0;
}

// ====================================================================================================
//
// Add a new row to the escalator table
//
// ====================================================================================================

function addEscalator() {

	// Select the div
	const Div = document.getElementById('escalators');
	
	// Create a new row
	const newRow = document.createElement('div');
	newRow.id = `escalator-${elevatorCount}`;
	newRow.innerHTML = `
		<div style="width: 100%; margin: 1em 0 1em 0;">
			<div style="width: 35%; float: left;">
			
				<label class="form-label-2">電扶梯經過耗能分區</label>
				<select class="form-input-2" multiple name="escalator-attr-${elevatorCount}-escalator_es" aria-label="escalator-attr-${elevatorCount}-escalator_es" size="10">
	` + es_option + `
				</select>

			</div>
			<div style="width: 35%; float: left;">

				<label class="form-label-2">電扶梯提升高度</label>
				<input class="form-input-2" type="number" name="escalator-attr-${elevatorCount}-escalator_elevate_height" aria-label="escalator-attr-${elevatorCount}-escalator_elevate_height" placeholder="m">

				<label class="form-label-2">電扶梯級寬</label>
				<input class="form-input-2" type="number" name="escalator-attr-${elevatorCount}-escalator_width" aria-label="escalator-attr-${elevatorCount}-escalator_width" min="0" min="3" step="0.01" placeholder="m">

			</div>
			<div style="width: 20%; float: right;">
				<button class="form-button-dynamic-delete" type="button" onclick="removeEscalator(${elevatorCount})">刪除</button>
			</div>
		</div>
		<hr style="clear: both;">
	`;
	Div.appendChild(newRow);
	elevatorCount++;
}

// ====================================================================================================
//
// Remove a row from the escalator table
//
// ====================================================================================================

function removeEscalator(escalatorIndex) {
	const Div = document.getElementById('escalators');
	const removedRow = document.querySelector(`#escalator-${escalatorIndex}`);
	Div.removeChild(removedRow);
}

// ====================================================================================================
//
// Clear all rows from the escalator table
//
// ====================================================================================================

function clearEscalators() {
	const Div = document.getElementById('escalators');
	Div.innerHTML = '';
	escalatorCount = 0;
}