$(document).ready(function () {


    $('.home-services').owlCarousel({
        loop: true,
        margin: 15,
        nav: false,
        dots: true,
        center: true,
        slideSpeed: 5000,
        autoplaySpeed: 800,
        autoplayTimeout: 10000,
        autoplay: true,
        responsive: {
            0: {
                items: 1
            },
            600: {
                items: 3
            },
            1000: {
                items: 5
            }
        }
    });


   $("#courses-requistes").niceScroll({
         
            cursoropacitymin:"1",
            cursorwidth :"15px" ,
            bouncescroll: true

            
        });
});