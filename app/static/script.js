const videoInfoBtn = document.getElementById("video-info-btn");

videoInfoBtn.addEventListener("click", async () => {

    const url = document.getElementById("video-url").value;

    if (!url) {
        showStatus("Please enter a video URL");
        return;
    }

    showStatus("Getting video information...");

    try {

        const response = await fetch("/video/info", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })

        });

        if (!response.ok) {
            throw new Error("Failed to get video information");
        }

        const data = await response.json();

        displayVideoInfo(data);

        showStatus("");

    } catch (error) {

        console.error(error);

        showStatus("Something went wrong");

    }

});

function displayVideoInfo(data) {

    document
        .getElementById("video-result")
        .classList.remove("hidden");

    document
        .getElementById("video-thumbnail")
        .src = data.thumbnail;

    document
        .getElementById("video-title")
        .textContent = data.title;

    document
        .getElementById("video-duration")
        .textContent =
        `Duration: ${formatDuration(data.duration)}`;


    const qualitySelect =
        document.getElementById("video-quality");

    qualitySelect.innerHTML = "";


    data.qualities
        .sort((a, b) => b - a)
        .forEach(quality => {

            const option =
                document.createElement("option");

            option.value = `${quality}p`;

            option.textContent = `${quality}p`;

            qualitySelect.appendChild(option);

        });
}
async function downloadVideo() {

    const url =
        document.getElementById("video-url").value;

    const quality =
        document.getElementById("video-quality").value;

    if (!url) {
        showStatus("Please enter a video URL");
        return;
    }

    showProgress("Starting download...");

    try {

        const response = await fetch(
            "/video/download",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: url,
                    quality: quality,
                    format: "mp4"
                })
            }
        );

        if (!response.ok) {

            const error = await response.json();

            throw new Error(
                error.detail || "Download failed."
            );
        }

        const data = await response.json();

        const jobId = data.job_id;

        await monitorVideoDownload(jobId);

    } catch (error) {

        console.error(error);

        showStatus(
            `Download failed: ${error.message}`
        );
    }
}

async function monitorVideoDownload(jobId) {

    while (true) {

        const response = await fetch(
            `/video/progress/${jobId}`
        );

        if (!response.ok) {
            throw new Error(
                "Could not get download progress."
            );
        }

        const job = await response.json();

        updateProgress(
            job.progress,
            job.message
        );

        if (job.status === "completed") {

            const downloadUrl =
                `/video/download/${jobId}`;

            const a =
                document.createElement("a");

            a.href = downloadUrl;

            document.body.appendChild(a);

            a.click();

            a.remove();

            updateProgress(
                100,
                "Download complete."
            );

            return;
        }

        if (job.status === "failed") {

            throw new Error(
                job.error || "Download failed."
            );
        }

        await new Promise(
            resolve => setTimeout(resolve, 1000)
        );
    }
}

document
    .getElementById("video-download-btn")
    .addEventListener("click", downloadVideo);
    
function formatDuration(seconds) {

    if (!seconds) {
        return "Unknown";
    }

    const minutes =
        Math.floor(seconds / 60);

    const remainingSeconds =
        seconds % 60;

    return `${minutes}:${String(remainingSeconds).padStart(2, "0")}`;
}

const playlistInfoBtn =
    document.getElementById("playlist-info-btn");


playlistInfoBtn.addEventListener("click", async () => {

    const url =
        document.getElementById("playlist-url").value;


    if (!url) {
        showStatus("Please enter a playlist URL");
        return;
    }


    showStatus("Getting playlist information...");


    try {

        const response = await fetch(
            "/video/playlist/info",
            {

                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: url
                })

            }
        );


        if (!response.ok) {
            throw new Error("Failed to get playlist");
        }


        const data = await response.json();

        displayPlaylist(data);

        showStatus("");

    } catch (error) {

        console.error(error);

        showStatus("Could not load playlist");

    }

});

function displayPlaylist(data) {

    document
        .getElementById("playlist-result")
        .classList.remove("hidden");


    document
        .getElementById("playlist-title")
        .textContent = data.playlist_title;


    document
        .getElementById("playlist-count")
        .textContent =
        `${data.video_count} videos`;


    const container =
        document.getElementById("playlist-videos");


    container.innerHTML = "";


    data.videos.forEach(video => {

        const div =
            document.createElement("div");

        div.className = "playlist-video";

        div.textContent =
            `${video.index}. ${video.title}`;

        container.appendChild(div);

    });

}
function showStatus(message) {
    document.getElementById("status").textContent = message;
}
const playlistDownloadBtn =
    document.getElementById("playlist-download-btn");


playlistDownloadBtn.addEventListener("click", async () => {

    const url =
        document.getElementById("playlist-url").value;

    const quality =
        document.getElementById("playlist-quality").value;


    if (!url) {
        showStatus("Please enter a playlist URL");
        return;
    }


    showStatus("Downloading playlist...");


    try {

        const response = await fetch(
            "/video/playlist/download",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    url: url,
                    quality: quality
                })
            }
        );


        if (!response.ok) {

            let errorMessage =
                "Playlist download failed.";

            try {
                const error =
                    await response.json();

                errorMessage =
                    error.detail || errorMessage;

            } catch {
                // Server did not return JSON
            }

            throw new Error(errorMessage);
        }


        const blob =
            await response.blob();


        const downloadUrl =
            URL.createObjectURL(blob);


        const a =
            document.createElement("a");

        a.href = downloadUrl;
        a.download = "playlist.zip";

        document.body.appendChild(a);

        a.click();

        a.remove();

        URL.revokeObjectURL(downloadUrl);


        showStatus("Playlist download complete.");

    } catch (error) {

        console.error(error);

        showStatus(
            `Download failed: ${error.message}`
        );
    }

});

function showProgress(message = "Downloading...") {
    const container =
        document.getElementById("progress-container");

    container.classList.remove("hidden");

    document.getElementById("progress-text")
        .textContent = message;

    document.getElementById("progress-percent")
        .textContent = "0%";

    document.getElementById("progress-fill")
        .style.width = "0%";
}


function updateProgress(percent, message = "Downloading...") {
    percent = Math.max(0, Math.min(100, percent));

    document.getElementById("progress-text")
        .textContent = message;

    document.getElementById("progress-percent")
        .textContent = `${Math.round(percent)}%`;

    document.getElementById("progress-fill")
        .style.width = `${percent}%`;
}


function hideProgress() {
    document
        .getElementById("progress-container")
        .classList.add("hidden");
}