
function createCalendar(div_id, function_name, anchorname){
	var calendar = new CalendarPopup(div_id);
	calendar.setReturnFunction(function_name);
	anchor = document.getElementById(anchorname);
	calendar.showCalendar(anchorname);
}
function setStartDate(y,m,d) {
	document.forms[0].hs_year.value = y;
	document.forms[0].hs_month.value = LZ(m);
	document.forms[0].hs_day.value = LZ(d);
}

function setEndDate(y,m,d) {
	document.forms[0].he_year.value = y;
	document.forms[0].he_month.value = LZ(m);
	document.forms[0].he_day.value = LZ(d);
}
