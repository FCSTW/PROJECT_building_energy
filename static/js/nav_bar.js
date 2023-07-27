function scrollToAnchor(anchorId) {
	const anchorElement = document.getElementById(anchorId);
	if (anchorElement) {
		anchorElement.scrollIntoView({ behavior: 'smooth' });
	}
}