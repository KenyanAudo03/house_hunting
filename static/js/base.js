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
