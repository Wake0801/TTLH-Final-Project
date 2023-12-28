document.addEventListener("DOMContentLoaded", function() {
    var bookButtons = document.querySelectorAll('[data-action="add"]');

    bookButtons.forEach(function(button) {
        button.addEventListener("click", function() {
            var movieId = button.dataset.movie;
            var action = button.dataset.action;
 
            console.log("Movie ID:", movieId, "Action:", action);

            updateMovie(movieId, action);
        });
    });

    function updateMovie(movieId, action) {
        var url = '/updateMovie/';
        fetch(url, {
            method: 'POST',
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken") 
            },
            body: JSON.stringify({"movieId": movieId, "action": action})
        })
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            console.log("data:", data);
        })
        .catch((error) => {
            console.error('Error:', error);
        });
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
