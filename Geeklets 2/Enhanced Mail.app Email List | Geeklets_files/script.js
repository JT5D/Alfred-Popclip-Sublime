$(document).ready(function() {
	var baseUrl = "http://www.macosxtips.co.uk/geeklets";
	
	// Drop-down navigation
	$('ul.sf-menu').superfish({
		delay: 800,                      
		speed: 'fast',
		autoArrows: false,
		dropShadows: false
	});
	
	// Search
	$('#search').submit(function() {
		document.location.href=baseUrl+"/search/"+this.search.value.replace(/\//g,"|").replace(/\?/g,"%3F"); 
		return false;
	});
	
	// Subscribe/Follow tooltips
	$('#follow a').tipsy({fade: true});
	
	// Animate scroll to #anchors
	$.localScroll();

	// FancyBox modal popup links
	$(".modal").fancybox();

});