function confirmAction(action, object)  {

    var message = '** Are you sure you wish to ' + action + ' this ' + object + '? **';

    box = confirm(message);

    if (box == true) {
        return true;
    }

    else {
        return false;
    }
}

function showHideEle(hide, show) { 
	if (hide != null) {
		document.getElementById(hide).style.display = "none";
	}
	
	if (show != null)  {
		document.getElementById(show).style.display = "block";
	}
}

// load field names and default values into list
	var defaultVals = new Array();
	defaultVals[0] = new Array("hs_day", "DD");
	defaultVals[1] = new Array("hs_month", "MM");
	defaultVals[2] = new Array("hs_year", "YYYY");
	defaultVals[3] = new Array("he_day", "DD");
	defaultVals[4] = new Array("he_month", "MM");
	defaultVals[5] = new Array("he_year", "YYYY");

// populate fields with default values on page load
function MPLoadDefaults(thisForm) {
	with (document.forms[thisForm]) {
		for (var n=0; n<defaultVals.length; n++) {
			var thisField = defaultVals[n][0];
			var thisDefault = defaultVals[n][1]; 
			if (elements[thisField].value == '') { 
					elements[thisField].value = thisDefault;
			 }
		  }
    } 
} 

 // clear default value from field when selected
function MPClearField(field) {
	 var fieldName = field.name;
	 for (var n=0; n<defaultVals.length; n++) {
		 var thisField = defaultVals[n][0];
		 var thisDefault = defaultVals[n][1];
		 if (thisField == fieldName) {
			 if (field.value == thisDefault) field.value = '';
			 break;
		 }
	}
}

// clear all defaults when form is submitted
function MPClearAll(thisForm) {
	 with (document.forms[thisForm]) {
		 for (var n=0; n<defaultVals.length; n++) {
			 var thisField = defaultVals[n][0];
			 var thisDefault = defaultVals[n][1];
			 if (elements[thisField].value == thisDefault){
				 elements[thisField].value = '';
			}
		 }
	}
}

function MPCReload (field) {
	 var fieldName = field.name;
	 for (var n=0; n<defaultVals.length; n++) {
		 var thisField = defaultVals[n][0];
		 var thisDefault = defaultVals[n][1];
		 if (thisField == fieldName) {
			 if (field.value == "" ) field.value = thisDefault;
			 break;
		 }
	}
}
