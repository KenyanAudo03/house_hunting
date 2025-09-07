const navToggle = document.getElementById("navToggle");
const sidebar = document.getElementById("sidebar");
const sidebarClose = document.getElementById("sidebarClose");
const overlay = document.getElementById("overlay");

// Open sidebar
function openSidebar() {
  sidebar.classList.add("open");
  overlay.style.display = "block";
  document.body.style.overflow = "hidden";
}

// Close sidebar
function closeSidebar() {
  sidebar.classList.remove("open");
  overlay.style.display = "none";
  document.body.style.overflow = "auto";
}

navToggle.addEventListener("click", openSidebar);
sidebarClose.addEventListener("click", closeSidebar);
overlay.addEventListener("click", closeSidebar);

document.addEventListener("keydown", function (e) {
  if (e.key === "Escape" && sidebar.classList.contains("open")) {
    closeSidebar();
  }
});

window.addEventListener("resize", function () {
  if (window.innerWidth > 768 && sidebar.classList.contains("open")) {
    closeSidebar();
  }
});

// Get current year
document.getElementById("currentYear").textContent = new Date().getFullYear();

const backToTop = document.getElementById("backToTop");

// Scroll back to top
window.addEventListener("scroll", function () {
  if (window.scrollY > 300) {
    backToTop.classList.add("visible");
  } else {
    backToTop.classList.remove("visible");
  }
});

backToTop.addEventListener("click", function () {
  window.scrollTo({
    top: 0,
    behavior: "smooth",
  });
});

// Profile dropdown functionality
const profileTrigger = document.getElementById("profileTrigger");
const profileDropdown = document.getElementById("profileDropdown");

if (profileTrigger && profileDropdown) {
  profileTrigger.addEventListener("click", function (e) {
    e.preventDefault();
    e.stopPropagation();

    const isOpen = profileDropdown.classList.contains("show");

    if (isOpen) {
      profileDropdown.classList.remove("show");
      profileTrigger.classList.remove("open");
    } else {
      profileDropdown.classList.add("show");
      profileTrigger.classList.add("open");
    }
  });

  document.addEventListener("click", function (e) {
    if (
      !profileTrigger.contains(e.target) &&
      !profileDropdown.contains(e.target)
    ) {
      profileDropdown.classList.remove("show");
      profileTrigger.classList.remove("open");
    }
  });

  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && profileDropdown.classList.contains("show")) {
      profileDropdown.classList.remove("show");
      profileTrigger.classList.remove("open");
    }
  });
}
