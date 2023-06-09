function isGood(password) {
    var password_strength = document.getElementById("password-text");

    //TextBox left blank.
    if (password.length == 0) {
        password_strength.innerHTML = "";
        return;
    }

    //Regular Expressions.
    var regex = new Array();
    regex.push("[A-Z]"); //Uppercase Alphabet.
    regex.push("[a-z]"); //Lowercase Alphabet.
    regex.push("[0-9]"); //Digit.
    regex.push("[$@$!%*#?&]"); //Special Character.

    var passed = 0;

    //Validate for each Regular Expression.
    for (var i = 0; i < regex.length; i++) {
        if (new RegExp(regex[i]).test(password)) {
            passed++;
        }
    }

    //Display status.
    var strength = "";
    switch (passed) {
        case 0:
        case 1:
            strength = "<small class='help-block-fill help-red-fill'></small>";
            break;
        case 2:
            strength = "<small class='help-block-fill help-orangered-fill'></small>";
            break;
        case 3:
            strength = "<small class='help-block-fill help-orange-fill'></small>";
            break;
        case 4:
            strength = "<small class='help-block-fill help-green-fill'></small>";
            break;

    }
    password_strength.innerHTML = strength;

}

$(document).ready(function () {
    AOS.init({
        once: true,
        disable: "mobile"
    });

    const navLinks = $('nav ul li a');
    const currentURL = window.location.pathname;
    const currentPath = currentURL.split(/[/_]/).filter(part => part !== '')[0];

    navLinks.each(function () {
        if ($(this).attr('onclick').indexOf(currentPath) !== -1) {
            $(this).addClass('active');
        }
    });

    $('#loginForm').submit(function (event) {
        event.preventDefault(); // Prevent form submission

        // Retrieve form input values
        var email = $('#email').val();
        var password = $('#password').val();
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        var passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

        let error = '';

        // Perform validation checks
        if (email === '') {
            error = 'Please enter your Email address';
            $('#loginForm .email-error').removeClass('d-none').html(error);
            $('#email').focus().addClass('input-error-danger');
        } else if (emailPattern.test(email)) {
            $('#loginForm .email-error').addClass('d-none');
            $('#email').focus().removeClass('input-error-danger');
        } else {
            error = 'Invalid email address';
            $('#loginForm .email-error').removeClass('d-none').html(error);
            $('#email').focus().addClass('input-error-danger');
        }

        if (password === '') {
            error = 'Please enter your password';
            $('#loginForm .password-error').removeClass('d-none').html(error);
            $('#password').focus().addClass('input-error-danger');
        } else if (passwordPattern.test(password)) {
            $('#loginForm .password-error').addClass('d-none');
            $('#password').focus().removeClass('input-error-danger');
        } else {
            error = 'Invalid password. Password must contain at least 8 characters, including letters and numbers';
            $('#loginForm .password-error').removeClass('d-none').html(error);
            $('#password').focus().addClass('input-error-danger');
        }

    });
    $('#signup').submit(function (event) {
        event.preventDefault(); // Prevent form submission

        // Retrieve form input values
        var email = $('#email').val();
        var fullname = $('#fullname').val();
        var password = $('#password').val();
        var emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        var passwordPattern = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$/;

        let error = '';

        // Perform validation checks

        if (fullname === '') {
            error = 'Please enter your Full Name';
            $('#signup .fullname-error').removeClass('d-none').html(error);
            $('#fullname').focus().addClass('input-error-danger');
        } else {
            $('#signup .fullname-error').addClass('d-none');
            $('#fullname').focus().removeClass('input-error-danger');
        }

        if (email === '') {
            error = 'Please enter your Email address';
            $('#signup .email-error').removeClass('d-none').html(error);
            $('#email').focus().addClass('input-error-danger');
        } else if (emailPattern.test(email)) {
            $('#signup .email-error').addClass('d-none');
            $('#email').focus().removeClass('input-error-danger');
        } else {
            error = 'Invalid email address';
            $('#loginForm .email-error').removeClass('d-none').html(error);
            $('#email').focus().addClass('input-error-danger');
        }

        if (password === '') {
            error = 'Please enter your Password.';
            $('#signup .password-error').removeClass('d-none').html(error);
            $('#password').focus().addClass('input-error-danger');
        } else if (passwordPattern.test(password)) {
            $('#signup .password-error').addClass('d-none');
            $('#password').focus().removeClass('input-error-danger');
        } else {
            error = 'Password must have at least 8 characters and contain Uppercase Alphabet ,Lowercase Alphabet,Special Characteras (@,!,#), and numbers .';

            $('#signup .password-error').removeClass('d-none').html(error);
            $('#password').focus().addClass('input-error-danger');
        }

    });

    setTimeout(function () {
        $('body').addClass('loaded');
        AOS.init({
            once: true,
            disable: function () {
                var maxWidth = 50;
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
            t = setInterval(function () {
                w = w + 1;
                inner.textContent = w + '%';
                if (w === 100) {
                    obj.classList.remove('show');
                    page.classList.add('show');
                    clearInterval(t);
                    w = 0;
                    if (_success) {
                        return _success();
                    }
                }
            }, 30);
    }
    console.log(document.documentElement.lang);

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
        });

        $('.service-carousel').owlCarousel({
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
                    items: 2
                },
                1000: {
                    items: 4
                }
            }
        });


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
            loop: true,
            margin: 10,
            nav: true,
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
        })

        // $('.owl-carousel').owlCarousel({
        //     loop: true,
        //     margin: 15,
        //     nav: false,
        //     dots: true,
        //     center: true,
        //     slideSpeed: 5000,
        //     autoplaySpeed: 800,
        //     autoplayTimeout: 10000,
        //     autoplay: true,
        //     responsive: {
        //         0: {
        //             items: 1
        //         },
        //         600: {
        //             items: 2
        //         },
        //         1000: {
        //             items: 4
        //         }
        //     }
        // });

    }

    let btn = document.querySelector(".burger-mune")
    let nav = document.querySelector(".editnav")
    let close = document.querySelector(".editnav .close")

    btn.addEventListener("click", function () {
        nav.classList.toggle("trans")
    })
    close.addEventListener("click", function () { nav.classList.toggle("trans") })

});

// image
var loadFile = function (event) {
    var image = document.getElementById("output");
    image.src = URL.createObjectURL(event.target.files[0]);
};

// loadPdf

// scrollToSection
function scrollToSection(targetId) {
    var section = document.getElementById(targetId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}