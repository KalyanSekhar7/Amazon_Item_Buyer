function getItems(items) {
  // Send an HTTP POST request to the FastAPI server
  fetch('http://localhost:8000/get_items', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `items=${encodeURIComponent(items)}`,
  })
    .then(response => response.text())
    .then(data => {
      console.log(data); // Optional: Handle the server response
    })
    .catch(error => {
      console.error('Error:', error);
    });
}

// Listen for messages from the popup
chrome.runtime.onMessage.addListener(function (request, sender, sendResponse) {
  if (request.action === 'getItems') {
    getItems(request.items);
  }
});