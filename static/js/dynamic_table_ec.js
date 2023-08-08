
// ====================================================================================================
//
// EC input type change
//
// ====================================================================================================

// If the select box select_ec is changed, the content of building-ec div will be changed.
function ecInputTypeChange(select_ec) {

    // Variable declaration
    // Get the element of building-ec div
    const buildingEc = document.getElementById('building-ec');

    // Determine the type of ec input
    if (select_ec == 'direct') {

        buildingEc.innerHTML = `
            <label class="form-label-1">建物能耗</label>
            <input class="form-input-1" type="text" placeholder="建物能耗 [kWh/year]" required name="ec">
        `;

    } else if (select_ec == 'monthly') {

        buildingEc.innerHTML = `
            <label class="form-label-1">月電費</label>
        `;

        let monthlyInput = ``;
        for (let i = 1; i <= 24; i++) {
            monthlyInput = monthlyInput + `
                <input class="form-input-4" type="text" placeholder="第 ${i} 個月建物能耗 [kWh]" required name="ec_monthly_${i}" onchange="ecValueValidation('monthly')">
            `;
        }
        buildingEc.innerHTML = buildingEc.innerHTML + `
            <div style="flex-direction: column; display: flex;">`
        + monthlyInput + `
            </div>
        `;

    } else if (select_ec == 'bimonthly') {

        buildingEc.innerHTML = `
            <label class="form-label-1">雙月電費</label>
        `;
        
        let monthlyInput = ``;
        for (let i = 1; i <= 12; i++) {
            monthlyInput = monthlyInput + `
                <input class="form-input-4" type="text" placeholder="第 ${i*2-1}~${i*2} 個月建物能耗 [kWh]" required name="ec_bimonthly_${i*2-1}" onchange="ecValueValidation('bimonthly')">
            `
        }
        buildingEc.innerHTML = buildingEc.innerHTML + `
            <div style="flex-direction: column; display: flex;">`
        + monthlyInput + `
            </div>
        `;
    }

    // Clear the alert message in building-ec-message div
    document.getElementById('building-ec-message').innerHTML = '';
}