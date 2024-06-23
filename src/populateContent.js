document.addEventListener("DOMContentLoaded", function() {
    // Fetch the JSON data from content.json
    fetch('content.json')
        .then(response => response.json())
        .then(data => {
            for (const key in data) {
                document.body.innerHTML = document.body.innerHTML.replace(new RegExp(`{{${key}}}`, 'g'), data[key]);
            }
        })
        .catch(error => console.error('Error fetching JSON data:', error));
});