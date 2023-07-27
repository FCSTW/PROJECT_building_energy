// Initialization

let energySectionCount = 0;
let energySectionExclusiveCount = 0;

// ====================================================================================================
//
// Add a new row to the ES table
//
// ====================================================================================================

function addEnergySection() {

    // Select the div
	const Div = document.getElementById('energy-sections');

	// Create a new row
	const newRow = document.createElement('div');
	newRow.id = `energy-section-${energySectionCount}`;
	newRow.innerHTML = `
		<div style="width: 100%; margin: 1em 0 1em 0;">
			<div style="width: 35%; float: left;">
				<label class="form-label-2">耗能分區</label>
				<select class="form-input-2" name="es-id-${energySectionCount}" onchange="esIdChange(${energySectionCount})" aria-label="es-id-${energySectionCount}">
		` + es_option + `
				</select>
			</div>
			<div style="width: 40%; float: left;">
				<div name="form-es-attr-${energySectionCount}" style="flex-direction: column; display: flex;"></div>
			</div>
			<div style="width: 20%; float: right;">
				<button class="form-button-dynamic-delete" type="button" onclick="removeEnergySection(${energySectionCount})">刪除</button>
			</div>
		</div>
		<hr style="clear: both;">
	`;
	Div.appendChild(newRow);
	energySectionCount++;
}

// ====================================================================================================
//
// Remove a row from the ES table
//
// ====================================================================================================

function removeEnergySection(sectionIndex) {
	const Div = document.getElementById('energy-sections');
	const removedRow = document.querySelector(`#energy-section-${sectionIndex}`);
	Div.removeChild(removedRow);
}

// ====================================================================================================
//
// Clear all rows from the ES table
//
// ====================================================================================================

function clearEnergySections() {
	const Div = document.getElementById('energy-sections');
	Div.innerHTML = '';
	energySectionCount = 0;
}

// ====================================================================================================
//
// ES ID change
//
// ====================================================================================================

function esIdChange(sectionIndex) {
	// Select the div
	const form = document.querySelector(`div[name="form-es-attr-${sectionIndex}"]`);
	// Get the selected value
	const esId = document.querySelector(`select[name="es-id-${sectionIndex}"]`).value;
	
	// Clear the form
	form.innerHTML = `
		<div>
			<label class="form-label-2">分區面積</label>
			<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-a" placeholder="分區面積 [m2]" onchange="esAreaChange()" required>
		</div>
		<div>
			<label class="form-label-2">空調營運類型</label>
			<select class="form-input-3" name="es-attr-${sectionIndex}-ac_operation" aria-label="es-attr-${sectionIndex}-ac_operation">
				<option disabled selected>選擇空調營運類型</option>
				<option value="interval">間歇式</option>
				<option value="continue">全年式</option>
			</select>
		</div>
		<div>
			<label class="form-label-2">是否為水冷式空調系統</label>
			<select class="form-input-3" name="es-attr-${sectionIndex}-ac_type" aria-label="es-attr-${sectionIndex}-ac_type">
				<option disabled selected>選擇是否為水冷式空調系統</option>
				<option value="watercooled">水冷式</option>
				<option value="normal">一般</option>
			</select>
		</div>
	`;

	// Create the new form
	switch (esId) {
		case "H1": case "H2":
			// Facility: Hotel
			form.innerHTML = form.innerHTML + `
				<div>
					<label class="form-label-2">客房數量</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-hotel-n_room" placeholder="客房數量" required>
				</div>
				<div>
					<label class="form-label-2">年住房率</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-hotel-coef_usage_r_room" placeholder="客房使用比例，介於 0 至 1" min="0" max="1" step="0.01" required>
				</div>
			`
			break;
		case "A1": case "A2": case "K1": case "K3": case "K8": case "K9":
			// Facility: Hospital
			form.innerHTML = form.innerHTML + `
				<div>
					<label class="form-label-2">病床數量</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-hospital-n_hospitalbed" placeholder="病床數量" required>
				</div>
				<div>
					<label class="form-label-2">年病床占床率</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-hospital-coef_usage_r_hospitalbed" placeholder="介於 0 至 1" min="0" max="1" step="0.01" required>
				</div>
			`
			break;
		case "H7": case "H9": case "L2": case "L3": case "L4-2":
			// Facility: Sports bathroom
			form.innerHTML = form.innerHTML + `
				<div>
					<label class="form-label-2">盥洗區面積</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-sportbathroom-a" placeholder="m2（無盥洗區則免填）" required>
				</div>
				<div>
					<label class="form-label-2">全年營運時數</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-sportbathroom-coef_usage_h" placeholder="h/year（無盥洗區則免填）" required>
				</div>
			`
			break;
		case "H8": case "L6-1": case "L6-2": case "L6-3":
			// Facility: Swimming pool, SPA, and sport bathroom
			form.innerHTML = form.innerHTML + `
				<div>
					<label class="form-label-2">游泳池加熱方式</label>
					<select class="form-input-3" name="es-attr-${sectionIndex}-swimmingpool-ec_heating" aria-label="es-attr-${sectionIndex}-swimmingpool-ec_heating">
						<option disabled selected>選擇氣源熱泵加熱方式</option>
						<option value="BHPE">BHPE - 硬銲型板式熱交換器</option>
						<option value="Other">其他</option>
					</select>
				</div>
				<div>
					<label class="form-label-2">游泳池體積</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-swimmingpool-v" placeholder="m3" required>
				</div>
				<div>
					<label class="form-label-2">游泳池全年營運時數</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-swimmingpool-coef_usage_h" placeholder="h/year" min="0" max="8760" step="1" required>
				</div>
				<div>
					<label class="form-label-2">游泳池水塔高度</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-swimmingpool-height_watertower" placeholder="m" required>
				</div>
				<div>
					<label class="form-label-2">游泳池是否恆溫</label>
					<select class="form-input-3" name="es-attr-${sectionIndex}-swimmingpool-constant_temperature" aria-label="es-attr-${sectionIndex}-swimmingpool-constant_temperature">
						<option disabled selected>選擇是否恆溫</option>
						<option value="True">是</option>
						<option value="False">否</option>
					</select>
				</div>
				<div>
					<label class="form-label-2">SPA 池加熱方式</label>
					<select class="form-input-3" name="es-attr-${sectionIndex}-spa-ec_heating" aria-label="es-attr-${sectionIndex}-spa-ec_heating">
						<option disabled selected>選擇氣源熱泵加熱方式</option>
						<option value="BHPE">BHPE - 硬銲型板式熱交換器</option>
						<option value="Other">其他</option>
					</select>
				</div>
				<div>
					<label class="form-label-2">SPA 池體積</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-spa-v" placeholder="m3" required>
				</div>
				<div>
					<label class="form-label-2">SPA 池全年營運時數</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-spa-coef_usage_h" placeholder="h/year" min="0" max="8760" step="1" required>
				</div>
				<div>
					<label class="form-label-2">SPA 池水塔高度</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-spa-height_watertower" placeholder="m" required>
				</div>
				<div>
					<label class="form-label-2">SPA 池是否恆溫</label>
					<select class="form-input-3" name="es-attr-${sectionIndex}-spa-constant_temperature" aria-label="es-attr-${sectionIndex}-spa-constant_temperature">
						<option disabled selected>選擇是否恆溫</option>
						<option value="True">是</option>
						<option value="False">否</option>
					</select>
				</div>
				<div>
					<label class="form-label-2">盥洗區面積</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-sportbathroom-a" placeholder="m2（無盥洗區則免填）">
				</div>
				<div>
					<label class="form-label-2">盥洗區全年營運時數</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-sportbathroom-coef_usage_h" placeholder="h/year（無盥洗區則免填）" min="0" max="8760" step="1">
				</div>
			`
			break;
		case "H10": case "I1": case "I2": case "I3": case "I4": case "I5": case "I6": case "I7":
			// Facility: Dinning area
			form.innerHTML = form.innerHTML + `
				<div>
					<label class="form-label-2">用餐區面積</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-diningarea-a" placeholder="m2">
				</div>
				<div>
					<label class="form-label-2">每天提供餐數</label>
					<select class="form-input-3" name="es-attr-${sectionIndex}-diningarea-n_meal_per_day" aria-label="es-attr-${sectionIndex}-diningarea-n_meal_per_day">
						<option disabled selected>選擇每天提供餐數</option>
						<option value="1">每日一餐</option>
						<option value="2">每日兩餐</option>
						<option value="3">每日三餐</option>
						<option value="4">24 小時供餐</option>
					</select>
				</div>
				<div>
					<label class="form-label-2">是否手洗碗</label>
					<select class="form-input-3" name="es-attr-${sectionIndex}-diningarea-washdishes_by_hand" aria-label="es-attr-${sectionIndex}-diningarea-washdishes_by_hand">
						<option disabled selected>選擇是否手洗碗</option>
						<option value="True">手洗</option>
						<option value="False">洗碗機</option>
					</select>
				</div>
				<div>
					<label class="form-label-2">全年營運天數</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-diningarea-coef_usage_d" placeholder="day/year" min="0" max="365" step="1">
				</div>
			`
			break;
		case "D1": case "D2": case "D3": case "E1":
			// Facility: Exhibition area
			form.innerHTML = form.innerHTML + `
				<div>
					<label class="form-label-2">全年營運天數</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-exhibitionarea-coef_usage_d" placeholder="day/year" min="0" max="365" step="1">
				</div>
			`
			break;
		case "F1": case "F2": case "G1": case "G2":
			// Facility: Performance area
			form.innerHTML = form.innerHTML + `
				<div>
					<label class="form-label-2">全年營運天數</label>
					<input class="form-input-3" type="number" name="es-attr-${sectionIndex}-performancearea-coef_usage_d" placeholder="day/year" min="0" max="365" step="1">
				</div>
			`
			break;
	}
}

// ====================================================================================================
//
// ES area change
//
// ====================================================================================================

// Add all the ES area and change the text of div form-total-area
function esAreaChange() {
	let totalArea = 0;
	for (let i = 0; i < energySectionCount; i++) {
	 	// Check if the input object exists
	 	if (!document.querySelector(`input[name="es-attr-${i}-a"]`)) {
	 		continue;
	 	}
	 	const area = document.querySelector(`input[name="es-attr-${i}-a"]`).value;
	 	// If the area is not null, add it to the total area
	 	if (area) {
	 		totalArea += parseFloat(area);
	 	}
	}	
	document.getElementById('form-total-area').innerHTML = `分區總面積：${totalArea} [m2]`;
}

// ====================================================================================================
//
// Add a new row to the ES exclusive table
//
// ====================================================================================================

function addEnergySectionExclusive() {

    // Select the div
	const Div = document.getElementById('energy-sections-exclusive');

	// Create a new row
	const newRow = document.createElement('div');
	newRow.id = `energy-section-exclusive-${energySectionCount}`;
	newRow.innerHTML = `
		<div style="width: 100%; margin: 1em 0 1em 0;">
			<div style="width: 35%; float: left;">
				<label class="form-label-2">免評估分區</label>
				<select class="form-input-2" name="es-exclusive-id-${energySectionCount}" onchange="esExclusiveIdChange(${energySectionCount})" aria-label="es-exclusive-id-${energySectionCount}">
		` + es_exclusive_option + `
				</select>
			</div>
			<div style="width: 40%; float: left;">
				<div name="form-es-exclusive-attr-${energySectionCount}" style="flex-direction: column; display: flex;"></div>
			</div>
			<div style="width: 20%; float: right;">
				<button class="form-button-dynamic-delete" type="button" onclick="removeEnergySectionExclusive(${energySectionCount})">刪除</button>
			</div>
		</div>
		<hr style="clear: both;">
	`;
	Div.appendChild(newRow);
	energySectionCount++;
}


// ====================================================================================================
//
// Remove a row from the ES exclusive table
//
// ====================================================================================================

function removeEnergySectionExclusive(sectionIndex) {
	const Div = document.getElementById('energy-sections-exclusive');
	const removedRow = document.querySelector(`#energy-section-exclusive-${sectionIndex}`);
	Div.removeChild(removedRow);
}

// ====================================================================================================
//
// Clear all rows from the ES exclusive table
//
// ====================================================================================================

function clearEnergySectionsExclusive() {
	const Div = document.getElementById('energy-sections-exclusive');
	Div.innerHTML = '';
	energySectionCount = 0;
}

// ====================================================================================================
//
// ES exclusive ID change
//
// ====================================================================================================

function esExclusiveIdChange(sectionIndex) {
	// Select the div
	const form = document.querySelector(`div[name="form-es-exclusive-attr-${sectionIndex}"]`);
	// Get the selected value
	const esId = document.querySelector(`select[name="es-exclusive-id-${sectionIndex}"]`).value;
	
	// Clear the form
	form.innerHTML = ``;

	// Create the new form
	switch (esId) {
		case "N1-1-1": case "N1-1-2": case "N1-2-1": case "N1-2-2": case "N1-3-1": case "N1-3-2": case "N1-4-1": case "N1-4-2": case "N1-5": case "N1-6": case "N1-7":
			// Collect area (kitchen)
			form.innerHTML = `
				<div>
					<label class="form-label-2">專用廚房面積</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-a" placeholder="m2" required>
				</div>
			`
			break;
		case "N3-1-1": case "N3-1-2": case "N3-2-1": case "N3-2-2": case "N3-3-1": case "N4-1": case "N4-2": case "N4-3":
			// Collect area
			form.innerHTML = `
				<div>
					<label class="form-label-2">分區面積</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-a" placeholder="m2" required>
				</div>
			`
			break;
		case "N5":
			// Collect area (refrigeration)
			form.innerHTML = `
				<div>
					<label class="form-label-2">冷藏室面積</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-a" placeholder="m2" required>
				</div>
			`
			break;
		case "N6":
				// Collect area (freezing)
				form.innerHTML = `
					<div>
						<label class="form-label-2">冷凍室面積</label>
						<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-a" placeholder="m2" required>
					</div>
				`
				break;
		case "N2-1-1": case "N2-1-2":
			// Collect number of hotel rooms and annual ratio of room usage
			form.innerHTML = `
				<div>
					<label class="form-label-2">洗衣負責客房數量</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-n_hotelroom" placeholder="客房數量" required>
				</div>
				<div>
					<label class="form-label-2">年住房率</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-coef_usage_r_hotelroom" placeholder="介於 0 至 1" min="0" max="1" step="0.01" required>
				</div>
			`
			break;
		case "N2-2":
			// Collect number of hospital beds and annual bed usage
			form.innerHTML = `
				<div>
					<label class="form-label-2">洗衣負責病床數量</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-n_hospitalbed" placeholder="病床數量" required>
				</div>
				<div>
					<label class="form-label-2">年住房率</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-coef_uage_r_hospitalbed" placeholder="介於 0 至 1" min="0" max="1" step="0.01" required>
				</div>
			`
			break;
		case "N2-1-3":
			// Collect area of dining area and number of meals per day
			form.innerHTML = `
				<div>
					<label class="form-label-2">洗衣（餐具廚具等）負責用餐區面積</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-a" placeholder="m2" required>
				</div>
				<div>
					<label class="form-label-2">每天提供餐數</label>
					<select class="form-input-3" name="es-exclusive-attr-${sectionIndex}-n_meal_per_day" aria-label="es-exclusive-attr-${sectionIndex}-n_meal_per_day">
						<option disabled selected>選擇每天提供餐數</option>
						<option value="1">每日一餐</option>
						<option value="2">每日兩餐</option>
						<option value="3">每日三餐</option>
					</select>
				</div>
			`
			break;
		case "N7":
			// Collect area and annual usage
			form.innerHTML = `
				<div>
					<label class="form-label-2">休閒設施面積</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-a" placeholder="m2" required>
				</div>
				<div>
					<label class="form-label-2">全年營運時數</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-coef_usage_h" placeholder="h/year" min="0" max="8760" step="1" required>
				</div>
			`
			break;
		case "N8":
			// Collect area and power of cabinet rack
			form.innerHTML = `
				<div>
					<label class="form-label-2">機房面積</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-a" placeholder="m2" required>
				</div>
				<div>
					<label class="form-label-2">機房機櫃功率</label>
					<input class="form-input-3" type="number" name="es-exclusive-attr-${sectionIndex}-datacenter-coef_power_cabinetrack" placeholder="kW" required>
				</div>
			`
			break;
	}
}