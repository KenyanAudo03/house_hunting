// FAQ Toggle Functionality
document.querySelectorAll(".faq-question").forEach((question) => {
  question.addEventListener("click", () => {
    const faqItem = question.parentElement;
    const answer = faqItem.querySelector(".faq-answer");
    const icon = question.querySelector("i");

    // Close other open FAQs
    document.querySelectorAll(".faq-item").forEach((item) => {
      if (item !== faqItem && item.classList.contains("active")) {
        item.classList.remove("active");
        item.querySelector(".faq-answer").style.maxHeight = null;
        item.querySelector(".faq-question i").style.transform = "rotate(0deg)";
      }
    });

    // Toggle current FAQ
    faqItem.classList.toggle("active");

    if (faqItem.classList.contains("active")) {
      answer.style.maxHeight = answer.scrollHeight + "px";
      icon.style.transform = "rotate(180deg)";
    } else {
      answer.style.maxHeight = null;
      icon.style.transform = "rotate(0deg)";
    }
  });
});

// Search Functionality (basic)
document
  .getElementById("supportSearch")
  .addEventListener("input", function (e) {
    const searchTerm = e.target.value.toLowerCase();
    const faqItems = document.querySelectorAll(".faq-item");

    faqItems.forEach((item) => {
      const question = item
        .querySelector(".faq-question h4")
        .textContent.toLowerCase();
      const answer = item
        .querySelector(".faq-answer p")
        .textContent.toLowerCase();

      if (question.includes(searchTerm) || answer.includes(searchTerm)) {
        item.style.display = "block";
      } else {
        item.style.display = searchTerm === "" ? "block" : "none";
      }
    });
  });

// Smooth scrolling for help links
document.querySelectorAll(".help-link").forEach((link) => {
  link.addEventListener("click", function (e) {
    e.preventDefault();
    const targetId = this.getAttribute("href");
    const targetElement = document.querySelector(targetId);

    if (targetElement) {
      targetElement.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    }
  });
});
