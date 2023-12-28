document.addEventListener("DOMContentLoaded", function () {
  var dateButtons = document.querySelectorAll('.button3.booking-date');

  dateButtons.forEach(function (button) {
    button.addEventListener('click', function () {
      var movieId = button.dataset.movie;
      var dateId = button.dataset.date;
      var timeId = button.dataset.time;
      var action = button.dataset.action;

      console.log('Movie ID:', movieId, 'Date ID:', dateId, 'Time ID:', timeId, 'Action:', action);

      if (!dateId || !timeId) {
        alert("Please select a date and time before proceeding.");
      } else {
        updateDate(movieId, dateId, timeId, action);
      }
    });
  });

  function updateDate(movieId, dateId, timeId, action) {
    var url = '/updateDate/';  
    fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')  
      },
      body: JSON.stringify({
        'movieId': movieId,
        'dateId': dateId,
        'timeId': timeId,
        'action': action
      })
    })
    .then(response => response.json())
    .then(data => {
      console.log('data', data);
    })
    .catch(error => {
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
