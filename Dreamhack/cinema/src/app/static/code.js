document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('cinemaVideo');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const videoContainer = document.getElementById('videoContainer');
    
    function togglePlayPause() {
        if (video.paused) {
            video.play();
            playPauseBtn.textContent = 'Pause';
            playPauseBtn.style.opacity = '0';
        } else {
            video.pause();
            playPauseBtn.textContent = 'Play';
            playPauseBtn.style.opacity = '0.8';
        }
    }

    playPauseBtn.addEventListener('click', togglePlayPause);
    
    video.addEventListener('play', () => {
        playPauseBtn.textContent = 'Pause';
        playPauseBtn.style.opacity = '0';
    });

    video.addEventListener('pause', () => {
        playPauseBtn.textContent = 'Play';
        playPauseBtn.style.opacity = '0.8';
    });

    videoContainer.addEventListener('mouseover', () => {
        playPauseBtn.style.opacity = '0.8';
    });

    videoContainer.addEventListener('mouseout', () => {
        if (!video.paused) {
            playPauseBtn.style.opacity = '0';
        }
    });

    video.play().catch(error => {
        console.log("Autoplay was prevented. User interaction may be required to start the video.");
        playPauseBtn.style.opacity = '0.8';
    });
});

window.addEventListener('load', () => {
    let params = new URLSearchParams(window.location.search);
    let xss = params.get('xss');
    let sanitize_xss = DOMPurify.sanitize(xss);
    document.getElementById("cinemaVideo").innerHTML = sanitize_xss;
});