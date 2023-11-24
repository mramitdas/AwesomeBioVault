/**
 *
 * This script is designed to enhance a web page containing a list of cards.
 * It includes functionality to filter and display cards based on a search input.
 *
 * Variables:
 * - searchBar: Represents the HTML element for the search input.
 * - cardTitles: Represents a NodeList of HTML elements with the class "card__title,"
 *               typically containing the titles of cards.
 * - cardContainers: Represents a NodeList of HTML elements with the class "card_container,"
 *                   representing the containers for individual cards.
 * - cardTitlesText: An array to store the lowercase text content of card titles.
 *
 * Functions:
 * - collectCardTitle: A function that populates the cardTitlesText array with the
 *                     lowercase text content of card titles. This function is called
 *                     during initialization to set up the initial state.
 *
 * - filter: A function that is triggered on each keyup event in the search input.
 *           It filters and displays only the cards whose titles contain the entered text.
 *           It updates the display style of card containers accordingly.
 *
 * Execution:
 * The script initializes by calling collectCardTitle() to populate the cardTitlesText array.
 * The filter() function is also called initially to set up the initial state.
 * Event listener is added to the search input, so that the filter() function is triggered
 * every time the user types into the search bar.
 *
 * Note: This script assumes a specific HTML structure with elements having specific classes.
 * Adjustments may be needed based on the actual structure of the web page.
 */
const searchBar = document.querySelector(".searchInput");
const cardTitles = document.querySelectorAll(".card__title");
const cardContainers = document.querySelectorAll(".card_container");
const cardTitlesText = [];

/**
 * Collects the lowercase text content of card titles and logs the result to the console.
 */
const collectCardTitle = () => {
  cardTitles.forEach((title) => {
    cardTitlesText.push(title.innerHTML.toLowerCase());
  });
  console.log(cardTitlesText);
};

/**
 * Filters and displays cards based on the entered search text.
 * Updates the display style of card containers accordingly.
 */
const filter = () => {
  const text = searchBar.value.toLowerCase();
  const matchingTitles = cardTitlesText.filter((title) => title.includes(text));

  cardContainers.forEach((container, index) => {
    if (matchingTitles.includes(cardTitlesText[index])) {
      container.style.display = "block";
    } else {
      container.style.display = "none";
    }
  });
};

// Initial setup
collectCardTitle();
filter();

// Event listener for search input
searchBar.addEventListener("keyup", filter);
