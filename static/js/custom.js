// protect against csrf
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

  // start of jquery script
  //like script

$(document).ready(function(){
  $('select').formSelect();
  $('#datepicker').datepicker();
  // var date = $('#datepicker').val();
  // console.log(date);
  // if (top.location.pathname === "/lecturer_dashboard"){
  //   M.toast({html:'logged in',classes:''})
  // }
  // moment js
  $('.due_date').each(function(index){
    var date = $(this).text();
    var due_date = moment(date,'MMMM Do, YYYY').fromNow();
    // change the date
    $(this).text(due_date);
  });

  $('.name').click(function(event){
    M.toast({html: 'I am a toast!',classes:'red'})
    console.log('data');
  })



// Account creation 
$('.sign_up').on('submit', function(event){
  event.preventDefault();
  var username = $('#id_username').val();
  var email = $('#id_email').val();
  var password = $('#id_password').val();

  console.log(username, email, password);
  M.toast({html: "Creating account...",classes:''});
  $.ajax({
    url: '/sign_up',
    type: 'POST',
    data: { username: username,
            email: email,
            password:password,
    },
    success:function(data){
      $("#id_password").val('');
      if(data.not_created){
        $('#id_username').css("border", "1px solid #e71d36");
        M.toast({html: "Contact the ICT department",classes:'red'});
      } else if (data.created){
        $('#id_username').css("border", "1px solid #4CAF50");
        M.toast({html: "Your account has been created. <a href='accounts/login/' style='color: white;text-decoration: underline'>You need to login now</a>",classes:''});

        window.setTimeout(reload_page, 5000);
        function reload_page() {
            window.location = "/accounts/login/";
          }
      } else if (data.user_exists){
        $('#id_username').css("border", "1px solid #e71d36");
        M.toast({html: "You already have an account... Please login.",classes:''});
      }
    },
    error:function(xhr,errmsg,err){
      console.log(errmsg,err)
      M.toast({html: "Can't create an account",classes:''});
    }
  });
});

  // get user units from the server 
  var user_units = [];
  var selected;
  $(document).ready(function(){ 
    var i;
    $.ajax({
      url: '/student_get_units',
      async: false,
      success:function(data){
        var i;
        var l = data.length;
        for(i=0;i<l;++i){
          user_units.push(data[i]);
        }
      } 
    })
    // looping through the DOM highlighting the user units
    $('.unit_container').each(function(){
      var id = this.id;
      var this_container = $(this);
      var i;
      var l = user_units.length;
      for(i=0;i<l;++i){
          if(user_units[i] === id){
            this_container.addClass('unit_container_selected');
          }
        }
    });
  });

// select the unit
$('.unit_container').click(function(){
  $('.save_changes').css("background-color", "#2ec4b6");
    var id = this.id;
  if($(this).hasClass("unit_container_selected")){
    // remove unit from the array && not the last element in the array(pop)
    $(this).removeClass("unit_container_selected");
    user_units = jQuery.grep(user_units,function(value){
      return value != id;
    });
  } else{
    // add unit to the array (at the end) 
     $(this).addClass("unit_container_selected");
     user_units.push(id);
  }
  selected = user_units.length;
  console.log(user_units)
  M.toast({html: selected + " units selected",classes:''});
});



// Send the units changes the server
var $modal = $('#modal');
$('.save_changes').click(function(){
  var final = user_units;
  console.log(final)
  M.toast({html: "Updating unit...",classes:''});
  $.ajax({
  url: '/student_edit_units',
  type: 'POST',
  data: {'data':final},
  success:function(data){
    if(data.changes_saved){
      M.toast({html: selected + " Units saved",classes:''});
    }
    window.setTimeout(reload_page, 1000);
      function reload_page() {
          window.location = "/student_dashboard";
        } 
  },
  error:function(xhr,errmsg,err){
    M.toast({html: "Cannot save units, Try Again",classes:'red'});
    }
})
});


// handle lec units api
$('.get_units').on('submit', function(event){
  event.preventDefault();
  
  $('.all_units').empty();
  // get the api values
  var course = $('#id_course').val();
  var year = $('#id_year').val();
  var semester = $('#id_semester').val();
  var course_code = this.id;

  $.ajax({
    url: '/lec_get_units/'+course+"/"+year+"/"+semester,
    type: 'POST',
    success:function(data){
      if (data.no_units){
        $('.all_units').append("<p class='no_parameters'>No units Found</p>");
        M.toast({html: 'No units found!',classes:'red'});

      } else {
        var count = Object.keys(data).length;
        M.toast({html: count +' units found!',classes:''});
        for (const unit_code in data) {
          if (data.hasOwnProperty(unit_code)) {
            const element = data[unit_code];
            $('.all_units').append("<p class='lec_unit_details' id='"+element.unit_code+"'><span class='unit_sem'>Semester "+element.semester+"</span>"+element.unit_code+": "+element.unit_name+"</p>") 
          }
        }
      }
      
    },
    error:function(xhr,errmsg,err){
      console.log(xhr)
      }
  })
});

// add units to the lec model
$(document).on('click', '.lec_unit_details', function(){
  var course_code = this.id;
  
  $.ajax({
    url: '/lecturer_add_units',
    type: 'POST',
    data: {course_code ,course_code},
    success:function(data){
      if(data.saved){
        M.toast({html: course_code + " Unit saved",classes:''});
        $('.lec_units').empty();
        data.lec_units.forEach(unit => {
          $('.lec_units').append("<div class='unit_chip'>"+unit+"<span class='del_lec_unit' id='"+unit+"'>&times;</span></div>")
        });
        
      } else {
        M.toast({html: course_code + " Unit already exists",classes:'red'});
      }
    },
    error:function(xhr,errmsg,err){
      M.toast({html: 'Cannot save unit',classes:'red'});
      }
  })
});

//remove units from the lec model
$(document).on('click', '.del_lec_unit', function(){
  var course_code= this.id;
  $.ajax({
    url: '/lecturer_remove_units',
    type: 'POST',
    data: {course_code ,course_code},
    success:function(data){
      if(data.removed){
        M.toast({html: course_code + " Unit Removed",classes:'red'});
        $('.lec_units').empty();
        data.lec_units.forEach(unit => {
          $('.lec_units').append("<div class='unit_chip'>"+unit+"<span class='del_lec_unit' id='"+unit+"'>&times;</span></div>")
        });
      }
    },
    error:function(xhr,errmsg,err){
      M.toast({html: 'Cannot remove unit',classes:'red'});
      }
  })
});

// lec give assignments
$('.collection-item').click(function(){
  $('.collection-item.active').removeClass('active');
  $(this).addClass('active');
  var unit_code = $(this).text();
  $( "#id_unit_code" ).val(unit_code);
});

// delete assign action
$('.del_btn').on("click", function(){
  var id = this.id;
  if (confirm("You are about to delete an assignment.\nClick the OK to confirm")) {
    $.ajax({
      url: '/lec_del_assign/'+id+'/',
      type: 'POST',
      success:function(data){
        if(data.deleted){
          M.toast({html:"Assignment Removed",classes:'red'});
          window.location = "/lec_view_assignments";
        }
      }
    })
  } 
});


$('.find_lecturer').on('submit', function(event){
  event.preventDefault();
  var q = $('#q').val();

  $.ajax({
    url: '/find_lecturer',
    type: 'POST',
    data: {q ,q},
      success:function(data){
        console.log(data)
        $('#search_results').empty();
        var count = Object.keys(data).length;
        if (count >= 2){
          M.toast({html: count +' Lecturers found',classes:''});
        } else if(count == 0){
          $('#search_results').append('No Lecturers found');
          M.toast({html: 'No Lecturers found',classes:'red'});
        } else if(count == 1){
          M.toast({html: count +' Lecturer found',classes:''});
        }
        for (const lec in data) {
          if (data.hasOwnProperty(lec)) {
            const element = data[lec];
            $('#search_results').append('<div class="lec_container"><img src="static/img/avatar.png" class="float-center" alt="profile" width="100" height="100"><p>'+element.name+'</p><br><a href="tel:+1-303-499-7111" class="btn btn-flat btn-call">CALL</a><a href="mailto:someone@example.com" target="_top"class="float-right btn btn-flat btn-email">Email</a></div>') 
          }
        }
      }
  })
});

});

 // End of jquery script
