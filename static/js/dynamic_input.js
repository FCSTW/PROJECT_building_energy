
// ====================================================================================================
//
// Building type changed
//
// ====================================================================================================

// When the building type is changed to apartment, enable the input named "n_suite" and "n_household_big".
// Otherwise, disable them.

function buildingTypeChange() {

    const building_type = document.getElementsByName("building_type")[0].value;
    
    if (building_type == "apartment") {

        // Enable the input named "n_suite" and "n_household_big"
        document.getElementsByName("n_suite")[0].disabled = false;
        document.getElementsByName("n_household_big")[0].disabled = false;

    } else {
        
        // Clear the input value and disable the input named "n_suite" and "n_household_big"
        document.getElementsByName("n_suite")[0].value = "";
        document.getElementsByName("n_household_big")[0].value = "";
        document.getElementsByName("n_suite")[0].disabled = true;
        document.getElementsByName("n_household_big")[0].disabled = true;

    }
}