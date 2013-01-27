
/* Function to create
   an ajax http request object
   depending on the browswer being 
   used  
*/
function createAjaxRequest()
{
  var xmlHttp;
  try
  {
    // Firefox, Opera 8.0+, Safari
    xmlHttp=new XMLHttpRequest();
  }
  catch (e)
  {
    // Internet Explorer
    try
    {
      xmlHttp=new ActiveXObject("Msxml2.XMLHTTP");
    }
    catch (e)
    {
      try
      {
        xmlHttp=new ActiveXObject("Microsoft.XMLHTTP");
      }
      catch (e)
      {
      	alert("Your browser does not support AJAX!");
        return false;
      }
    }
  }
  return xmlHttp
}
//
// This method provides an ajax mechanism to generate 
// a new password. It makes a database call that
// ensures the password is not being used by someone
// else.
//
function genPassword(element_id)
{
	// create ajax request
	request = createAjaxRequest();

	if (request != null)
	{
		// Get all issues associated to the category
		url = urlrel +"admin/genpass/" ;
		
		// Show the issues once we have retrieved them		
		request.onreadystatechange = function() {
			if (request.readyState == 4) {
				var response = request.responseText;

				var pass_span = document.getElementById(element_id+'_span');
				var pass_form = document.getElementById(element_id+'_form');

				pass_span.innerHTML = response;
				pass_form.value = response;
			}		
		}
		request.open("GET",url);
		request.send(null);
	}
}

function getusers(select_element, target_id)
{
	// create ajax request
	request = createAjaxRequest();

	if (request != null)
	{
		var selectedIndex = select_element.selectedIndex;
		var domain = select_element.options[selectedIndex].value


		// Get all users of this domain 
		url = urlrel +"admin/domain/"+domain+"/userget/" ;
		
		// Show the issues once we have retrieved them		
		request.onreadystatechange = function() {
			if (request.readyState == 4) {
				var response = request.responseText;

				var usersrow = document.getElementById(target_id);
				usersrow.innerHTML = response;

			}		
		}
		request.open("GET",url);
		request.send(null);
	}
	
}

function postusers(target_id, prev_domain, prev_users)
{
	// create ajax request
	request = createAjaxRequest();
	if (request != null)
	{
		params = "users="+prev_users
		domain = prev_domain 
		// Get all users of this domain 
		url = urlrel +"admin/domain/"+domain+"/userget/" ;
		
		// Show the issues once we have retrieved them		
		request.onreadystatechange = function() {
			if (request.readyState == 4) {
				var response = request.responseText;

				var usersrow = document.getElementById(target_id);
				usersrow.innerHTML = response;

			}		
		}
		request.open("POST",url);
		request.send(params);
	}
	
}
