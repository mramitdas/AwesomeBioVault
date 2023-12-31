/**
 * Increments a counter on the client side and updates the user profile views on the server.
 *
 * @param {string} id - The identifier associated with the counter and user profile.
 *
 * @returns {Promise<void>} - A Promise that resolves when the operation is complete.
 *
 * @throws {Error} - If there is an issue with the fetch operation or server response.
 *
 * @example
 * // Increment the counter for user with id 'mramitdas'
 * incrementCounter('mramitdas');
 */
async function incrementCounter(element, id) {
  try {
    // Get the counter element and increment the count
    let counterElement = document.getElementById(element + String(id));
    let count = parseInt(counterElement.innerText) + 1;
    counterElement.innerText = count;

    // Prepare data for server update
    let requestData = {
      github_username: id,
      user_data: {},
    };

    if (element === 'counter') {
      requestData.user_data.profile_views = count; 
    } else if (element === 'likes') {
      requestData.user_data.profile_likes = count; 
    } else {
      console.log("code broke while appending json with counter")
    }

    // Make a PATCH request to update the user profile on the server
    const response = await fetch("/profile/update", {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(requestData),
    });

    // Parse the server response as JSON
    const data = await response.json();
    console.log("Server response:", data);
    // Handle the server response if needed
  } catch (error) {
    console.error("There was a problem:", error);
    // Handle errors if needed
    throw error;
  }
}
