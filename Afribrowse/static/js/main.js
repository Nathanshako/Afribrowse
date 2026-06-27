document.getElementById('search-button').addEventListener('click', performSearch);
document.getElementById('search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});

function performSearch() {
    const query = document.getElementById('search-input').value.trim();
    const resultsContainer = document.getElementById('results-container');
    const searchContainer = document.getElementById('search-container');

    if (!query) return;

    // Fetch data asynchronously from our Flask API
    fetch(`/search?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
            // Move search bar to top once search happens
            searchContainer.classList.add('active');
            resultsContainer.innerHTML = ''; // Clear old results

            if (data.length === 0) {
                resultsContainer.innerHTML = `<p class="subtitle" style="text-align:center;">No offline results found for "${query}".</p>`;
                return;
            }

            // Loop through results and display them
            data.forEach(item => {
                const resultCard = document.createElement('div');
                resultCard.className = 'result-card';
                
                resultCard.innerHTML = `
                    <a href="${item.url}" class="result-title" target="_blank">${item.title}</a>
                    <span class="result-url">${item.url}</span>
                    <p class="result-snippet">${item.snippet}</p>
                `;
                
                resultsContainer.appendChild(resultCard);
            });
        })
        .catch(error => {
            console.error('Error fetching search results:', error);
        });
}