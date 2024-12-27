(function() {
    const regexPattern = /(\d{2})-(\d{3})-(\d{2})-(\d{2})/g;
    function extractCodeAndQuantity() {
        const bodyText = document.body.innerText; // Get the entire page text
        const matches = [...bodyText.matchAll(regexPattern)];
        return matches.map(match => ({
            code: match[0],   // Entire matched string
            // If you want specific segments, use match[1], match[2], etc.
        }));
    }
    const result = extractCodeAndQuantity();
    // Display the results
    if (result.length === 0) {
        console.log("No match found.");
    } else {
        console.log("Results status: present.");
        result.forEach(({ code }) => {
            console.log(code);
        });
    }
})();