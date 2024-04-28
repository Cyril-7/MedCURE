// Get the HTML search input element
const searchInput = document.getElementById("search");

// Get all elements with different class names
const elements = document.querySelectorAll(".nav-link, .nav-item", ".doctors");

// Loop through each element and add the common class name
elements.forEach(function (element) {
  element.classList.add("searchable");
});

// Create a new HTML element for the dropdown menu
const dropdown = document.createElement("div");
dropdown.classList.add("dropdown1");

// Append the dropdown menu to the search bar element
searchInput.parentNode.appendChild(dropdown);

// Add event listener for input changes
searchInput.addEventListener("input", function () {
  // Get the search query
  const query = searchInput.value.toLowerCase();

  // Get all the items to search through
  const items = document.querySelectorAll(".nav-link");

  // Create a new HTML element for the dropdown items
  let dropdownItems = "";

  // Loop through all the items
  items.forEach(function (item) {
    // Check if the item contains the search query
    if (item.textContent.toLowerCase().includes(query)) {
      // Add the item to the dropdown items
      dropdown.style.position = "relative";
      dropdown.style.width = "800px"
      dropdown.style.top = 0;
      dropdownItems +=
        '<div class="dropdown-item"><a href="' +
        item.href +
        '">' +
        item.textContent +
        "</a></div>";
    }
  });

  // dropdownItems.forEach(function (list) {

  // });

  // Set the dropdown HTML to the dropdown items

  for (let i = 0; i < dropdownItems.length; i++) {
    dropdown.innerHTML = dropdownItems;
  }

  // Show or hide the dropdown based on whether there are any search results
  if (dropdownItems === "") {
    dropdown.style.display = "none";
  } else {
    dropdown.style.display = "block";

    // Add event listeners to each dropdown item
    const dropdownLinks = dropdown.querySelectorAll("a");
    dropdownLinks.forEach(function (link) {
      link.addEventListener("click", function (event) {
        event.preventDefault();
        window.location = link.href;

        // Add the search query to the recent search history array
        searchHistory.push(query);

        // Display the recent search history in the HTML
        const historyList = document.getElementById("searchHistory");
        let historyItems = "";
        for (let i = searchHistory.length - 1; i >= 0; i--) {
          historyItems += "<li>" + searchHistory[i] + "</li>";
        }
        historyList.innerHTML = historyItems;
      });
    });
  }
});
