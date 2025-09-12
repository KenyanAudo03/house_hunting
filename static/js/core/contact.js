document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector(".contact-form");
  const submitBtn = form.querySelector("button[type=submit]");
  const successOverlay = document.getElementById("successOverlay");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Disable button and show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<div class="loading-spinner"></div>Sending...';

    // Gather form data
    const formData = new FormData(form);
    const data = {
      first_name: formData.get("first_name"),
      last_name: formData.get("last_name"),
      email: formData.get("email"),
      phone: formData.get("phone") || "",
      subject: formData.get("subject"),
      message: formData.get("message"),
    };

    try {
      // Send request to backend
      const response = await fetch("/contact/submit-contact-inquiry/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": getCsrfToken(),
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        // Small delay to show loading effect
        await new Promise((resolve) => setTimeout(resolve, 3000));

        // Show success message and lock scrolling
        successOverlay.style.display = "flex";
        document.body.style.overflow = "hidden";
        form.reset();

        // Hide message after 4 seconds
        setTimeout(() => {
          successOverlay.style.display = "none";
          document.body.style.overflow = "auto";
        }, 4000);
      } else {
        throw new Error("Submission failed");
      }
    } catch (error) {
      console.error("Error:", error);
      alert("There was an error submitting your message. Please try again.");
    } finally {
      // Restore button
      submitBtn.disabled = false;
      submitBtn.innerHTML = '<i class="bx bx-send"></i> Send Message';
    }
  });

  // Get CSRF token from input or cookie
  function getCsrfToken() {
    const csrfToken = document.querySelector("[name=csrfmiddlewaretoken]");
    if (csrfToken) {
      return csrfToken.value;
    }

    const cookies = document.cookie.split(";");
    for (let cookie of cookies) {
      const [name, value] = cookie.trim().split("=");
      if (name === "csrftoken") {
        return value;
      }
    }
    return "";
  }
});
