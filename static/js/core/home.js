document.addEventListener("DOMContentLoaded", function () {
  const cardsContainer = document.getElementById("hostelCards");
  const prevBtn = document.getElementById("prevBtn");
  const nextBtn = document.getElementById("nextBtn");
  const carouselControls = document.getElementById("carousel-controls");

  if (!cardsContainer) return;

  const cards = cardsContainer.querySelectorAll(".house-card");
  const totalCards = cards.length;

  if (totalCards === 0) {
    carouselControls.style.display = "none";
    return;
  }

  let currentIndex = 0;
  let cardsPerView = 4; // Desktop default
  let resizeTimeout;

  function forceCSSUpdate() {
    cardsContainer.style.opacity = "0";

    // Force reflow by accessing offsetHeight
    cards.forEach((card) => {
      card.offsetHeight;
    });

    // Small delay to ensure CSS media queries are applied
    setTimeout(() => {
      cardsContainer.style.opacity = "1";
      updateCarousel();
    }, 10);
  }

  // Get actual card width including margin
  function getCardWidth() {
    if (cards.length > 0) {
      const cardStyle = window.getComputedStyle(cards[0]);
      const cardWidth = parseFloat(cardStyle.width);
      return cardWidth;
    }
    return 280; // fallback
  }

  // Calculate cards per view based on screen size
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

  // Update carousel position
  function updateCarousel() {
    const cardWidth = getCardWidth();
    const gap = 20; // Gap between cards
    const translateX = -(currentIndex * (cardWidth + gap));
    cardsContainer.style.transform = `translateX(${translateX}px)`;

    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex >= totalCards - cardsPerView;

    // Hide controls if not enough cards to scroll
    if (totalCards <= cardsPerView) {
      carouselControls.style.display = "none";
    } else {
      carouselControls.style.display = "flex";
    }
  }

  // Previous button click - move by cardsPerView
  prevBtn.addEventListener("click", function () {
    if (currentIndex > 0) {
      currentIndex = Math.max(0, currentIndex - cardsPerView);
      updateCarousel();
    }
  });

  // Next button click - move by cardsPerView
  nextBtn.addEventListener("click", function () {
    const maxIndex = Math.max(0, totalCards - cardsPerView);
    if (currentIndex < maxIndex) {
      currentIndex = Math.min(maxIndex, currentIndex + cardsPerView);
      updateCarousel();
    }
  });

  // Handle window resize with debouncing
  window.addEventListener("resize", function () {
    // Clear existing timeout
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

  // Initialize
  updateCardsPerView();
  updateCarousel();
});
