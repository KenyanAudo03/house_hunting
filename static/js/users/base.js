const navToggle = document.getElementById("navToggle");
const sidebar = document.getElementById("sidebar");
const overlay = document.getElementById("overlay");
const desktopProfile = document.getElementById("desktopProfile");
const sidebarClose = document.getElementById("sidebarClose");

// Close sidebar function
function closeSidebar() {
  sidebar.classList.remove("active");
  overlay.classList.remove("active");
}

function handleResize() {
  if (window.innerWidth >= 1024) {
    closeSidebar();
  }
}

window.addEventListener("resize", handleResize);
handleResize();

if (navToggle) {
  navToggle.addEventListener("click", () => {
    sidebar.classList.toggle("active");
    overlay.classList.toggle("active");
    if (sidebar.classList.contains("active")) {
      sidebar.classList.add("slide-in");
    }
  });
}

if (sidebarClose) {
  sidebarClose.addEventListener("click", closeSidebar);
}

if (overlay) {
  overlay.addEventListener("click", closeSidebar);
}

// Desktop profile dropdown
if (desktopProfile) {
  desktopProfile.addEventListener("click", (e) => {
    e.stopPropagation();
    desktopProfile.classList.toggle("active");
  });

  document.addEventListener("click", () => {
    desktopProfile.classList.remove("active");
  });
}

// Close sidebar on 'Escape' key press
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape") {
    closeSidebar();
    if (desktopProfile) {
      desktopProfile.classList.remove("active");
    }
  }
});
