let amountElement = document.getElementById('amount');
if (amountElement) {
    let amount = amountElement.value;
}

function handlePlus(inputId) {
    var input = document.getElementById(inputId);
    input.value = parseInt(input.value) + 1;
    updateProduct(inputId, input.value);
}

function handleMinus(inputId) {
    var input = document.getElementById(inputId);
    if (parseInt(input.value) > 0) {
        input.value = parseInt(input.value) - 1;
    }
    updateProduct(inputId, input.value);
}

function updateProduct(inputId, newAmount) {
    let productId = inputId.substring(6);
    console.log(`Product ${productId}, amount ${newAmount}`);
    var url = '/updateProduct/';
    fetch(url,{
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            productId: productId,
            amount: newAmount,
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