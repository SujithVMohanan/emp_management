"use strict";
var SigninGeneral = function () { // Elements
    var form;
    var submitButton;
    var validator;

    // Handle form
    var handleForm = function (e) {
        validator = FormValidation.formValidation(form, {
            fields: {
                'username': {
                    validators: {
                        notEmpty: {
                            message: 'Username is required'
                        },
                        regexp: {
                            regexp: /^[^\s]+$/,
                            message: 'Username cannot contain spaces'
                        }
                    }
                },
                'password': {
                    validators: {
                        notEmpty: {
                            message: 'The password is required'
                        }
                    }
                }
            },
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                bootstrap: new FormValidation.plugins.Bootstrap5(
                    { rowSelector: '.fv-row' }
                )
            }
        });

        // Handle form submit
        submitButton.addEventListener('click', function (e) { // Prevent button default action
            e.preventDefault();

            // Validate form
            validator.validate().then(function (status) {
                if (status == 'Valid') { // Show loading indication
                    submitButton.setAttribute('data-kt-indicator', 'on');

                    // Disable button to avoid multiple click
                    submitButton.disabled = true;


                    // Simulate ajax request
                    

                    // Enable button
                    submitButton.disabled = false;
                    let username = form.querySelector('[name="username"]').value
                    let password = form.querySelector('[name="password"]').value
                    
                    $.post(`${api_config.authentication_url}`, {
                        username: username,
                        password: password
                    }, function (data, status, xhr) {

                        if (data.status_code == 100) {
                            // Swal.fire({
                            //     text: data.message,
                            //     icon: "success",
                            //     buttonsStyling: false,
                            //     confirmButtonText: "Ok, got it!",
                            //     customClass: {
                            //         confirmButton: "btn btn-primary"
                            //     }
                            // }).then(function (result) {

                            //     if (result.isConfirmed) {
                                    
                            //     }
                            // });
                            form.querySelector('[name="username"]').value = "";
                            form.querySelector('[name="password"]').value = "";

                            var redirectUrl = form.getAttribute('data-redirect-url');
                            if (redirectUrl) {
                                location.href = redirectUrl;
                            }
                        } else {
                            Swal.fire({
                                text: data.message,
                                icon: "error",
                                buttonsStyling: false,
                                confirmButtonText: "Ok, got it!",
                                customClass: {
                                    confirmButton: "btn btn-primary"
                                }
                            });
                        }

                    }, 'json').done(function () {
                        submitButton.removeAttribute('data-kt-indicator');
                        console.log('Request done!');
                    }).fail(function (jqxhr, settings, ex) {
                        console.log('failed, ' + ex);
                    });


                } else {
                    Swal.fire({
                        text: "Please Enter Username and Password.",
                        icon: "error",
                        buttonsStyling: false,
                        confirmButtonText: "Ok, got it!",
                        customClass: {
                            confirmButton: "btn btn-primary"
                        }
                    });
                }
            });
        });
    }

    // Public functions
    return { // Initialization
        init: function () {
            form = document.querySelector('#_sign_in_form');
            submitButton = document.querySelector('#_sign_in_submit');

            handleForm();
        }
    };
}();

KTUtil.onDOMContentLoaded(function () {
    SigninGeneral.init();
});