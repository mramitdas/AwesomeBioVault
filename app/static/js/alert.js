/**
 * Display a toast notification with custom content and styling.
 *
 * This function shows a toast notification with a specified title, description,
 * color, and icon. The toast includes a progress element and is set to automatically
 * hide after a certain time. It also provides a close button to manually hide the toast.
 *
 * @param {string} title - The title of the toast notification.
 * @param {string} description - The description or content of the toast notification.
 * @param {string} colorVariable - The CSS variable representing the custom color for the toast.
 * @param {string} alertIcon - The class name of the icon to display in the toast.
 */
function showToast(title, description, colorVariable, alertIcon) {
  const toast = document.querySelector(".toast"),
    toastContent = document.querySelector(".toast-content"),
    progress = document.querySelector(".progress"),
    iconElement = document.getElementById("alert-icon"),
    alerTitle =  document.getElementById("alert-title"),
    alerDescription =  document.getElementById("alert-description");

  // Show the toast and progress
  toast.classList.add("active");
  progress.classList.add("active");

  // Set a custom color for the progress element using a CSS variable
  progress.style.setProperty("--alert", `var(${colorVariable})`);
  toastContent.style.setProperty("--alert", `var(${colorVariable})`);
  iconElement.classList.replace("fa-check", alertIcon);

  alerTitle.textContent = title;
  alerDescription.textContent = description;

  // Set timers to hide the toast and progress after a certain time
  const timer1 = setTimeout(() => {
    toast.classList.remove("active");
  }, 5000); // 5 seconds

  const timer2 = setTimeout(() => {
    progress.classList.remove("active");
  }, 5300); // 5.3 seconds

  // Function to clear the timers and hide the toast and progress
  const hideToast = () => {
    clearTimeout(timer1);
    clearTimeout(timer2);
    toast.classList.remove("active");
    progress.classList.remove("active");
  };

  // Attach the hideToast function to the close icon click event
  const closeIcon = document.querySelector(".close");
  closeIcon.addEventListener("click", hideToast);
}
