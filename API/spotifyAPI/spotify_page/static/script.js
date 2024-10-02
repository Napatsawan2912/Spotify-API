document.addEventListener("DOMContentLoaded", function() {
    var skyElement = document.querySelector(".sky");
    if (skyElement) {
        var imageUrl = skyElement.getAttribute("data-background");
        console.log("Image URL:", imageUrl); 
        skyElement.style.backgroundImage = "url('" + imageUrl + "')";
    }
});


