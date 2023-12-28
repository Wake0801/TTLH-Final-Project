document.addEventListener("DOMContentLoaded", function() {
  var seats = document.querySelectorAll(".row1 .seat");
  var confirmButton = document.getElementById("buy-btn");
  
  seats.forEach(function(seat) {
      seat.addEventListener("click", function() {
          seat.classList.toggle("selected");
      });
  });
  if (!confirmButton) {
    console.error("confirmButton is null");
    return;
  }
  confirmButton.addEventListener("click", function(event) {
      var seatCount = document.querySelectorAll(".row1 .seat.selected").length;
      console.log("Seat Count:", seatCount);
      updateSeat("submit", seatCount);
      var selectedSeats = Array.from(seats).filter(seat => seat.classList.contains("selected"));
      if (selectedSeats.length === 0) {
      event.preventDefault();
      alert("You haven't choose seat yet!, Please choose seat to continue");
    }
  });

  function updateSeat(action, seatCount) {
    var url = '/updateSeat/';
        fetch(url, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                action: action,
                seatCount: seatCount,
            }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("Data:", data);
        })
        .catch(error => {
            console.error("Error:", error);
        });
  }

  function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      var cookies = document.cookie.split(";");
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
});