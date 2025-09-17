document.addEventListener("DOMContentLoaded", function () {
  const checkboxes = document.querySelectorAll(".hostel-checkbox");
  const compareBtn = document.getElementById("compareBtn");
  const selectedHostelsDiv = document.getElementById("selectedHostels");
  const comparisonResults = document.getElementById("comparisonResults");
  let selectedHostels = [];

  // Prevent hostel card links from being triggered when clicking checkboxes
  const hostelLinks = document.querySelectorAll(".hostel-link");
  hostelLinks.forEach((link) => {
    link.addEventListener("click", function (e) {
      if (e.target.closest(".hostel-checkbox-container")) {
        e.preventDefault();
        e.stopPropagation();
        return false;
      }
    });
  });

  // Handle checkbox interactions
  checkboxes.forEach((checkbox) => {
    const checkboxContainer = checkbox.closest(".hostel-checkbox-container");

    checkboxContainer.addEventListener("click", function (e) {
      e.preventDefault();
      e.stopPropagation();

      const hostelId = checkbox.value;
      const hostelName = checkbox.dataset.hostelName;
      const card = checkbox.closest(".house-card");
      const isCurrentlyChecked = checkbox.checked;

      // Prevent more than 2 selections (only if trying to check a new one)
      if (!isCurrentlyChecked && selectedHostels.length >= 2) {
        alert(
          "You can only select 2 hostels for comparison. Uncheck one first."
        );
        return;
      }

      checkbox.checked = !isCurrentlyChecked;

      if (checkbox.checked) {
        selectedHostels.push({ id: hostelId, name: hostelName });
        card.classList.add("selected");
      } else {
        selectedHostels = selectedHostels.filter((h) => h.id !== hostelId);
        card.classList.remove("selected");
      }

      updateCompareUI();
    });

    checkbox.addEventListener("change", function (e) {
      e.stopPropagation();

      const hostelId = this.value;
      const hostelName = this.dataset.hostelName;
      const card = this.closest(".house-card");

      if (this.checked) {
        if (selectedHostels.length >= 2) {
          this.checked = false;
          alert(
            "You can only select 2 hostels for comparison. Uncheck one first."
          );
          return;
        }
        selectedHostels.push({ id: hostelId, name: hostelName });
        card.classList.add("selected");
      } else {
        selectedHostels = selectedHostels.filter((h) => h.id !== hostelId);
        card.classList.remove("selected");
      }

      updateCompareUI();
    });

    checkbox.addEventListener("click", function (e) {
      e.stopPropagation();
    });
  });

  function updateCompareUI() {
    if (selectedHostels.length === 0) {
      selectedHostelsDiv.innerHTML = `
                <p style="color: #666; font-size: 14px; text-align: center; margin: 20px 0;">
                    Use the checkboxes on hostel cards to select hostels for comparison
                </p>
            `;
      compareBtn.disabled = true;
    } else if (selectedHostels.length === 1) {
      selectedHostelsDiv.innerHTML = `
                <div style="background: #f8f9fa; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                    <strong>Selected:</strong><br>
                    • ${selectedHostels[0].name}
                </div>
                <p style="color: #666; font-size: 14px; text-align: center;">
                    Select 1 more hostel to compare
                </p>
            `;
      compareBtn.disabled = true;
    } else if (selectedHostels.length === 2) {
      selectedHostelsDiv.innerHTML = `
                <div style="background: #f8f9fa; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                    <strong>Selected:</strong><br>
                    • ${selectedHostels[0].name}<br>
                    • ${selectedHostels[1].name}
                </div>
            `;
      compareBtn.disabled = false;
    }

    comparisonResults.style.display = "none";
  }

  compareBtn.addEventListener("click", function () {
    if (selectedHostels.length === 2) {
      compareHostels(selectedHostels[0].id, selectedHostels[1].id);
    }
  });

  function compareHostels(hostel1Id, hostel2Id) {
    compareBtn.textContent = "Comparing...";
    compareBtn.disabled = true;

    fetch("/users/compare-hostels/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken"),
      },
      body: JSON.stringify({
        hostel1_id: hostel1Id,
        hostel2_id: hostel2Id,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        displayComparison(data);
        compareBtn.textContent = "Compare Selected Hostels";
        compareBtn.disabled = false;
      })
      .catch((error) => {
        console.error("Error:", error);
        alert("Error comparing hostels. Please try again.");
        compareBtn.textContent = "Compare Selected Hostels";
        compareBtn.disabled = false;
      });
  }

  function displayComparison(data) {
    const resultsHTML = `
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th class="feature">Feature</th>
                        <th class="hostel-data">${data.hostel1.name}</th>
                        <th class="hostel-data">${data.hostel2.name}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="feature">Price</td>
                        <td class="price-comparison ${
                          data.price_winner === 1
                            ? "price-better"
                            : "price-worse"
                        }">
                            KSh ${data.hostel1.pricing}/${
      data.hostel1.billing_cycle
    }
                            ${
                              data.price_winner === 1
                                ? '<span class="winner-badge">Better Deal</span>'
                                : ""
                            }
                        </td>
                        <td class="price-comparison ${
                          data.price_winner === 2
                            ? "price-better"
                            : "price-worse"
                        }">
                            KSh ${data.hostel2.pricing}/${
      data.hostel2.billing_cycle
    }
                            ${
                              data.price_winner === 2
                                ? '<span class="winner-badge">Better Deal</span>'
                                : ""
                            }
                        </td>
                    </tr>
                    <tr>
                        <td class="feature">Room Type</td>
                        <td>${data.hostel1.category}</td>
                        <td>${data.hostel2.category}</td>
                    </tr>
                    <tr>
                        <td class="feature">Rating</td>
                        <td>
                            <div class="rating-stars">
                                ${"★".repeat(
                                  Math.floor(data.hostel1.rating)
                                )}${"☆".repeat(
      5 - Math.floor(data.hostel1.rating)
    )}
                            </div>
                            ${data.hostel1.rating}/5.0
                            ${
                              data.rating_winner === 1
                                ? '<span class="winner-badge">Higher Rating</span>'
                                : ""
                            }
                        </td>
                        <td>
                            <div class="rating-stars">
                                ${"★".repeat(
                                  Math.floor(data.hostel2.rating)
                                )}${"☆".repeat(
      5 - Math.floor(data.hostel2.rating)
    )}
                            </div>
                            ${data.hostel2.rating}/5.0
                            ${
                              data.rating_winner === 2
                                ? '<span class="winner-badge">Higher Rating</span>'
                                : ""
                            }
                        </td>
                    </tr>
                    <tr>
                        <td class="feature">Available Units</td>
                        <td>${data.hostel1.available_vacants} units</td>
                        <td>${data.hostel2.available_vacants} units</td>
                    </tr>
                    <tr>
                        <td class="feature">Location</td>
                        <td>${data.hostel1.location}</td>
                        <td>${data.hostel2.location}</td>
                    </tr>
                    <tr>
                        <td class="feature">Amenities</td>
                        <td class="amenity-list">
                            ${
                              data.hostel1.amenities.length > 0
                                ? data.hostel1.amenities.join("<br>")
                                : "None listed"
                            }
                            ${
                              data.amenity_winner === 1
                                ? '<br><span class="winner-badge">More Amenities</span>'
                                : ""
                            }
                        </td>
                        <td class="amenity-list">
                            ${
                              data.hostel2.amenities.length > 0
                                ? data.hostel2.amenities.join("<br>")
                                : "None listed"
                            }
                            ${
                              data.amenity_winner === 2
                                ? '<br><span class="winner-badge">More Amenities</span>'
                                : ""
                            }
                        </td>
                    </tr>
                </tbody>
            </table>
            
            <div class="recommendation">
                <h4><i class='bx bx-trophy'></i> Recommendation</h4>
                <p>${data.recommendation}</p>
            </div>
        `;

    comparisonResults.innerHTML = resultsHTML;
    comparisonResults.style.display = "block";
  }

  // Helper function to get CSRF token
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
