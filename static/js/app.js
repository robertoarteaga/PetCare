$(document).ready(function(){
    $(window).scroll(function(){
      var scroll = $(window).scrollTop();
      if (scroll >= 700) {
        $(".blue-scroll").css("color" , "#2c3645", "important");
      }
      if (scroll < 700) {
        $(".blue-scroll").css("color" , "#edfaff", "important");
      }
      
    })
})