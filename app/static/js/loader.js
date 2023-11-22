function imageLoaded(username) {
  // When the image is loaded, show the image and hide the loading spinner
  setTimeout(function () {
    const loader = document.querySelector(".loader" + username);
    const loadedImage = document.getElementById("loadedImage" + username);

    // Hide the loader
    loader.style.display = "none";
  }, 1000);
}
