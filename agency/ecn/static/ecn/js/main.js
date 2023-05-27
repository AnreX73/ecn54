
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

});

