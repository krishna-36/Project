document.getElementById("uploadForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevent form from submitting normally

    // Get the file input and the selected video file
    const videoInput = document.getElementById("videoInput");
    const videoFile = videoInput.files[0];

    // Show loading indicator
    document.getElementById("loading").style.display = "block";

    // Create a FormData object to send the video file via POST
    const formData = new FormData();
    formData.append("video", videoFile);

    // Create an XMLHttpRequest to send the file
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/summarize", true);

    // On successful response from the backend
    xhr.onload = function() {
        if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            const summary = response.summary || "Sorry, we couldn't summarize the video.";
            alert("Summary: " + summary);
        } else {
            alert("Error processing the video.");
        }

        // Hide loading indicator after processing
        document.getElementById("loading").style.display = "none";
    };

    // Send the video file to the server
    xhr.send(formData);
});
