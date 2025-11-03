        function detectPlatform(url) {
            if (url.includes('youtube.com') || url.includes('youtu.be')) {
                return 'youtube';
            } else if (url.includes('instagram.com')) {
                return 'instagram';
            } else if (url.includes('facebook.com') || url.includes('fb.watch')) {
                return 'facebook';
            }
            return null;
        }

        function getYouTubeVideoId(url) {
            const regex = /(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/\s]{11})/;
            const match = url.match(regex);
            return match ? match[1] : null;
        }

        function getInstagramEmbedUrl(url) {
            let postUrl = url;
            if (url.includes('/reel/')) {
                postUrl = url.split('?')[0];
            } else if (url.includes('/p/')) {
                postUrl = url.split('?')[0];
            }
            return postUrl.endsWith('/') ? postUrl : postUrl + '/';
        }

        function getFacebookEmbedUrl(url) {
            return url;
        }

        function generateEmbedCode(platform, url, index) {
            let embedHTML = '';
            
            switch(platform) {
                case 'youtube':
                    const videoId = getYouTubeVideoId(url);
                    embedHTML = `
                        <div class="video-wrapper">
                            <iframe 
                                src="https://www.youtube.com/embed/${videoId}" 
                                allowfullscreen
                                loading="lazy"
                            ></iframe>
                            <div class="video-number">YouTube Video #${index}</div>
                        </div>
                    `;
                    break;
                    
                case 'instagram':
                    const instaUrl = getInstagramEmbedUrl(url);
                    embedHTML = `
                        <div class="video-wrapper">
                            <iframe 
                                src="${instaUrl}embed" 
                                allowfullscreen
                                loading="lazy"
                                scrolling="no"
                                style="border: none; overflow: hidden;"
                            ></iframe>
                            <div class="video-number">Instagram Video #${index}</div>
                        </div>
                    `;
                    break;
                    
                case 'facebook':
                    const fbEncodedUrl = encodeURIComponent(url);
                    embedHTML = `
                        <div class="video-wrapper">
                            <iframe 
                                src="https://www.facebook.com/plugins/video.php?href=${fbEncodedUrl}&show_text=false" 
                                allowfullscreen
                                loading="lazy"
                                scrolling="no"
                                style="border: none; overflow: hidden;"
                            ></iframe>
                            <div class="video-number">Facebook Video #${index}</div>
                        </div>
                    `;
                    break;
            }
            
            return embedHTML;
        }

        function showError(message) {
            const errorDiv = document.getElementById('errorMessage');
            errorDiv.textContent = message;
            errorDiv.style.display = 'block';
            setTimeout(() => {
                errorDiv.style.display = 'none';
            }, 5000);
        }

        function generateVideos() {
            const urlInput = document.getElementById('videoUrl').value.trim();
            const count = parseInt(document.getElementById('videoCount').value);
            const container = document.getElementById('videoContainer');

            if (!urlInput) {
                showError('Please enter a video URL');
                return;
            }

            const platform = detectPlatform(urlInput);
            
            if (!platform) {
                showError('Invalid URL. Please enter a valid YouTube, Instagram, or Facebook video link');
                return;
            }

            if (platform === 'youtube' && !getYouTubeVideoId(urlInput)) {
                showError('Invalid YouTube URL. Please check the link and try again');
                return;
            }

            let gridHTML = '<div class="video-grid">';
            
            for (let i = 1; i <= count; i++) {
                gridHTML += generateEmbedCode(platform, urlInput, i);
            }
            
            gridHTML += '</div>';
            container.innerHTML = gridHTML;
        }

        function clearVideos() {
            document.getElementById('videoUrl').value = '';
            document.getElementById('videoCount').value = '5';
            document.getElementById('videoContainer').innerHTML = `
                <div class="empty-state">
                    <svg width="120" height="120" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path>
                        <polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon>
                    </svg>
                    <h3>No Videos Yet</h3>
                    <p>Enter a video URL from YouTube, Instagram, or Facebook to get started</p>
                </div>
            `;
        }

        function autoplayAll() {
            const iframes = document.querySelectorAll('#videoContainer iframe');
            iframes.forEach(iframe => {
                let src = iframe.src;
                if (src.includes('youtube.com') && !src.includes('autoplay')) {
                    const separator = src.includes('?') ? '&' : '?';
                    iframe.src = src + separator + 'autoplay=1&mute=1';
                }
            });
        }

        document.getElementById('videoUrl').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                generateVideos();
            }
        });
