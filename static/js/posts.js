// posts.js

function likePost(blogId) {
    fetch(`/like/${blogId}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),  // Assumes you have a CSRF token setup
        },
        body: JSON.stringify({
            'liked': true,
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Optionally update the UI to reflect the like
            alert('Post liked successfully!');
        }
    })
    .catch(error => console.error('Error:', error));
}

// Function to get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
