console.log("landing_page.js loaded successfully.")

window.onload = function() {
    console.log("Window loaded.");

    let submit_btn = document.getElementById("signup-submit-btn")
    console.log(submit_btn);
    submit_btn.onclick = function() {
        console.log("Signup submit clicked.");
        let data = {
            "first_name": document.getElementsByClassName("signup-first").item(0).value,
            "last_name": document.getElementsByClassName("signup-last").item(0).value,
            "email": document.getElementsByClassName("signup-email").item(0).value
        }

        fetch("/_submit_signup_form", {
            method: "POST",
            body: JSON.stringify(data),
        }).then(response => response.json())
        .then(jsonData =>
            swal({
              title: `Thanks!`,
              html: `
              <hr>
              <div class="contact-modal-text">
                Choose from the options below to get updates about Mosaic.
              </div>
              <div class="contact-modal-options">
                <input type="checkbox" id="contact-modal-notify"> Notify me when Mosaic is available to the public!</input><br>
                <input type="checkbox" id="contact-modal-updates"> Send me regular updates about Mosaic. (1 per month or fewer)</input><br>
                <input type="checkbox" id="contact-modal-beta"> Please contact me about trying a beta version of Mosaic.<br>(permanent discount applies)</input><br>
              </div>
              <div class="contact-modal-unsub-notice">You can unsubscribe from our update emails any time.</div>
              `,
              type: 'success',
              confirmButtonColor: '#3085d6',
              confirmButtonText: 'Continue'
            }).then((result) => {
              if (result.value) {
                post_contact_preferences()
              }
            })
        ).catch(err => {
            console.log("Signup form data could not be posted to the server.")
        });
    };
};

function post_contact_preferences() {
    let data = {
        "email": document.getElementsByClassName("signup-email").item(0).value,
        "notify": document.getElementById("contact-modal-notify").checked,
        "updates": document.getElementById("contact-modal-updates").checked,
        "beta": document.getElementById("contact-modal-beta").checked
    }

    fetch("/_submit_contact_preferences", {
            method: "POST",
            body: JSON.stringify(data),
    }).then(response => response.json())
    .then(jsonData => console.log(jsonData));
};