document.getElementById('trip-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const userQuery = document.getElementById('user-query').value;
    const resultContainer = document.getElementById('result');
    resultContainer.innerHTML = "Processing...";

    try {
        const response = await fetch('/process_query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ user_query: userQuery }),
        });

        const data = await response.json();

        if (data.result) {
            const formattedHTML = formatResult(data.result);
            resultContainer.innerHTML = formattedHTML;
        } else {
            resultContainer.innerHTML = "No result returned.";
        }
    } catch (error) {
        resultContainer.innerHTML = "An error occurred: " + error.message;
    }
});

function formatResult(resultText) {
    // Split the summary and details sections
    const [summaryPart, detailsPart] = resultText.split("\n\nDetails:\n");
    const summaryLines = summaryPart.split("\n").filter(line => line.startsWith("-"));
    const detailsContent = detailsPart || "";

    // Parse details content into subsections by day
    const daySections = detailsContent.split("Day ").slice(1).map(dayContent => {
        const [dayTitle, ...dayDetails] = dayContent.split(":");
        return `<div class="day-section">
            <h4>Day ${dayTitle.trim()}</h4>
            <p>${dayDetails.join(":").trim()}</p>
        </div>`;
    }).join("");

    // Create formatted HTML
    const summaryHTML = `
        <h3>Summary</h3>
        <ul>
            ${summaryLines.map(line => `<li>${line.replace("- ", "")}</li>`).join("")}
        </ul>
    `;

    const detailsHTML = `
        <h3>Details</h3>
        ${daySections}
    `;

    return `
        <div class="result-summary">
            ${summaryHTML}
        </div>
        <div class="result-details">
            ${detailsHTML}
        </div>
    `;
}
