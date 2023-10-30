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
                    items: 1
                },
                1000: {
                    items: 3
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


// loadPdf

// scrollToSection
function scrollToSection(targetId) {
    var section = document.getElementById(targetId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}



function getServerUrl() {
    var serverUrl = window.location.protocol + "//" + window.location.host;
    return serverUrl;
}

function submitForm(event, loc, form) {
    event.preventDefault(); // Prevent the default form submission behavior
    var form = document.getElementById(form);
    var url = getServerUrl() + loc;
    form.action = url;
    form.method = 'post';
    form.submit();
}

function checkTS(check, butt) {
    var checkbox = document.getElementById(check);
    var button = document.getElementById(butt);

    checkbox.addEventListener('change', function () {
        button.disabled = !checkbox.checked;
    });
}



function uploading() {
    // console.log('test')
    let file = document.getElementById('file')
    let name = document.getElementById('name')
    let fileInput = file.files;


    let datePicker = document.getElementById('datePicker')
    let datePickerL = document.getElementById('datePickerL')
    let btnUpload = document.getElementById('inputfile')
    name.textContent = 'File Name: ' + fileInput[0].name;
    name.style.display = 'block';
    // console.log('pdf' in fileInput[0].name);
    if (fileInput.length > 0) {
        datePicker.style.display = "block";
        datePickerL.style.display = "block";
        btnUpload.style.display = "none";
    }
    else {
        datePicker.style.display = "none";
        datePickerL.style.display = "none";
        btnUpload.style.display = "block";
    }
}



function updateSchedule() {
    let schedule = document.getElementById('datePicker');
    let date = document.getElementById('dateL');
    date.textContent = 'Start Time: ' + schedule.value;
    date.style.display = 'block';
    let datePicker = document.getElementById('datePicker')
    let datePickerL = document.getElementById('datePickerL')
    let send = document.getElementById('button')

    datePicker.style.display = "none";
    datePickerL.style.display = "none";
    send.style.display = "block";


};


function checkFileUpload(file, pic, name) {

    var fileInput = document.createElement('input');
    fileInput.type = 'file';

    fileInput.addEventListener('change', function (event) {
        var file = event.target.files[0];
        console.log('Selected file:', file);
    });

    fileInput.click();
    var fileInput = document.getElementById('input');
    var uploadedFile = fileInput.files[0]; // Get the first file from the file input
    document.getElementById(file).textContent = "send";
    document.getElementById(pic).style.display = 'block';
    document.getElementById(name).textContent = uploadedFile.name;
    document.getElementById(name).style.display = 'block';
    if (uploadedFile) {
        // File has been uploaded, show the other button or perform your desired action
        console.log("onchange");

        document.getElementById(file).textContent = "send";
        document.getElementById(pic).style.display = 'block';
        document.getElementById(name).textContent = uploadedFile.name;
        document.getElementById(name).style.display = 'block';

    }

}



var loadFile = function (event, elementId) {
    var image = document.getElementById(elementId);
    image.src = URL.createObjectURL(event.target.files[0]);
};

const signUpGoogle = () => {
    let googleImage = document.getElementById('signupGoogle');
    googleImage.onclick = () => { location.href = '/auth/google'; }
}
// signUpGoogle();



const acceptRequest = function (event, myVariable, target) {
    let data = {
        variable: myVariable
    };
    fetch(target, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
        .then(response => response.json)
        .then(data => {
            window.location.reload()
        })


};

const showLessonData = async (event, target) => {
    let selected = event.target.selectedIndex
    id = event.target.options[selected].value
    try {
        const response = await fetch(`${target}/${id}`);
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log('Received data:', data);
        console.log('Received data1:', data.lessonLoc);
        let lectureName = document.getElementById('lectureName')
        let lectureDate = document.getElementById('lectureDate')
        let lectureStudent = document.getElementById('lectureStudent')
        let lectureStudentEmail = document.getElementById('lectureStudentEmail')
        let lectureButton = document.getElementById('lectureButton')
        let lectureButton2 = document.getElementById('lectureButton2')

        lectureName.textContent = data['lessonName'];
        lectureName.href = data['lessonLoc'];
        lectureName.target = 'blank_'
        lectureDate.textContent = data['username'];
        lectureStudent.textContent = data['email'];
        lectureStudentEmail.textContent = data['date'];

        if (data['state'] == 1) {
            lectureButton.classList.add('invisible')
            lectureButton2.classList.add('invisible')
        }
        else if (data['state'] == 2) {
            lectureButton2.classList.remove('invisible')
            lectureButton.classList.remove('invisible')

        }
        else {
            lectureButton.classList.add('invisible')
            lectureButton2.classList.add('invisible')

        }
    } catch (error) {
        console.error('Error:', error);
    }
};

function updateDateInput() {
    var today = new Date().toISOString().split('T')[0];
    var datePicker = document.getElementById('datePicker');
    datePicker.setAttribute('min', today);
    if (datePicker.value <= today) {
        datePicker.value == today;
    }
    datePicker.style.display = 'none';
}
window.onload = updateDateInput;
document.getElementById('datePicker').addEventListener('change', updateDateInput);





function finishLesson(event){
    let state = prompt('Are you sure for deleting this course?, you can not undo this action!\n type DELETE to confirm')
    if (state == 'DELETE'){
        alert('press ok to continue')
        submitForm(event,'/finish_lesson','selectLessonForm')
    }
    else{
        alert('the finish lesson process is canceled')
    }
}