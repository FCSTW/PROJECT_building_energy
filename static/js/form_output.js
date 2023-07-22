function saveAsJSON() {
	var formData = JSON.stringify($("#form-main").serializeArray());
	window.alert(formData);
}