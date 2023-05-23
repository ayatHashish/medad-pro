
$(document).ready(function () {
  
    AOS.init({
        once: true,
         disable: "mobile"
   
   });



     setTimeout(function () {
        $('body').addClass('loaded');
        AOS.init({
            once: true,
            disable: function () {
                var maxWidth = 800;
                return window.innerWidth < maxWidth;
            }
        });

     }, 1500);
      loader();
    
          function loader(_success) {
            var obj = document.querySelector('.loader'),
            inner = document.querySelector('.preloader_inner'),
            page = document.querySelector('body');
            obj.classList.add('show');
            page.classList.remove('show');
            var w = 0,
                t = setInterval(function() {
                    w = w + 1;
                    inner.textContent = w+'%';
                    if (w === 100){
                        obj.classList.remove('show');
                        page.classList.add('show');
                        clearInterval(t);
                        w = 0;
                        if (_success){
                            return _success();
                        }
                    }
                }, 30);
        }


    if (document.documentElement.lang == 'en') {

        $('.banner-slide').owlCarousel({
            loop: true,
            items: 1,
            dots: true,
            slideSpeed: 10000,
            autoplaySpeed: 800,
            autoplayTimeout: 10000,
            autoplay: true,
            slideBy: 1,
        })
        $('.confernces-sec').owlCarousel({
            loop: true,
            nav: true,
            margin: 50,
            items: 3,
            dots: true,
            slideSpeed: 10000,
            autoplaySpeed: 800,
            autoplayTimeout: 10000,
            // autoplay: true,
            navText: [
                '<i class="fi-circle-arrow-left1"></i>',
                '<i class="fi-circle-arrow-right1"></i>'
            ],
            responsiveClass: true,
            responsive: {
                1200: { items: 3 },
                900: { items: 2 },
                700: { items: 2 },
                0: { items: 1 }
            }
        })
        $('.media-highlights').owlCarousel({
            loop: true,
            nav: true,
            margin: 50,
            items: 3,
            dots: true,
            slideSpeed: 10000,
            autoplaySpeed: 800,
            autoplayTimeout: 10000,
            autoplay: true,
            navText: [
                '<i class="fi-circle-arrow-left1"></i>',
                '<i class="fi-circle-arrow-right1"></i>'
            ],
            responsiveClass: true,
            responsive: {
                1200: { items: 3 },
                900: { items: 2 },
                700: { items: 2 },
                0: { items: 1 }
            }
        })

    } else {

        $('.banner-slide').owlCarousel({
            rtl: true,
            loop: true,
            items: 1,
            dots: true,
            slideSpeed: 10000,
            autoplaySpeed: 800,
            autoplayTimeout: 10000,
            autoplay: true,
            slideBy: 1,
        });
       
        $('.login-carousel').owlCarousel({
            loop:true,
            margin:10,
            nav:true,
            responsive:{
                0:{
                    items:1
                },
                600:{
                    items:3
                },
                1000:{
                    items:5
                }
            }
        })



    }

    let btn = document.querySelector(".burger-mune")
    let nav = document.querySelector(".editnav")
    let close = document.querySelector(".editnav .close")

    btn.addEventListener("click", function () {
        nav.classList.toggle("trans")
    })
    close.addEventListener("click", function () { nav.classList.toggle("trans") })

     });  


  

