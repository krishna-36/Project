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
            const fullTranscript = response.full_transcript || "No transcript available.";

            // Display the summary
            document.getElementById("summaryText").innerText = summary;

            // Create and show the "Download Transcript" button
            const downloadButton = document.createElement("button");
            downloadButton.innerText = "Download Transcript";
            downloadButton.onclick = function() {
                // Create a Blob from the full transcript
                const blob = new Blob([fullTranscript], { type: 'text/plain' });
                const url = URL.createObjectURL(blob);
                
                // Create a link element and trigger a download
                const a = document.createElement("a");
                a.href = url;
                a.download = "transcript.txt";  // Set file name
                a.click();
                
                // Revoke the object URL after download
                URL.revokeObjectURL(url);
            };

            // Append the download button after the summary
            document.getElementById("summary").appendChild(downloadButton);
        } else {
            alert("Error processing the video.");
        }

        // Hide loading indicator after processing
        document.getElementById("loading").style.display = "none";
    };

    // Send the video file to the server
    xhr.send(formData);
});
