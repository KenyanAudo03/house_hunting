document.addEventListener("DOMContentLoaded", function () {
  // Main video and image elements
  const mainVideo = document.getElementById("mainVideo");
  const mainImage = document.getElementById("mainImage");
  const thumbnails = document.querySelectorAll(".thumbnail");
  const currentMediaNumber = document.getElementById("currentMediaNumber");
  const mediaItems = [];

  // Setup media items and thumbnail click behavior
  thumbnails.forEach((thumbnail, index) => {
    if (thumbnail.dataset.type === "video") {
      mediaItems.push({
        type: "video",
        src: thumbnail.querySelector("source").src,
        element: thumbnail,
      });
    } else {
      mediaItems.push({
        type: "image",
        src: thumbnail.src,
        element: thumbnail,
      });
    }

    // Click to switch main media
    thumbnail.addEventListener("click", function () {
      thumbnails.forEach((t) => t.classList.remove("active"));
      this.classList.add("active");

      const mediaType = this.dataset.type;
      const mediaIndex = parseInt(this.dataset.index);

      // Fade effect
      if (mainVideo) mainVideo.style.opacity = "0.7";
      if (mainImage) mainImage.style.opacity = "0.7";

      setTimeout(() => {
        if (mediaType === "video") {
          if (mainVideo && mainImage) {
            mainVideo.style.display = "block";
            mainImage.style.display = "none";
            mainVideo.src = mediaItems[mediaIndex].src;
            mainVideo.load();
          }
        } else {
          if (mainVideo) {
            mainVideo.pause();
            mainVideo.style.display = "none";
          }
          if (mainImage) {
            mainImage.style.display = "block";
            mainImage.src = this.src;
          }
        }

        // Update media number
        currentMediaNumber.textContent = mediaIndex + 1;

        if (mainVideo) mainVideo.style.opacity = "1";
        if (mainImage) mainImage.style.opacity = "1";
      }, 150);
    });
  });

  // Touch swipe detection
  let touchStartX = 0;
  let touchEndX = 0;
  const mainMediaContainer = document.querySelector(".main-media");

  mainMediaContainer.addEventListener("touchstart", function (e) {
    touchStartX = e.changedTouches[0].screenX;
  });

  mainMediaContainer.addEventListener("touchend", function (e) {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipe();
  });

  function handleSwipe() {
    const swipeThreshold = 50; // Minimum distance for swipe
    const diff = touchStartX - touchEndX;

    if (Math.abs(diff) > swipeThreshold) {
      const currentIndex = parseInt(currentMediaNumber.textContent) - 1;
      let newIndex;

      if (diff > 0 && currentIndex < mediaItems.length - 1) {
        newIndex = currentIndex + 1; // Swipe left → next
      } else if (diff < 0 && currentIndex > 0) {
        newIndex = currentIndex - 1; // Swipe right → previous
      } else {
        return;
      }

      thumbnails[newIndex].click(); // Trigger click on new thumbnail
    }
  }

  // Keyboard navigation
  document.addEventListener("keydown", function (e) {
    const currentIndex = parseInt(currentMediaNumber.textContent) - 1;

    if (e.key === "ArrowRight" && currentIndex < mediaItems.length - 1) {
      thumbnails[currentIndex + 1].click();
    } else if (e.key === "ArrowLeft" && currentIndex > 0) {
      thumbnails[currentIndex - 1].click();
    }
  });

  // Tab switching logic
  const tabLinks = document.querySelectorAll(".tab-link");
  const tabContents = document.querySelectorAll(".tab-content");

  tabLinks.forEach((link) => {
    link.addEventListener("click", function () {
      const targetTab = this.dataset.tab;

      tabLinks.forEach((l) => l.classList.remove("active"));
      tabContents.forEach((c) => c.classList.remove("active"));

      this.classList.add("active");
      document.getElementById(targetTab).classList.add("active");
    });
  });

  // Inquiry form submission via AJAX
  const inquiryForm = document.getElementById("inquiryForm");
  const submitBtn = document.getElementById("submitBtn");
  const successOverlay = document.getElementById("successOverlay");

  inquiryForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const formData = new FormData(this);
    const originalBtnContent = submitBtn.innerHTML;

    submitBtn.disabled = true;
    submitBtn.innerHTML = '<div class="loading-spinner"></div>Sending...';
    document.body.classList.add("no-scroll");

    fetch(window.location.href, {
      method: "POST",
      body: formData,
      headers: { "X-Requested-With": "XMLHttpRequest" },
    })
      .then((response) => response.json())
      .then((data) => {
        setTimeout(() => {
          if (data.success) {
            successOverlay.style.display = "flex";
            setTimeout(() => {
              successOverlay.style.display = "none";
              document.body.classList.remove("no-scroll");
              inquiryForm.reset();
            }, 3000);
          } else {
            alert("There was an error sending your message. Please try again.");
            document.body.classList.remove("no-scroll");
          }

          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnContent;
        }, 3000);
      })
      .catch((error) => {
        setTimeout(() => {
          alert("There was an error sending your message. Please try again.");
          submitBtn.disabled = false;
          submitBtn.innerHTML = originalBtnContent;
          document.body.classList.remove("no-scroll");
        }, 3000);
      });
  });

  // Copy current page URL to clipboard
  const copyLinkBtn = document.getElementById("copyLinkBtn");
  const copySuccess = document.getElementById("copySuccess");

  copyLinkBtn.addEventListener("click", function (e) {
    e.preventDefault();
    const currentUrl = window.location.href;

    if (navigator.clipboard && window.isSecureContext) {
      navigator.clipboard
        .writeText(currentUrl)
        .then(showCopySuccess)
        .catch(() => {
          fallbackCopyTextToClipboard(currentUrl);
        });
    } else {
      fallbackCopyTextToClipboard(currentUrl);
    }
  });

  // Fallback for older browsers
  function fallbackCopyTextToClipboard(text) {
    const textArea = document.createElement("textarea");
    textArea.value = text;
    textArea.style.top = "0";
    textArea.style.left = "0";
    textArea.style.position = "fixed";
    textArea.style.opacity = "0";
    document.body.appendChild(textArea);
    textArea.focus();
    textArea.select();

    try {
      const successful = document.execCommand("copy");
      if (successful) showCopySuccess();
    } catch (err) {
      console.error("Fallback: Unable to copy", err);
    }

    document.body.removeChild(textArea);
  }

  // Show "copied" success message
  function showCopySuccess() {
    copySuccess.classList.add("show");
    setTimeout(() => {
      copySuccess.classList.remove("show");
    }, 2000);
  }
});
