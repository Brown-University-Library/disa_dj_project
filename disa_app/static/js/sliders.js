new Glider(document.querySelector('.glider-stories'), {
  slidesToShow: 1,
  slidesToScroll: 1,
  itemWidth: "5rem",
  exactWidth: false,
  arrows: {
    prev: ".is-glider-prev",
    next: ".is-glider-next"
  },
  responsive: [
  {
    breakpoint: 800,
    settings: {
      slidesToShow: 2
    }
  },
  {
    breakpoint: 1024,
    settings: {
      slidesToShow: 3,
      slidesToScroll: 2
    }
  }]
});

new Glider(document.querySelector('.glider-voices'), {
  slidesToShow: 1,
  slidesToScroll: 1,
  itemWidth: "5rem",
  exactWidth: false,
  arrows: {
    prev: ".is-glider-prev",
    next: ".is-glider-next"
  },
  responsive: [
  {
    breakpoint: 800,
    settings: {
      slidesToShow: 2
    }
  },
  {
    breakpoint: 1024,
    settings: {
      slidesToShow: 3,
      slidesToScroll: 2
    }
  }]
});

// hiding horizontal scrollbars in Firefox
document.addEventListener('glider-loaded', hideFFScrollBars);
document.addEventListener('glider-refresh', hideFFScrollBars);
function hideFFScrollBars(e){
  var scrollbarHeight = 17; // Currently 17, may change with updates
  if(/firefox/i.test(navigator.userAgent)){
    // We only need to appy to desktop. Firefox for mobile uses
    // a different rendering engine (WebKit)
    if (window.innerWidth > 575){
      e.target.parentNode.style.height = (e.target.offsetHeight - scrollbarHeight) + 'px'
    }
  }
}
