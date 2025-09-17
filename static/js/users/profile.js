// Check if user is on mobile device
function isMobile() {
  return /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
    navigator.userAgent
  );
}

// Sanitize input by escaping dangerous HTML characters
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

function containsDangerousChars(input) {
  return /[<>"'&]/.test(input);
}

function formHasDangerousChars(form) {
  const inputs = form.querySelectorAll(
    'input[type="text"], input[type="tel"], textarea'
  );
  return Array.from(inputs).some((input) =>
    containsDangerousChars(input.value)
  );
}

// Update save button state based on form validation
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

// Update character count for textarea with validation
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
    const form = textarea.closest("form");
    if (form && !formHasDangerousChars(form)) {
      updateSaveButtonState(form);
    }
  }
}

// Show upload progress modal overlay
function showUploadProgress() {
  const existingOverlay = document.getElementById("upload-progress-overlay");
  if (existingOverlay) existingOverlay.remove();

  const overlay = document.createElement("div");
  overlay.id = "upload-progress-overlay";
  overlay.style.cssText = `
    position: fixed; top: 0; left: 0; width: 100%; height: 100%;
    background: rgba(0, 0, 0, 0.8); display: flex; flex-direction: column;
    justify-content: center; align-items: center; z-index: 10000; font-family: inherit;
  `;

  const progressContainer = document.createElement("div");
  progressContainer.style.cssText = `
    background: white; padding: 30px; border-radius: 12px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3); text-align: center;
    min-width: 300px; max-width: 400px;
  `;

  const uploadIcon = document.createElement("div");
  uploadIcon.innerHTML =
    '<i class="bx bx-cloud-upload" style="font-size: 48px; color: #4CAF50; margin-bottom: 16px;"></i>';

  const statusText = document.createElement("div");
  statusText.id = "upload-status-text";
  statusText.style.cssText =
    "font-size: 16px; font-weight: 500; color: #333; margin-bottom: 20px;";
  statusText.textContent = "Uploading your profile picture...";

  const progressBarContainer = document.createElement("div");
  progressBarContainer.style.cssText = `
    width: 100%; height: 8px; background: #e0e0e0;
    border-radius: 4px; overflow: hidden; margin-bottom: 16px;
  `;

  const progressBar = document.createElement("div");
  progressBar.id = "upload-progress-bar";
  progressBar.style.cssText = `
    height: 100%; width: 0%; background: linear-gradient(90deg, #4CAF50, #45a049);
    border-radius: 4px; transition: width 0.3s ease;
  `;

  const progressPercent = document.createElement("div");
  progressPercent.id = "upload-progress-percent";
  progressPercent.style.cssText =
    "font-size: 14px; color: #666; font-weight: 500;";
  progressPercent.textContent = "0%";

  progressBarContainer.appendChild(progressBar);
  progressContainer.appendChild(uploadIcon);
  progressContainer.appendChild(statusText);
  progressContainer.appendChild(progressBarContainer);
  progressContainer.appendChild(progressPercent);
  overlay.appendChild(progressContainer);
  document.body.appendChild(overlay);

  return overlay;
}

function hideUploadProgress() {
  const overlay = document.getElementById("upload-progress-overlay");
  if (overlay) {
    overlay.style.opacity = "0";
    setTimeout(() => overlay.remove(), 300);
  }
}

function updateProgress(percent) {
  const progressBar = document.getElementById("upload-progress-bar");
  const progressPercent = document.getElementById("upload-progress-percent");

  if (progressBar) progressBar.style.width = percent + "%";
  if (progressPercent) progressPercent.textContent = Math.round(percent) + "%";
}

function showUploadSuccess() {
  const statusText = document.getElementById("upload-status-text");
  const uploadIcon = document.querySelector("#upload-progress-overlay i");

  if (statusText) {
    statusText.textContent = "Profile picture updated successfully!";
    statusText.style.color = "#4CAF50";
  }

  if (uploadIcon) uploadIcon.className = "bx bx-check-circle";

  updateProgress(100);
  setTimeout(() => hideUploadProgress(), 1500);
}

function showUploadError(message = "Upload failed. Please try again.") {
  const statusText = document.getElementById("upload-status-text");
  const uploadIcon = document.querySelector("#upload-progress-overlay i");

  if (statusText) {
    statusText.textContent = message;
    statusText.style.color = "#f44336";
  }

  if (uploadIcon) {
    uploadIcon.className = "bx bx-error-circle";
    uploadIcon.style.color = "#f44336";
  }

  setTimeout(() => hideUploadProgress(), 3000);
}

// Handle profile picture upload with validation and progress
function submitProfilePicture() {
  const fileInput = document.getElementById("file-input");
  const file = fileInput.files[0];

  if (!file) return;

  const allowedTypes = [
    "image/jpeg",
    "image/jpg",
    "image/png",
    "image/gif",
    "image/webp",
  ];
  const maxSize = 5 * 1024 * 1024;

  if (!allowedTypes.includes(file.type)) {
    alert("Please select a valid image file (JPEG, PNG, GIF, WebP)");
    fileInput.value = "";
    return;
  }

  if (file.size > maxSize) {
    alert("File size must be less than 5MB");
    fileInput.value = "";
    return;
  }

  showUploadProgress();

  const formData = new FormData();
  formData.append("profile_picture", file);
  const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;
  const xhr = new XMLHttpRequest();

  xhr.upload.addEventListener("progress", function (e) {
    if (e.lengthComputable) {
      const percentComplete = (e.loaded / e.total) * 100;
      updateProgress(percentComplete);
    }
  });

  xhr.addEventListener("load", function () {
    if (xhr.status === 200) {
      showUploadSuccess();
      setTimeout(() => {
        window.location.reload();
      }, 1500);
    } else {
      showUploadError("Server error. Please try again.");
    }
  });

  xhr.addEventListener("error", () => {
    showUploadError("Network error. Please check your connection.");
  });

  xhr.addEventListener("timeout", () => {
    showUploadError("Upload timeout. Please try again.");
  });

  xhr.open("POST", document.getElementById("profilePictureForm").action, true);
  xhr.setRequestHeader("X-CSRFToken", csrfToken);
  xhr.timeout = 30000;
  xhr.send(formData);
  fileInput.value = "";
}

// Open modal and initialize date picker for personal info modal
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

// Close modal and clean up error states
function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  modal.classList.remove("active");
  document.body.classList.remove("modal-open");

  const usernameError = document.getElementById("username-error");
  if (usernameError) usernameError.style.display = "none";

  const emailError = document.getElementById("email-error");
  if (emailError) emailError.style.display = "none";

  if (modalId === "editPersonalModal") {
    const dateInput = document.getElementById("date_of_birth");
    if (dateInput && dateInput._flatpickr) {
      dateInput._flatpickr.destroy();
    }
  }
}

// Check if username is available via AJAX
function checkUsername() {
  const username = document.getElementById("username").value;
  const currentUsername = "{{ user.username }}";
  const errorElement = document.getElementById("username-error");

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
    .catch((error) => console.error("Error:", error));
}

// Check if email is available via AJAX
function checkEmail() {
  const email = document.getElementById("email").value;
  const currentEmail = "{{ user.email }}";
  const errorElement = document.getElementById("email-error");

  if (email === currentEmail || email === "") {
    errorElement.style.display = "none";
    return;
  }

  const emailPattern = /^[^@]+@[^@]+\.[^@]+$/;
  if (!emailPattern.test(email)) {
    errorElement.textContent = "Invalid email format";
    errorElement.style.display = "block";
    return;
  }

  fetch("/users/check-email/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
    },
    body: JSON.stringify({ email: email }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.exists) {
        errorElement.textContent = "Email already exists";
        errorElement.style.display = "block";
      } else {
        errorElement.style.display = "none";
      }
    })
    .catch((error) => console.error("Error:", error));
}

// Validate form on submit with comprehensive checks
function validateForm(event) {
  const form = event.target;
  const inputs = form.querySelectorAll(
    'input[type="text"], input[type="tel"], textarea'
  );

  const hasDangerous = formHasDangerousChars(form);
  if (hasDangerous) {
    event.preventDefault();
    alert(
      "Please remove special characters (<, >, ', \", &) before submitting"
    );
    return false;
  }

  const bioTextarea = form.querySelector(
    'textarea[name*="bio"], textarea[id*="bio"], #bio'
  );
  if (bioTextarea && bioTextarea.value.length > 500) {
    event.preventDefault();
    alert("Bio must be 500 characters or less");
    bioTextarea.focus();
    return false;
  }

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

// Show visual warning for inputs with dangerous characters
function showSecurityWarning(input) {
  const form = input.closest("form");

  if (containsDangerousChars(input.value)) {
    input.style.borderColor = "#ff6b6b";
    input.title = "Special characters will be sanitized when you submit";
  } else {
    input.style.borderColor = "";
    input.title = "";
  }

  if (form) updateSaveButtonState(form);
}

// Initialize event listeners when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  const usernameInput = document.getElementById("username");
  if (usernameInput) usernameInput.addEventListener("input", checkUsername);

  const emailInput = document.getElementById("email");
  if (emailInput) emailInput.addEventListener("input", checkEmail);

  const allForms = document.querySelectorAll("form");
  allForms.forEach((form) => {
    form.addEventListener("submit", validateForm);
    updateSaveButtonState(form);
  });

  const textInputs = document.querySelectorAll(
    'input[type="text"], input[type="tel"], textarea'
  );
  textInputs.forEach((input) => {
    input.addEventListener("input", function () {
      showSecurityWarning(this);
    });
  });

  const bioTextareas = document.querySelectorAll(
    'textarea[name*="bio"], textarea[id*="bio"], #bio'
  );
  bioTextareas.forEach((textarea) => {
    textarea.setAttribute("maxlength", "500");
    updateCharCount(textarea);
    textarea.addEventListener("input", function () {
      updateCharCount(this);
      showSecurityWarning(this);
    });
  });
});

// Close modal when clicking overlay
document.addEventListener("click", function (e) {
  if (e.target.classList.contains("modal-overlay")) {
    e.target.classList.remove("active");
    document.body.classList.remove("modal-open");
  }
});

// Close modal on Escape key
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    const activeModal = document.querySelector(".modal-overlay.active");
    if (activeModal) closeModal(activeModal.id);
  }
});
