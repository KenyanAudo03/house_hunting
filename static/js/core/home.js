document.addEventListener("DOMContentLoaded", function () {
  // Initialize carousel for latest hostels
  initializeCarousel("latest");
  initializeCarousel("more");

  function initializeCarousel(prefix) {
    const cardsContainer = document.getElementById(`${prefix}-hostelCards`);
    const prevBtn = document.getElementById(`${prefix}-prevBtn`);
    const nextBtn = document.getElementById(`${prefix}-nextBtn`);
    const carouselControls = document.getElementById(
      `${prefix}-carousel-controls`
    );

    if (!cardsContainer) return;

    const cards = cardsContainer.querySelectorAll(".house-card");
    const totalCards = cards.length;

    if (totalCards === 0) {
      if (carouselControls) carouselControls.style.display = "none";
      return;
    }

    let currentIndex = 0;
    let cardsPerView = 4; // Desktop default
    let resizeTimeout;

    function forceCSSUpdate() {
      cardsContainer.style.opacity = "0";
      cards.forEach((card) => {
        card.offsetHeight;
      });
      setTimeout(() => {
        cardsContainer.style.opacity = "1";
        updateCarousel();
      }, 10);
    }

    function getCardWidth() {
      if (cards.length > 0) {
        const cardStyle = window.getComputedStyle(cards[0]);
        const cardWidth = parseFloat(cardStyle.width);
        return cardWidth;
      }
      return 280; // fallback
    }

    function updateCardsPerView() {
      const screenWidth = window.innerWidth;
      if (screenWidth <= 480) {
        cardsPerView = 2;
      } else if (screenWidth <= 768) {
        cardsPerView = 2;
      } else if (screenWidth <= 1024) {
        cardsPerView = 3;
      } else {
        cardsPerView = 4;
      }
    }

    function updateCarousel() {
      const cardWidth = getCardWidth();
      const gap = 20;
      const translateX = -(currentIndex * (cardWidth + gap));
      cardsContainer.style.transform = `translateX(${translateX}px)`;

      if (prevBtn) prevBtn.disabled = currentIndex === 0;
      if (nextBtn) nextBtn.disabled = currentIndex >= totalCards - cardsPerView;

      if (carouselControls) {
        if (totalCards <= cardsPerView) {
          carouselControls.style.display = "none";
        } else {
          carouselControls.style.display = "flex";
        }
      }
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        if (currentIndex > 0) {
          currentIndex = Math.max(0, currentIndex - cardsPerView);
          updateCarousel();
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        const maxIndex = Math.max(0, totalCards - cardsPerView);
        if (currentIndex < maxIndex) {
          currentIndex = Math.min(maxIndex, currentIndex + cardsPerView);
          updateCarousel();
        }
      });
    }

    window.addEventListener("resize", function () {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(function () {
        updateCardsPerView();

        const maxIndex = Math.max(0, totalCards - cardsPerView);
        if (currentIndex > maxIndex) {
          currentIndex = maxIndex;
        }

        forceCSSUpdate();
      }, 150);
    });

    updateCardsPerView();
    updateCarousel();
  }
});
