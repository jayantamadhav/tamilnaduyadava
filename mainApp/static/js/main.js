$(document).ready(function() {
	$(".navbar-burger").click(function() {
			// Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
			$(".navbar-burger").toggleClass("is-active");
			$(".navbar-menu").toggleClass("is-active");
		});
	$('#file-input').on('change', function(){ //on file input change
		if (window.File && window.FileReader && window.FileList && window.Blob) //check File API supported browser
		{
			$('#thumb-output').html(''); //clear html of output element
			var data = $(this)[0].files; //this file data
			$.each(data, function(index, file){ //loop though each file
				if(/(\.|\/)(gif|jpe?g|png)$/i.test(file.type)){ //check supported file type
					var fRead = new FileReader(); //new filereader
					fRead.onload = (function(file){ //trigger function on successful read
						return function(e) {
							$('.avatar').attr({'src':e.target.result, 'height':"128px", 'width':"128px"})
							//var img = $('<img/>').addClass('thumb').attr({'src' : e.target.result, 'height':"128px", 'width':"128px"}); //create image element 
							//$('#thumb-output').append(img); //append image to output element
						};
					})(file);
					fRead.readAsDataURL(file); //URL representing the file's data.
				}
			});				
		}
		else{
			alert("Your browser doesn't support File API!"); //if File API is absent
		}
	});
	$('#profile-update').on('change', function(){ //on file input change
		$('#manage_pic').submit()
	});
	$('#horoscope-update').on('change', function(){ //on file input change
		$('#manage-horoscope').submit()
	});
	$("#file-upload").on('change', function(){
		var file = $(this)[0].files[0].name;
		$('#file-label').text(file);
	});
	$('.dropdown').on('click', function(){
		$(this).toggleClass('is-active');
		$('div button span i', this).toggleClass('fa-angle-down fa-angle-up');
	});

	//MANAGE PROFILE
	$(".edit").on("click", function() {
		$('.modal').addClass('is-active');
		var field = "";
		field = $(this).attr('data-tag');
		var new_data = '';
		if(
			field == "name" 				|| field == "dob" 			|| field == "occupation" ||
			field == "religion"  			|| field == "caste" 		|| field == "mother_prof" ||
			field == "physical_disability" 	|| field == "complexion" 	|| field == "phone1" ||
			field == "city" 				|| field == "state" 		|| field == "native_city" || 
			field == "native_state" 		|| field == "father_name" 	|| field == "father_prof" || 
			field == "mother_name"
			)
		{
			var html = '<input type="text" class="input" id="new-data" placeholder="Enter new details">';
			$('#modal-control').html(html);
		}
		else if(field == "salary" || field == "phone2"){
			var html = '<input type="number" class="input numbers" id="new-data" placeholder="Enter only the numbers..">';
			$('#modal-control').html(html);
		}
		else if(field == "height" || field == "weight"){
			var html = '<input type="number" class="input height-weight" id="new-data" placeholder="Enter only the numbers..">';
			$('#modal-control').html(html);
		}
		else if(field == "education"){
			var html = '<div class="select"><select  id="new-data"><option>Secondary</option><option>Higher Secondary</option><option>Under Graduate</option><option>Post Graduate</option><option>Ph.D</option><option>Self Taught</option></select></div>';
			$('#modal-control').html(html);
		}
		else if(field == "rasi"){
			var html = '<div class="select is-fullwidth"><select  id="new-data"><option> Mesham </option><option> Rishabam </option><option> Mithunam </option><option> Kadakam </option><option> Simham </option><option> Kanni </option><option> Tulam </option><option> Vrischikam </option><option> Dhanusu </option><option> Makaram </option><option> Kumbham </option><option> Meenam </option></select></div>';
			$('#modal-control').html(html);
		}
		else if(field == "nakshatra"){
			var html = '<div class="select is-fullwidth"><select  id="new-data"><option>Aswini</option><option>Bharani</option><option>Karthigai</option><option>Rohini</option><option>Mrigasheersham</option><option>Thiruvaathirai</option><option>Punarpoosam</option><option>Poosam</option><option>Aayilyam</option><option>Makam</option><option>Pooram</option><option>Uthiram</option><option>Hastham</option><option>Chithirai</option><option>Swaathi</option><option>Visaakam</option><option>Anusham</option><option>Kettai</option><option>Moolam</option><option>Pooraadam</option><option>Uthiraadam</option><option>Thiruvonam</option><option>Avittam</option><option>Sadayam</option><option>Poorattathi</option><option>Uthirattathi</option><option>Revathi</option></select></div>';
			$('#modal-control').html(html);
		}
		else if(field == "marital_status"){
			var html = '<div class="select"><select  id="new-data"><option>Not Married</option><option>Divorced</option><option>Widow</option><option>Other reason</option></select></div>';
			$('#modal-control').html(html);
		}
		else if(field == "bio"){
			var html = '<textarea class="textarea" id="new-data" placeholder="Update bio.."></textarea>';
			$('#modal-control').html(html);
		}
		else if(field == "sibling_bro" || field == "sibling_bro_married" || field == "sibling_sis" || field == "sibling_sis_married"){
			var html = '<div class="select"><select  id="new-data"><option>None 0</option><option>1</option><option>2</option><option>3</option><option>4</option><option>5</option></select></div>';
			$('#modal-control').html(html);
		}
		$('#update').on('click', function(){
			new_data = $('#new-data').val();
			$.ajax(
			{
				type: "POST",
				async: "true",
				cache:"false",
				url: 'ajax_profile_update',
				data: {
					'new_data' : new_data,
					'field' : field,
				},
				success: function(data){
					alert("Updated!");
					$('.modal').removeClass('is-active');
					$('#'+field).text(new_data);
					location.reload();
				},
				error:function(data){
					alert("Make sure you've entered correct format.");
				}
			})
		});
	});

	//removes the "active" class to .popup and .popup-content when the "Close" button is clicked 
	$("#close").on("click", function() {
		$('.modal').removeClass('is-active');
		//$(".popup-overlay, .popup-content").removeClass("active");	
	});
	$(document).on('keypress', '.numbers', function(key) {
		if(key.charCode < 48 || key.charCode > 57) return false;
		if($(this).val().length > 9) return false;
	});
	$(document).on('keypress', '.height-weight', function(key) {
		if(key.charCode < 48 || key.charCode > 57) return false;
		if($(this).val().length > 2) return false;
	});

});
