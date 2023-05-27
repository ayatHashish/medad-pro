// function validateLoginForm(event) {
//     event.preventDefault(); // Prevent form submission
//     // Retrieve form input values
//     var emailInput = document.getElementById('email');
//     var passwordInput = document.getElementById('password');

//     // Perform validation checks
//     var email = emailInput.value;
//     var password = passwordInput.value;

//     if (email === 'mohamed') {
//         console.log('Email');
//         alert('Please enter your username.');
//         emailInput.focus();
//         return;
//     }

//     if (password === '') {
//         alert('Please enter your password.');
//         passwordInput.focus();
//         return;
//     }

//     alert('Login successful!');
//     // Reset the form if needed
//     document.getElementById('loginForm').reset();
// }


$(document).ready(function () {

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
    }

    let btn = document.querySelector(".burger-mune")
    let nav = document.querySelector(".editnav")
    let close = document.querySelector(".editnav .close")

    btn.addEventListener("click", function () {
        nav.classList.toggle("trans")
    })
    close.addEventListener("click", function () { nav.classList.toggle("trans") })

});



// (function () {
//     function passwordCount(value, peak) {
//         value = typeof value === 'string' ? value : '';
//         peak = isFinite(peak) ? peak : 7;

//         return value && (value.length > peak ? peak + '+' : value.length);
//     }

//     function zxcvbnScore() {
//         var compute = zxcvbn.apply(null, arguments);
//         return compute && compute.score;
//     }

//     function okPasswordDirective(zxcvbn) {
//         return {
//             restrict: 'AC',
//             require: 'ngModel',
//             link: function (scope, element, attrs, ngModelCtrl) {
//                 element.on('blur change keydown', function (evt) {
//                     scope.$evalAsync(function (scope) {
//                         var pwd = scope.password = element.val();
//                         scope.passwordStrength = pwd ? (pwd.length > 7 && zxcvbn.score(pwd) || 0) : null;
//                         ngModelCtrl.$setValidity('okPassword', scope.passwordStrength >= 2);
//                     });
//                 });
//             }
//         };
//     }

//     var formController = function () {

//     };
//     var passwordStrengthModule = {
//         passwordCount: passwordCount,
//         zxcvbnScore: zxcvbnScore,
//         okPasswordDirective: okPasswordDirective,
//         formController: formController
//     };

//     // تعيين الدوال ككائن على النطاق العام
//     window.PasswordStrength = passwordStrengthModule;
// })();

// form-login 
