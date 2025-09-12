function copyToClipboard(elementId) {
  const element = document.getElementById(elementId);
  if (element) {
    // Select the text
    element.select();
    element.setSelectionRange(0, 99999); // For mobile devices

    try {
      // Copy to clipboard
      const successful = document.execCommand("copy");
      if (successful) {
        // Show temporary success message
        showCopyMessage(element, "Copied!");
      } else {
        showCopyMessage(element, "Copy failed");
      }
    } catch (err) {
      // Fallback for modern browsers
      navigator.clipboard
        .writeText(element.value)
        .then(function () {
          showCopyMessage(element, "Copied!");
        })
        .catch(function () {
          showCopyMessage(element, "Copy failed");
        });
    }
  }
}

function showCopyMessage(element, message) {
  // Create temporary message element
  const messageEl = document.createElement("span");
  messageEl.textContent = message;
  messageEl.style.cssText =
    "color: green; font-weight: bold; margin-left: 5px; font-size: 12px;";

  // Insert after the button
  const button = element.parentNode.querySelector("button");
  button.parentNode.insertBefore(messageEl, button.nextSibling);

  // Remove message after 2 seconds
  setTimeout(function () {
    if (messageEl.parentNode) {
      messageEl.parentNode.removeChild(messageEl);
    }
  }, 2000);
}
