var swiper = new Swiper(".mySwiper", {
  speed: 250,
  spaceBetween: 15,
  initialSlide: 0,
  loop: false, 
  freeMode: true,
  cssWidthAndHeight: true,

  slidesPerView: 'auto',
  visibilityFullFit: true,
  autoResize: false,
  centeredSlides: false,
  observer: true,
  observeParents: true,


  navigation: {
  nextEl: '.swiper-button-next',
  prevEl: '.swiper-button-prev',
},

/*
on: {
slideChangeTransitionEnd: function (swiper) {
  console.log('is end:', swiper.activeIndex)
}
}
*/  
});
