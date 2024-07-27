// VARIABLES
const firstNameField = document.querySelector("#firstNameField");
const lastNameField = document.querySelector("#lastNameField");
const emailField = document.querySelector("#emailField");
const passwordField = document.querySelector("#passwordField");
const emailFeedbackField = document.querySelector(".invalid-emailFeedback");
const submitBtn = document.querySelector(".submit-btn");

// INVALID FEEDBACK
const firstNameFeedbackField = document.querySelector(
  ".invalid-firstNameFeedback"
);
const lastNameFeedbackField = document.querySelector(
  ".invalid-lastNameFeedback"
);

// FIRSTNAME VALIDATION
firstNameField.addEventListener("keyup", (e) => {
  const firstNameFieldValue = e.target.value;

  firstNameSuccessOutput.style.display = "block";
  firstNameSuccessOutput.textContent = `Checking ${firstNameFieldValue}`;

  firstNameField.classList.remove("is-invalid");
  firstNameFeedbackField.style.display = "none";

  if (firstNameFieldValue.length > 0) {
    fetch("/authentication/validate-first-name", {
      body: JSON.stringify({ first_name: firstNameFieldValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        firstNameSuccessOutput.style.display = "none";
        if (data.first_name_error) {
          firstNameField.classList.add("is-invalid");
          firstNameFeedbackField.style.display = "block";
          firstNameFeedbackField.innerHTML = `<p>${data.first_name_error}</p>`;
        }
      });
  }
});

// LASTNAME VALIDATION
lastNameField.addEventListener("keyup", (e) => {
  const lastNameFieldValue = e.target.value;

  lastNameSuccessOutput.style.display = "block";
  lastNameSuccessOutput.textContent = `Checking ${lastNameFieldValue}`;

  lastNameField.classList.remove("is-invalid");
  firstNameFeedbackField.style.display = "none";

  if (lastNameFieldValue.length > 0) {
    fetch("/authentication/validate-last-name", {
      body: JSON.stringify({ last_name: lastNameFieldValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        lastNameSuccessOutput.style.display = "none";
        if (data.last_name_error) {
          lastNameField.classList.add("is-invalid");
          lastNameFeedbackField.style.display = "block";
          lastNameFeedbackField.innerHTML = `<p>${data.last_name_error}</p>`;
        }
      });
  }
});

// EMAIL
emailField.addEventListener("keyup", (e) => {
  const emailFieldValue = e.target.value;

  emailSuccessOutput.style.display = "block";
  emailSuccessOutput.textContent = `Checking ${emailFieldValue}`;

  emailField.classList.remove("is-invalid");
  emailFeedbackField.style.display = "none";

  if (emailFieldValue.length > 0) {
    fetch("/authentication/validate-email", {
      body: JSON.stringify({ email: emailFieldValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("data", data);
        emailSuccessOutput.style.display = "none";
        if (data.email_error) {
          submitBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedbackField.style.display = "block";
          emailFeedbackField.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          submitBtn.removeAttribute("disabled");
        }
      });
  }
});
