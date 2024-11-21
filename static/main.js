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
            const refinedPlanHTML = formatResultAsHTML(data.result);
            resultContainer.innerHTML = refinedPlanHTML;
        } else {
            resultContainer.innerHTML = "No result returned.";
        }
    } catch (error) {
        resultContainer.innerHTML = "An error occurred: " + error.message;
    }
});

function formatResultAsHTML(resultText) {
    // Convert text to formatted HTML
    const formatted = resultText
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>') // Bold for **text**
        .replace(/### (.*?)\n/g, '<h3>$1</h3>')          // Convert ### to <h3>
        .replace(/- (.*?)\n/g, '<li>$1</li>')            // Convert - to <li>
        .replace(/\n\n/g, '</ul><ul>')                   // Newline -> close/reopen list
        .replace(/\n/g, '<br>');                         // Remaining newlines -> <br>

    return `<div><ul>${formatted}</ul></div>`;
}
