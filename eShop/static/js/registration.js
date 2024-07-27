const firstNameField = document.querySelector("#firstNameField");
const lastNameField = document.querySelector("#lastNameField");
const emailField = document.querySelector("#emailField");
const submitBtn = document.querySelector(".submit-btn");
const passwordField = document.querySelector("#passwordField");
const repeatPasswordField = document.querySelector("#repeatPasswordField");

// INVALID FEEDBACK
const firstNameFeedbackField = document.querySelector(
  ".invalid-firstNameFeedback"
    );
const lastNameFeedbackField = document.querySelector(
  ".invalid-lastNameFeedback"
    );
const emailFeedbackField = document.querySelector(
    ".invalid-emailFeedback"
    );
const passFeedbackField = document.querySelector(
    ".invalid-passwordFeedback"
    );

// FIRSTNAME
firstNameField.addEventListener("keyup", (e) => {
  const firstNameFieldValue = e.target.value;
  firstNameField.classList.remove("is-invalid");
  firstNameFeedbackField.style.display = "none";

  if (firstNameFieldValue.length > 0) {
    fetch("/authentication/validate-first-name", {
      body: JSON.stringify({ first_name: firstNameFieldValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.first_name_error) {
          firstNameField.classList.add("is-invalid");
          firstNameFeedbackField.style.display = "block";
          firstNameFeedbackField.innerHTML = `<p>${data.first_name_error}</p>`;
          lastNameField.disabled = true;
          emailField.disabled = true;
          passwordField.disabled = true;
          repeatPasswordField.disabled = true;
          submitBtn.disabled = true;
        } else {
          lastNameField.removeAttribute("disabled");
          emailField.removeAttribute("disabled");
          passwordField.removeAttribute("disabled");
          repeatPasswordField.removeAttribute("disabled");
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});
// LASTNAME
lastNameField.addEventListener("keyup", (e) => {
  const lastNameFieldValue = e.target.value;
  lastNameField.classList.remove("is-invalid");
  lastNameFeedbackField.style.display = "none";

  if (lastNameFieldValue.length > 0) {
    fetch("/authentication/validate-last-name", {
      body: JSON.stringify({ last_name: lastNameFieldValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.last_name_error) {
          lastNameField.classList.add("is-invalid");
          lastNameFeedbackField.style.display = "block";
          lastNameFeedbackField.innerHTML = `<p>${data.last_name_error}</p>`;
          firstNameField.disabled = true;
          emailField.disabled = true;
          passwordField.disabled = true;
          repeatPasswordField.disabled = true;
          submitBtn.disabled = true;
        } else {
          firstNameField.removeAttribute("disabled");
          emailField.removeAttribute("disabled");
          passwordField.removeAttribute("disabled");
          repeatPasswordField.removeAttribute("disabled");
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});

// EMAIL
emailField.addEventListener("keyup", (e) => {
  const emailFieldValue = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedbackField.style.display = "none";

  if (emailFieldValue.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailFieldValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          submitBtn.disabled = true;
          firstNameField.disabled = true;
          lastNameField.disabled = true;
          passwordField.disabled = true;
          repeatPasswordField.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedbackField.style.display = "block";
          emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          passwordField.removeAttribute("disabled");
          repeatPasswordField.removeAttribute("disabled");
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});
