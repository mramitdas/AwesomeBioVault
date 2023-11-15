const button = document.querySelector(".modal-buttons"),
  toast = document.querySelector(".toast"),
  closeIcon = document.querySelector(".close"),
  progress = document.querySelector(".progress");

let timer1, timer2;

// Initially hide the toast and progress
toast.classList.remove("active");
progress.classList.remove("active");

button.addEventListener("click", () => {
  // Show the toast and progress when the button is clicked
  toast.classList.add("active");
  progress.classList.add("active");

  // Set timers to hide the toast and progress after a certain time
  timer1 = setTimeout(() => {
    toast.classList.remove("active");
  }, 5000); // 5 seconds

  timer2 = setTimeout(() => {
    progress.classList.remove("active");
  }, 5300); // 5.3 seconds
});

closeIcon.addEventListener("click", () => {
  // Hide the toast and progress when the close icon is clicked
  toast.classList.remove("active");

  // Use a setTimeout to delay hiding the progress for a smoother transition
  setTimeout(() => {
    progress.classList.remove("active");
  }, 300);

  // Clear the timers to prevent the automatic hiding
  clearTimeout(timer1);
  clearTimeout(timer2);
});
