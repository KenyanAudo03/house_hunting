document.addEventListener("DOMContentLoaded", function () {
  const favoriteBtn = document.getElementById("favorite-btn");

  if (favoriteBtn) {
    favoriteBtn.addEventListener("click", function () {
      const hostelId = this.dataset.hostelId;

      fetch(`/users/favorites/${hostelId}/toggle/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": getCookie("csrftoken"),
          "X-Requested-With": "XMLHttpRequest",
        },
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.success) {
            const heartIcon = this.querySelector("i");
            if (data.favorited) {
              heartIcon.className = "bx bxs-heart";
              this.title = "Remove from favorites";
            } else {
              heartIcon.className = "bx bx-heart";
              this.title = "Add to favorites";
            }
          } else {
            alert(data.error || "Something went wrong");
          }
        })
        .catch((error) => console.error("Error:", error));
    });
  }

  // Helper: get CSRF token from cookies
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});
