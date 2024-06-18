document.addEventListener("DOMContentLoaded", function() {
    const topArtistSection = document.getElementById("topArtist");
    const topAlbumSection = document.getElementById("topAlbum");
    const prevButton = document.getElementById("prevButton");
    const nextButton = document.getElementById("nextButton");


    function showTopArtist() {
        topArtistSection.style.display = "block";
        topAlbumSection.style.display = "none";
    }


    function showTopAlbum() {
        topArtistSection.style.display = "none";
        topAlbumSection.style.display = "block";
    }


    showTopAlbum();


    prevButton.addEventListener("click", function() {
        if (topArtistSection.style.display === "block") {
            showTopAlbum();
        } else {
            showTopArtist();
        }
    });

    nextButton.addEventListener("click", function() {
        if (topArtistSection.style.display === "block") {
            showTopAlbum();
        } else {
            showTopArtist();
        }
    });
});
