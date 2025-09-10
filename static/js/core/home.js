document.addEventListener("DOMContentLoaded", function () {
  // Initialize carousel for latest hostels
  initializeCarousel("latest");
  initializeCarousel("single");
  initializeCarousel("bedsitter");

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
    let cardsPerView = 4;
    let resizeTimeout;

    function getCardWidth() {
      if (cards.length > 0) {
        const cardStyle = window.getComputedStyle(cards[0]);
        return parseFloat(cardStyle.width);
      }
      return 280;
    }

    function updateCardsPerView() {
      const screenWidth = window.innerWidth;
      if (screenWidth <= 480) {
        cardsPerView = 1;
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
        carouselControls.style.display =
          totalCards <= cardsPerView ? "none" : "flex";
      }
    }

    if (prevBtn) {
      prevBtn.addEventListener("click", function () {
        if (currentIndex > 0) {
          currentIndex = Math.max(0, currentIndex - 1);
          updateCarousel();
        }
      });
    }

    if (nextBtn) {
      nextBtn.addEventListener("click", function () {
        const maxIndex = Math.max(0, totalCards - cardsPerView);
        if (currentIndex < maxIndex) {
          currentIndex = Math.min(maxIndex, currentIndex + 1);
          updateCarousel();
        }
      });
    }

    window.addEventListener("resize", function () {
      clearTimeout(resizeTimeout);
      resizeTimeout = setTimeout(function () {
        const oldCardsPerView = cardsPerView;
        updateCardsPerView();

        if (oldCardsPerView !== cardsPerView) {
          const maxIndex = Math.max(0, totalCards - cardsPerView);
          currentIndex = Math.min(currentIndex, maxIndex);
        }

        cardsContainer.style.opacity = "0";
        setTimeout(() => {
          cardsContainer.style.opacity = "1";
          updateCarousel();
        }, 10);
      }, 150);
    });

    updateCardsPerView();
    updateCarousel();
  }
});
