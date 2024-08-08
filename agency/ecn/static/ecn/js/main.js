
document.addEventListener('DOMContentLoaded', function() {
const swiper = new Swiper('.object-gallery', {
  // Optional parameters
//  direction: 'vertical',

  // If we need pagination
  pagination: {
    el: '.swiper-pagination',
    clickable:true,
    dynamicBullets: true,
   
  },
  effect:'flip',
  speed:1000,
  loop: true,
  grabCursor:true,

        // mousewheel:{
        //   eventTarget:".object-gallery",
        // },

  // Navigation arrows
  navigation: {
    nextEl: '.swiper-button-next',
    prevEl: '.swiper-button-prev',
  },

  // And if we need scrollbar
  scrollbar: {
    el: '.swiper-scrollbar',
  },
});

function divideNumberByPieces(x, delimiter) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, delimiter || "`");
}

var slider = document.getElementById("myRange");
var output = document.getElementById("demo");



var square_slider = document.getElementById("mySquareRange");
var square_output = document.getElementById("square_demo");

if(slider){
output.innerHTML = divideNumberByPieces(slider.value);
slider.oninput = function() {
  output.innerHTML =divideNumberByPieces(this.value);
}
}

if(square_slider){
square_output.innerHTML = square_slider.value;
square_slider.oninput = function() {
  square_output.innerHTML =this.value;
}
}




});

