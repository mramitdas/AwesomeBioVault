/**
 * Attach a submit event listener to a form element.
 *
 * This listener prevents the default form submission, collects form data,
 * converts it to JSON, and performs an AJAX request to a specified API endpoint.
 * Depending on the response status code, it triggers the display of success or failure alerts.
 *
 * @param {Event} event - The submit event triggered when the form is submitted.
 */
document.getElementById("myForm").addEventListener("submit", function (event) {
  event.preventDefault(); // Prevent the default form submission

  // Collect form data
  const formData = new FormData(this);

  // Convert FormData to JSON
  const formDataObject = {};
  formData.forEach((value, key) => {
    formDataObject[key] = value;
  });

  // Perform an AJAX request to your API
  fetch("/profile", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(Object.fromEntries(formData)),
  })
    .then((response) => {
      console.log(response);
      if (response.status === 200) {
        // Show the alert on success
        showToast(
          "Success",
          "Profile added successfully",
          "--success",
          "fa-check"
        );
      } else {
        showToast(
          "Failure",
          "Invalid Github username",
          "--failure",
          "fa-xmark"
        );
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});
