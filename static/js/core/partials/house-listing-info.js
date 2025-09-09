document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("propertyForm");
  const submitBtn = document.getElementById("submitBtn");
  const successOverlay = document.getElementById("successOverlay");

  form.addEventListener("submit", async function (e) {
    e.preventDefault();

    // Disable button and show loading state
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<div class="loading-spinner"></div>Submitting...';

    // Gather form data
    const formData = new FormData(form);
    const data = {
      name: formData.get("name"),
      contact: formData.get("contact"),
      role: formData.get("role"),
      area: formData.get("area"),
      rent: formData.get("rent"),
      hostel: formData.get("hostel") || "",
    };

    try {
      // Send request to backend
      const response = await fetch("/submit-property-listing/", {
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
      alert("There was an error submitting your listing. Please try again.");
    } finally {
      // Restore button
      submitBtn.disabled = false;
      submitBtn.innerHTML = "Submit";
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
