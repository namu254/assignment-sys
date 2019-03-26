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

  $('.name').click(function(event){
    window.location ="/";
  })



// Account creation 
$('.sign_up').on('submit', function(event){
  event.preventDefault();
  var username = $('#id_username').val();
  var email = $('#id_email').val();
  var password = $('#id_password').val();

  console.log(username, email, password);
  $('.response').css("background-color", "#000000");
  $('.response').text("Creating account...");
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
        $('#id_username').css("border", "1px solid red");
        $('.response').css("background-color", "red");
        $('.response').text("Contact the ICT department");
      } else if (data.created){
        $('#id_username').css("border", "1px solid #4CAF50");
        $('.response').css("background-color", "#4CAF50");
        $('.response').html("Your account has been created. <a href='accounts/login/' style='color: white;text-decoration: underline'>You need to login now</a>");
        window.setTimeout(reload_page, 5000);
        function reload_page() {
            window.location = "/accounts/login/";
          }
      } else if (data.user_exists){
        $('#id_username').css("border", "1px solid red");
        $('.response').css("background-color", "red");
        $('.response').text("You already have an account... Please login.");
      }
    },
    error:function(xhr,errmsg,err){
      console.log(errmsg,err)
      $('.response').css("background-color", "red");
      $('.response').text(err);
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
  $('.response').css("background-color", "#ff9f1c");
  $('.response').text(selected + " units selected" );
});



// Send the units changes the server
var $modal = $('#modal');
$('.save_changes').click(function(){
  var final = user_units;
  console.log(final)
  $('.response').css("background-color", "#000000");
  $('.response').text("Updating unit...");
  $.ajax({
  url: '/student_edit_units',
  type: 'POST',
  data: {'data':final},
  success:function(data){
    if(data.changes_saved){
      $('.response').css("background-color", "#2ec4b6");
        $('.response').text(selected + "Units saved");
    }
    window.setTimeout(reload_page, 1000);
      function reload_page() {
          window.location = "/student_dashboard";
        } 
  },
  error:function(xhr,errmsg,err){
      $('.response').css("background-color", "#e71d36");
      $('.response').text(err);
    }
})
.done(function() {
  $modal.html(resp).foundation('open');
});
})



});

 // End of jquery script
