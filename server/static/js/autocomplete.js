document.querySelector("#autoComplete").addEventListener("init", function (event) {
  console.log(event);
});

const autoCompleteJS = new autoComplete({
  data: {
    src: async () => {
      // Get user input
      const query = document.querySelector("#autoComplete").value;
      // Fetch External Data Source
      const source = await fetch(`http://localhost:5000/_autocomplete?name=${query}`);
      // Format data into JSON
      const data = await source.json();
      return data;
    },
    key: ["legal_business_name"],
    cache: false
  },
  placeHolder: "Vendor Name...",
  selector: "#autoComplete",
  observer: true,
  threshold: 3,
  debounce: 300,
  searchEngine: "strict",
  resultsList: {
      container: source => {
          source.setAttribute("id", "vendor_names");
      },
      destination: "#autoComplete",
      position: "afterend",
      element: "ul"
  },
  maxResults: 15,
  highlight: true,
  resultItem: {
      content: (data, element) => {
        // display both the vendor name and the cage code in the selector, with the cage code all
        // the way to the right and the vendor name on left.
        element.style = "display: flex; justify-content: space-between;";
        element.innerHTML = `<span style="text-overflow: ellipsis; white-space: nowrap; overflow: hidden;">
          ${data.match}</span>
          <span style="display: flex; align-items: center; font-size: 13px; font-weight: 100; text-transform: uppercase; color: rgba(0,0,0,.2);">
        ${data.value.cage_code}</span>`;
      },
      element: "li"
  },
  onSelection: (feedback) => {
    // when a user selects a value in the list, put the value in the text box
		document.querySelector("#autoComplete").blur();
		const selection = feedback.selection.value[feedback.selection.key];
		document.querySelector("#autoComplete").value = selection;
		console.log(feedback);
	},
  noResults: (dataFeedback, generateList) => {
      generateList(autoCompleteJS, dataFeedback, dataFeedback.results);
      const result = document.createElement("li");
      result.setAttribute("class", "no_result");
      result.setAttribute("tabindex", "1");
      result.innerHTML = `<span style="display: flex; align-items: center; font-weight: 100; color: rgba(0,0,0,.2);">Found No Results for "${dataFeedback.query}"</span>`;
      document.querySelector(`#${autoCompleteJS.resultsList.idName}`).appendChild(result);
  }
});