// Detect mobile device
function isMobile() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
}

// Sanitize input (prevent XSS) - only for submission, not real-time
function sanitizeInput(input) {
  return input.replace(/[<>'"&]/g, function (match) {
    switch (match) {
      case "<":
        return "&lt;";
      case ">":
        return "&gt;";
      case '"':
        return "&quot;";
      case "'":
        return "&#x27;";
      case "&":
        return "&amp;";
      default:
        return match;
    }
  });
}

// Check if input contains potentially dangerous characters
function containsDangerousChars(input) {
  return /[<>"'&]/.test(input);
}

// Check if any form has dangerous characters
function formHasDangerousChars(form) {
  const inputs = form.querySelectorAll(
    'input[type="text"], input[type="tel"], textarea'
  );
  return Array.from(inputs).some((input) =>
    containsDangerousChars(input.value)
  );
}

// Update save button state
function updateSaveButtonState(form) {
  const saveButtons = form.querySelectorAll(
    'button[type="submit"], input[type="submit"]'
  );
  const hasDangerous = formHasDangerousChars(form);

  saveButtons.forEach((button) => {
    if (hasDangerous) {
      button.disabled = true;
      button.style.opacity = "0.5";
      button.style.cursor = "not-allowed";
      button.title =
        "Cannot save: form contains special characters that need to be removed";
    } else {
      button.disabled = false;
      button.style.opacity = "1";
      button.style.cursor = "pointer";
      button.title = "";
    }
  });
}

// Update character count for bio
function updateCharCount(textarea, maxLength = 500) {
  const currentLength = textarea.value.length;
  const remaining = maxLength - currentLength;

  let countElement = textarea.parentNode.querySelector(".char-count");
  if (!countElement) {
    countElement = document.createElement("div");
    countElement.className = "char-count";
    countElement.style.cssText =
      "font-size: 12px; color: #666; margin-top: 4px; text-align: right;";
    textarea.parentNode.appendChild(countElement);
  }

  if (remaining < 0) {
    countElement.innerHTML = `<span style="color: #ff6b6b;">${Math.abs(
      remaining
    )} characters over limit</span>`;
    countElement.style.color = "#ff6b6b";
    textarea.style.borderColor = "#ff6b6b";
    // Disable save buttons when over limit
    const form = textarea.closest("form");
    if (form) {
      const saveButtons = form.querySelectorAll(
        'button[type="submit"], input[type="submit"]'
      );
      saveButtons.forEach((button) => {
        button.disabled = true;
        button.style.opacity = "0.5";
        button.title =
          "Bio exceeds maximum length of " + maxLength + " characters";
      });
    }
  } else {
    countElement.textContent = `${remaining} characters remaining`;
    countElement.style.color = remaining < 50 ? "#ff6b6b" : "#666";
    textarea.style.borderColor = "";
    // Re-enable save buttons if no other issues
    const form = textarea.closest("form");
    if (form && !formHasDangerousChars(form)) {
      updateSaveButtonState(form);
    }
  }
}

// Open modal + init date picker
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.add("active");
  document.body.classList.add("modal-open");

  if (modalId === "editPersonalModal" && !isMobile()) {
    setTimeout(() => {
      const dateInput = document.getElementById("date_of_birth");
      if (dateInput && !dateInput.classList.contains("flatpickr-input")) {
        flatpickr(dateInput, {
          dateFormat: "Y-m-d",
          maxDate: "today",
          altInput: true,
          altFormat: "F j, Y",
          allowInput: false,
          clickOpens: true,
          theme: "light",
        });
      }
    }, 100);
  }
}

// Close modal + destroy date picker
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.remove("active");
  document.body.classList.remove("modal-open");

  document.getElementById("username-error").style.display = "none";

  if (modalId === "editPersonalModal") {
    const dateInput = document.getElementById("date_of_birth");
    if (dateInput && dateInput._flatpickr) {
      dateInput._flatpickr.destroy();
    }
  }
}

// Validate and submit profile picture
function submitProfilePicture() {
  const fileInput = document.getElementById("file-input");
  const file = fileInput.files[0];

  if (file) {
    const allowedTypes = ["image/jpeg", "image/jpg", "image/png", "image/gif"];
    const maxSize = 5 * 1024 * 1024; // 5MB

    if (!allowedTypes.includes(file.type)) {
      alert("Please select a valid image file (JPEG, PNG, GIF)");
      fileInput.value = "";
      return;
    }

    if (file.size > maxSize) {
      alert("File size must be less than 5MB");
      fileInput.value = "";
      return;
    }

    document.getElementById("profilePictureForm").submit();
  }
}

// Check username availability
function checkUsername() {
  const username = document.getElementById("username").value;
  const currentUsername = "{{ user.username }}";
  const errorElement = document.getElementById("username-error");

  // Don't sanitize here - just validate
  if (username === currentUsername || username === "") {
    errorElement.style.display = "none";
    return;
  }

  if (!/^[a-zA-Z0-9_@.+-]+$/.test(username)) {
    errorElement.textContent = "Invalid characters in username";
    errorElement.style.display = "block";
    return;
  }

  fetch("/users/check-username/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({ username: username }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.exists) {
        errorElement.textContent = "Username already exists";
        errorElement.style.display = "block";
      } else {
        errorElement.style.display = "none";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Validate form inputs - prevent submission if dangerous chars or bio too long
function validateForm(event) {
  const form = event.target;
  const inputs = form.querySelectorAll(
    'input[type="text"], input[type="tel"], textarea'
  );

  // Check for dangerous characters - prevent submission
  const hasDangerous = formHasDangerousChars(form);
  if (hasDangerous) {
    event.preventDefault();
    alert(
      "Please remove special characters (<, >, ', \", &) before submitting"
    );
    return false;
  }

  // Check bio length
  const bioTextarea = form.querySelector(
    'textarea[name*="bio"], textarea[id*="bio"], #bio'
  );
  if (bioTextarea && bioTextarea.value.length > 500) {
    event.preventDefault();
    alert("Bio must be 500 characters or less");
    bioTextarea.focus();
    return false;
  }

  // Sanitize inputs only during form submission (after validation)
  inputs.forEach((input) => {
    input.value = sanitizeInput(input.value);
  });

  const phoneInputs = form.querySelectorAll('input[type="tel"]');
  phoneInputs.forEach((input) => {
    if (
      input.value &&
      !/^[+]?[0-9]{10,15}$/.test(input.value.replace(/\s/g, ""))
    ) {
      event.preventDefault();
      alert("Invalid phone number");
      input.focus();
      return false;
    }
  });

  const nameInputs = form.querySelectorAll("#county, #town");
  nameInputs.forEach((input) => {
    if (input.value && !/^[a-zA-Z\s-']+$/.test(input.value)) {
      event.preventDefault();
      alert("Invalid location name");
      input.focus();
      return false;
    }
  });

  const areaInput = form.querySelector("#area_of_stay");
  if (
    areaInput &&
    areaInput.value &&
    !/^[a-zA-Z0-9\s-']+$/.test(areaInput.value)
  ) {
    event.preventDefault();
    alert("Invalid area name");
    areaInput.focus();
    return false;
  }

  const usernameInput = form.querySelector("#username");
  if (
    usernameInput &&
    usernameInput.value &&
    !/^[a-zA-Z0-9_@.+-]+$/.test(usernameInput.value)
  ) {
    event.preventDefault();
    alert("Invalid username format");
    usernameInput.focus();
    return false;
  }
}

// Show warning for potentially dangerous characters and update save button
function showSecurityWarning(input) {
  const form = input.closest("form");

  if (containsDangerousChars(input.value)) {
    input.style.borderColor = "#ff6b6b";
    input.title = "Special characters will be sanitized when you submit";
  } else {
    input.style.borderColor = "";
    input.title = "";
  }

  // Update save button state for the form
  if (form) {
    updateSaveButtonState(form);
  }
}

// DOM ready: attach events
document.addEventListener("DOMContentLoaded", function () {
  const usernameInput = document.getElementById("username");
  if (usernameInput) {
    usernameInput.addEventListener("input", checkUsername);
  }

  const allForms = document.querySelectorAll("form");
  allForms.forEach((form) => {
    form.addEventListener("submit", validateForm);
    // Initial save button state check
    updateSaveButtonState(form);
  });

  // Add event listeners for text inputs
  const textInputs = document.querySelectorAll(
    'input[type="text"], input[type="tel"], textarea'
  );
  textInputs.forEach((input) => {
    input.addEventListener("input", function () {
      showSecurityWarning(this);
    });
  });

  // Special handling for bio textarea (character count)
  const bioTextareas = document.querySelectorAll(
    'textarea[name*="bio"], textarea[id*="bio"], #bio'
  );
  bioTextareas.forEach((textarea) => {
    // Set max length attribute
    textarea.setAttribute("maxlength", "500");

    // Initial character count
    updateCharCount(textarea);

    textarea.addEventListener("input", function () {
      updateCharCount(this);
      showSecurityWarning(this);
    });
  });
});

// Close modal on overlay click
document.addEventListener("click", function (e) {
  if (e.target.classList.contains("modal-overlay")) {
    e.target.classList.remove("active");
    document.body.classList.remove("modal-open");
  }
});

// Close modal on ESC key
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    const activeModal = document.querySelector(".modal-overlay.active");
    if (activeModal) {
      const modalId = activeModal.id;
      closeModal(modalId);
    }
  }
});
