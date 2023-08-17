// Initialization
let elevatorCount = 0;
let escalatorCount = 0;
let waterTowerCount = 0;
let heaterCount = 0;
let parkingGarageCount = 0;

// ====================================================================================================
// ELEVATOR

// ====================================================================================================
//
// Add a new row to the elevator table
//
// ====================================================================================================

function addElevator(estimationSystem) {

	// Select the div
	const Div = document.getElementById('elevators');
	
	// Create a new row
	const newRow = document.createElement('div');
	newRow.id = `elevator-${elevatorCount}`;

	// Set html content based on estimation system
	if (estimationSystem == 'BERSe') {

		newRow.innerHTML = `
			<div style="width: 100%; margin: 1em 0 1em 0;">
				<div style="width: 35%; float: left;">
					<label class="form-label-2">電梯最低樓層</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_bottom_floor" aria-label="elevator-attr-${elevatorCount}-elevator_bottom_floor" step="1">

					<label class="form-label-2">電梯最高樓層</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_top_floor" aria-label="elevator-attr-${elevatorCount}-elevator_top_floor" step="1">

					<label class="form-label-2">電梯樓層修正量</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_floor_offset" aria-label="elevator-attr-${elevatorCount}-elevator_floor_offset" value=0 step="1">

					<label class="form-label-2">電梯經過耗能分區</label>
					<select class="form-input-2" multiple name="elevator-attr-${elevatorCount}-elevator_es" aria-label="elevator-attr-${elevatorCount}-elevator_es" size="10">
		` + es_option + `
					</select>
				</div>
				<div style="width: 35%; float: left;">

					<label class="form-label-2">電梯類型</label>
					<select class="form-input-2" name="elevator-attr-${elevatorCount}-elevator_type" aria-label="elevator-attr-${elevatorCount}-elevator_type">
						<option disabled selected>選擇電梯類型</option>
						<option value="common">客用電梯</option>
						<option value="freight">貨用電梯</option>
					</select>
					
					<label class="form-label-2">電梯效率</label>
					<select class="form-input-2" name="elevator-attr-${elevatorCount}-coef_eff" aria-label="elevator-attr-${elevatorCount}-coef_eff">
						<option disabled selected>選擇電梯種類</option>
						<option value="1.0">1. 普通電梯（1.0）</option>
						<option value="0.7">2. 變頻電梯（0.7）</option>
						<option value="0.5">3. 變頻電力回收電梯（0.5）</option>
					</select>
					
					<label class="form-label-2">電梯額定人數</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_people_per_elevator" aria-label="elevator-attr-${elevatorCount}-coef_people_per_elevator" placeholder="人/臺" min="1" step="1">

					<label class="form-label-2">電梯額定載重</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_load_per_elevator" aria-label="elevator-attr-${elevatorCount}-coef_load_per_elevator" placeholder="kg/臺" min="1" step="1">

					<label class="form-label-2">電梯額定速度</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_speed" aria-label="elevator-attr-${elevatorCount}-coef_speed" placeholder="m/min" min="1" step="1">

				</div>
				<div style="width: 20%; float: right;">
					<button class="form-button-dynamic-delete" type="button" onclick="removeElevator(${elevatorCount})">刪除</button>
				</div>
			</div>
			<hr style="clear: both;">
		`;
		
	} else if (estimationSystem == 'R-BERS') {

		newRow.innerHTML = `
			<div style="width: 100%; margin: 1em 0 1em 0;">
				<div style="width: 35%; float: left;">
					<label class="form-label-2">電梯最低樓層</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_bottom_floor" aria-label="elevator-attr-${elevatorCount}-elevator_bottom_floor" step="1">

					<label class="form-label-2">電梯最高樓層</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_top_floor" aria-label="elevator-attr-${elevatorCount}-elevator_top_floor" step="1">

					<label class="form-label-2">電梯樓層修正量</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-elevator_floor_offset" aria-label="elevator-attr-${elevatorCount}-elevator_floor_offset" value=0 step="1">

				</div>
				<div style="width: 35%; float: left;">

					<label class="form-label-2">電梯效率</label>
					<select class="form-input-2" name="elevator-attr-${elevatorCount}-coef_eff" aria-label="elevator-attr-${elevatorCount}-coef_eff">
						<option disabled selected>選擇電梯種類</option>
						<option value="1.0">一般交流馬達：1.0</option>
						<option value="0.6">變壓變頻控制螺旋齒輪：0.6</option>
						<option value="0.5">變壓變頻控制永磁同步馬達：0.5</option>
						<option value="0.5">變壓變頻控制螺旋齒輪與電力回收裝置電梯：0.5</option>
						<option value="0.4">變壓變頻控制永磁同步馬達與電力回收裝置電梯：0.4</option>
					</select>
					
					<label class="form-label-2">電梯額定人數</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_people_per_elevator" aria-label="elevator-attr-${elevatorCount}-coef_people_per_elevator" placeholder="人/臺" min="1" step="1">

					<label class="form-label-2">電梯額定載重</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_load_per_elevator" aria-label="elevator-attr-${elevatorCount}-coef_load_per_elevator" placeholder="kg/臺" min="1" step="1">

					<label class="form-label-2">電梯額定速度</label>
					<input class="form-input-2" type="number" name="elevator-attr-${elevatorCount}-coef_speed" aria-label="elevator-attr-${elevatorCount}-coef_speed" placeholder="m/min" min="1" step="1">

				</div>
				<div style="width: 20%; float: right;">
					<button class="form-button-dynamic-delete" type="button" onclick="removeElevator(${elevatorCount})">刪除</button>
				</div>
			</div>
			<hr style="clear: both;">
		`;
		
	}

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
// ESCALATOR

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
	newRow.id = `escalator-${escalatorCount}`;
	newRow.innerHTML = `
		<div style="width: 100%; margin: 1em 0 1em 0;">
			<div style="width: 35%; float: left;">
			
				<label class="form-label-2">電扶梯經過耗能分區</label>
				<select class="form-input-2" multiple name="escalator-attr-${escalatorCount}-escalator_es" aria-label="escalator-attr-${escalatorCount}-escalator_es" size="10">
	` + es_option + `
				</select>

			</div>
			<div style="width: 35%; float: left;">

				<label class="form-label-2">電扶梯提升高度</label>
				<input class="form-input-2" type="number" name="escalator-attr-${escalatorCount}-escalator_elevate_height" aria-label="escalator-attr-${escalatorCount}-escalator_elevate_height" min="0" step="0.01" placeholder="m">

				<label class="form-label-2">電扶梯級寬</label>
				<input class="form-input-2" type="number" name="escalator-attr-${escalatorCount}-escalator_width" aria-label="escalator-attr-${escalatorCount}-escalator_width" min="0" max="3" step="0.01" placeholder="m">

			</div>
			<div style="width: 20%; float: right;">
				<button class="form-button-dynamic-delete" type="button" onclick="removeEscalator(${escalatorCount})">刪除</button>
			</div>
		</div>
		<hr style="clear: both;">
	`;
	Div.appendChild(newRow);
	escalatorCount++;
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


// ====================================================================================================
// WATER TOWER

// ====================================================================================================
//
// Add a new row to the water tower table
//
// ====================================================================================================

function addWaterTower(estimationSystem) {

	// Select the div
	const Div = document.getElementById('watertowers');
	
	// Create a new row
	const newRow = document.createElement('div');
	newRow.id = `watertower-${waterTowerCount}`;

	// Set html content based on estimation system
	if (estimationSystem == 'BERSe') {

		newRow.innerHTML = `
			<div style="width: 100%; margin: 1em 0 1em 0;">
				<div style="width: 35%; float: left;">
				
					<label class="form-label-2">水塔所在高度</label>
					<input class="form-input-2" type="number" name="watertower-attr-${waterTowerCount}-height_watertower" aria-label="watertower-attr-${waterTowerCount}-height_watertower" min="0" placeholder="m">

				</div>
				<div style="width: 35%; float: left;">

				</div>
				<div style="width: 20%; float: right;">
					<button class="form-button-dynamic-delete" type="button" onclick="removeWaterTower(${waterTowerCount})">刪除</button>
				</div>
			</div>
			<hr style="clear: both;">
		`;

	} else if (estimationSystem == 'R-BERS') {

		newRow.innerHTML = `
			<div style="width: 100%; margin: 1em 0 1em 0;">
				<div style="width: 35%; float: left;">
				
					<label class="form-label-2">設計揚水量</label>
					<input class="form-input-2" type="number" name="watertower-attr-${waterTowerCount}-water_pumping_capacity" aria-label="watertower-attr-${waterTowerCount}-water_pumping_capacity"  min="0" step="0.01" placeholder="L/min">

				</div>
				<div style="width: 35%; float: left;">

					<label class="form-label-2">基準靜揚程</label>
					<input class="form-input-2" type="number" name="watertower-attr-${waterTowerCount}-standard_hydraulic_head_static" aria-label="watertower-attr-${waterTowerCount}-standard_hydraulic_head_static" min="0" step="0.01" placeholder="m">

					<label class="form-label-2">基準摩擦揚程</label>
					<input class="form-input-2" type="number" name="watertower-attr-${waterTowerCount}-standard_hydraulic_head_friction" aria-label="watertower-attr-${waterTowerCount}-standard_hydraulic_head_friction" min="0" step="0.01" placeholder="m">

					<label class="form-label-2">設計總揚程</label>
					<input class="form-input-2" type="number" name="watertower-attr-${waterTowerCount}-hydraulic_head_total" aria-label="watertower-attr-${waterTowerCount}-hydraulic_head_total" min="0" step="0.01" placeholder="m">

				</div>
				<div style="width: 20%; float: right;">
					<button class="form-button-dynamic-delete" type="button" onclick="removeWaterTower(${waterTowerCount})">刪除</button>
				</div>
			</div>
			<hr style="clear: both;">
		`;

	}

	Div.appendChild(newRow);
	waterTowerCount++;
}

// ====================================================================================================
//
// Remove a row from the water tower table
//
// ====================================================================================================

function removeWaterTower(waterTowerIndex) {
	const Div = document.getElementById('watertowers');
	const removedRow = document.querySelector(`#watertower-${waterTowerIndex}`);
	Div.removeChild(removedRow);
}

// ====================================================================================================
//
// Clear all rows from the water tower table
//
// ====================================================================================================

function clearWaterTowers() {
	const Div = document.getElementById('watertowers');
	Div.innerHTML = '';
	waterTowerCount = 0;
}



// ====================================================================================================
// HEATER

// ====================================================================================================
//
// Add a new row to the heater table
//
// ====================================================================================================

function addHeater() {

	// Select the div
	const Div = document.getElementById('heaters');
	
	// Create a new row
	const newRow = document.createElement('div');
	newRow.id = `heater-${heaterCount}`;

	// Set html content
	newRow.innerHTML = `
		<div style="width: 100%; margin: 1em 0 1em 0;">
			<div style="width: 35%; float: left;">
			
				<label class="form-label-2">加熱設備種類</label>
				<select class="form-input-2" name="heater-attr-${heaterCount}-type" aria-label="heater-attr-${heaterCount}-type">
					<option disabled selected>請選擇加熱設備種類</option>
					<option value="1">1 瓦斯熱水器</option>
					<option value="2.1">2.1 瓦斯熱水器</option>
					<option value="2.2">2.2 端末蓄熱式用電熱水器</option>
					<option value="2.3">2.3 熱泵用電熱水器</option>
					<option value="3">3 燃氣爐臺</option>
					<option value="4.1">4.1 IH 電磁爐</option>
					<option value="4.2">4.2 鹵素爐、電陶爐</option>
				</select>

			</div>
			<div style="width: 35%; float: left;">
			
				<label class="form-label-2">加熱設備能效標章</label>
				<select class="form-input-2" name="heater-attr-${heaterCount}-energy_rating" aria-label="heater-attr-${heaterCount}-energy_rating">
					<option disabled selected>請選擇加熱設備種類</option>
					<option value="1">一級</option>
					<option value="2">二級</option>
					<option value="3">三級</option>
					<option value="4">四級</option>
					<option value="5">五級</option>
					<option value="none">無能效標章</option>
				</select>

				<label class="form-label-2">加熱設備數量</label>
				<input class="form-input-2" type="number" name="heater-attr-${heaterCount}-quantity" aria-label="heater-attr-${heaterCount}-quantity" min="1" step="1" placeholder="加熱設備數量">

				<label class="form-label-2">加熱設備熱水管路熱傳導率</label>
				<input class="form-input-2" type="number" name="heater-attr-${heaterCount}-coef_pipe_thermal_conductivity" aria-label="heater-attr-${heaterCount}-coef_pipe_thermal_conductivity" value=4.5 min="0" step="0.01" placeholder="W/(m^2*K)">

			</div>
			<div style="width: 20%; float: right;">
				<button class="form-button-dynamic-delete" type="button" onclick="removeHeater(${heaterCount})">刪除</button>
			</div>
		</div>
		<hr style="clear: both;">
	`;

	Div.appendChild(newRow);
	heaterCount++;
}

// ====================================================================================================
//
// Remove a row from the heater table
//
// ====================================================================================================

function removeHeater(heaterIndex) {
	const Div = document.getElementById('heaters');
	const removedRow = document.querySelector(`#heater-${heaterIndex}`);
	Div.removeChild(removedRow);
}

// ====================================================================================================
//
// Clear all rows from the heater table
//
// ====================================================================================================

function clearHeaters() {
	const Div = document.getElementById('heaters');
	Div.innerHTML = '';
	heaterCount = 0;
}



// ====================================================================================================
// PARKING GARAGE

// ====================================================================================================
//
// Add a new row to the parking garage table
//
// ====================================================================================================

function addParkingGarage() {

	// Select the div
	const Div = document.getElementById('parkinggarages');
	
	// Create a new row
	const newRow = document.createElement('div');
	newRow.id = `parkinggarage-${parkingGarageCount}`;

	// Set html content
	newRow.innerHTML = `
		<div style="width: 100%; margin: 1em 0 1em 0;">
			<div style="width: 35%; float: left;">
			
				<label class="form-label-2">地下停車場面積</label>
				<input class="form-input-2" type="number" name="parkinggarage-attr-${parkingGarageCount}-a" aria-label="parkinggarage-attr-${parkingGarageCount}-a" min="0" step="0.01" placeholder="地下停車場面積">

			</div>
			<div style="width: 35%; float: left;">
			
				<label class="form-label-2">地下停車場所在樓層</label>
				<input class="form-input-2" type="number" name="parkinggarage-attr-${parkingGarageCount}-floor" aria-label="parkinggarage-attr-${parkingGarageCount}-floor" max="-1" step="1" placeholder="地下停車場所在樓層">

				<label class="form-label-2">是否有送排風設備節能標章</label>
				<select class="form-input-2" name="parkinggarage-attr-${parkingGarageCount}-energy_rating" aria-label="parkinggarage-attr-${parkingGarageCount}-energy_rating">
					<option disabled selected>請選擇</option>
					<option value="False">無</option>
					<option value="True">有</option>
				</select>

				<label class="form-label-2">是否有送排風設備二氧化碳偵測變頻功能</label>
				<select class="form-input-2" name="parkinggarage-attr-${parkingGarageCount}-co2_variable_frequency" aria-label="parkinggarage-attr-${parkingGarageCount}-co2_variable_frequency">
					<option disabled selected>請選擇</option>
					<option value="False">無</option>
					<option value="True">有</option>
				</select>

			</div>
			<div style="width: 20%; float: right;">
				<button class="form-button-dynamic-delete" type="button" onclick="removeParkingGarage(${parkingGarageCount})">刪除</button>
			</div>
		</div>
		<hr style="clear: both;">
	`;

	Div.appendChild(newRow);
	parkingGarageCount++;
}

// ====================================================================================================
//
// Remove a row from the parking garage table
//
// ====================================================================================================

function removeParkingGarage(parkingGarageIndex) {
	const Div = document.getElementById('parkinggarages');
	const removedRow = document.querySelector(`#parkinggarage-${parkingGarageIndex}`);
	Div.removeChild(removedRow);
}

// ====================================================================================================
//
// Clear all rows from the parking garage table
//
// ====================================================================================================

function clearParkingGarages() {
	const Div = document.getElementById('parkinggarages');
	Div.innerHTML = '';
	parkingGarageCount = 0;
}