document.addEventListener("DOMContentLoaded", function () {
  const sections = document.querySelectorAll(".section[id]");
  const navLinks = document.querySelectorAll('.sidebar-nav a[href^="#"]');

  // Function to remove active class from all nav links
  function removeActiveClasses() {
    navLinks.forEach((link) => link.classList.remove("active"));
  }

  // Function to add active class to current section link
  function addActiveClass(id) {
    removeActiveClasses();
    const activeLink = document.querySelector(`.sidebar-nav a[href="#${id}"]`);
    if (activeLink) {
      activeLink.classList.add("active");
    }
  }
  
  const observerOptions = {
    root: null,
    rootMargin: "-20% 0px -70% 0px", // Trigger when section is in the middle third of viewport
    threshold: 0,
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        addActiveClass(entry.target.id);
      }
    });
  }, observerOptions);

  // Observe all sections
  sections.forEach((section) => {
    observer.observe(section);
  });

  // Handle click events for smooth scrolling
  navLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      e.preventDefault();
      const targetId = this.getAttribute("href").substring(1);
      const targetSection = document.getElementById(targetId);

      if (targetSection) {
        // Calculate offset to account for fixed header
        const headerOffset = 100; // Adjust this value based on your header height
        const elementPosition = targetSection.offsetTop;
        const offsetPosition = elementPosition - headerOffset;

        window.scrollTo({
          top: offsetPosition,
          behavior: "smooth",
        });

        // Manually set active class
        addActiveClass(targetId);
      }
    });
  });

  // Set initial active state
  if (sections.length > 0) {
    addActiveClass(sections[0].id);
  }
});
