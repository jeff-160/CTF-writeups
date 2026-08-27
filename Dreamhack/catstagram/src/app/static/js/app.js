// Catstagram Interactive Features

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize all interactive features
    initializeLikeButtons();
    initializeFileUpload();
    initializePostAnimations();
    initializeNavigation();
    initializeUploadForm();
    
});

// Initialize upload form validation
function initializeUploadForm() {
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', function(e) {
            const fileInput = document.getElementById('cat_image');
            const file = fileInput.files[0];
            
            if (!file) {
                e.preventDefault();
                showErrorModal('No File Selected', 'Please select an image file to upload.');
                return false;
            }
            
            // Validate form fields
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }
            
            // Double-check file validation before submission
            const filename = file.name.toLowerCase();
            const prohibitedExtensions = ['.html', '.py', '.js', '.css', '.json', '.php', '.exe', '.bat', '.sh', '.sql', '.xml', '.txt', '.md'];
            const isProhibited = prohibitedExtensions.some(ext => filename.endsWith(ext));
            
            if (isProhibited) {
                e.preventDefault();
                showErrorModal('Invalid File Type', 'This file type is not allowed for security reasons.');
                return false;
            }
            
            // Show loading state
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sharing...';
            
            // Show uploading feedback
            showToast('Uploading your cat photo... 📤', 'info', 3000);
        });
    }
}

// Enhanced like button functionality with AJAX
function initializeLikeButtons() {
    document.querySelectorAll('.like-btn').forEach(btn => {
        // Remove default form submission
        const form = btn.closest('form');
        if (form) {
            form.addEventListener('submit', function(e) {
                e.preventDefault();
                handleLikeAction(this);
            });
        }
        
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            const form = this.closest('form');
            if (form) {
                handleLikeAction(form);
            }
        });
    });
}

// Handle like action with AJAX
function handleLikeAction(form) {
    const formData = new FormData(form);
    const catId = formData.get('cat_id');
    const likeBtn = form.querySelector('.like-btn');
    const likeCountSpan = likeBtn.querySelector('span:last-child');
    
    // Add loading state
    likeBtn.disabled = true;
    likeBtn.style.opacity = '0.6';
    
    // Add animation
    likeBtn.classList.add('animate');
    
    // Update heart icon to filled immediately for better UX
    const heartIcon = likeBtn.querySelector('.icon-heart');
    if (heartIcon) {
        heartIcon.classList.add('liked');
    }
    
    // Send AJAX request
    fetch('?action=like', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Update like count
            likeCountSpan.textContent = data.new_like_count;
            
            // Show success feedback
            showToast('Liked! 💕', 'success', 2000);
            
            // Trigger celebration animation
            celebrateLike(likeBtn);
        } else {
            throw new Error('Failed to like');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        
        // Revert heart icon on error
        if (heartIcon) {
            heartIcon.classList.remove('liked');
        }
        
        // Show error feedback
        showToast('Failed to like. Please try again.', 'error', 3000);
    })
    .finally(() => {
        // Remove loading state
        likeBtn.disabled = false;
        likeBtn.style.opacity = '1';
        
        // Remove animation class after animation completes
        setTimeout(() => {
            likeBtn.classList.remove('animate');
        }, 300);
    });
}

// Celebration animation for likes
function celebrateLike(likeBtn) {
    const post = likeBtn.closest('.post');
    if (!post) return;
    
    // Create floating hearts
    for (let i = 0; i < 3; i++) {
        setTimeout(() => {
            createFloatingHeart(likeBtn);
        }, i * 100);
    }
    
    // Add pulse effect to the post
    post.style.transform = 'scale(1.02)';
    post.style.transition = 'transform 0.2s ease-out';
    
    setTimeout(() => {
        post.style.transform = 'scale(1)';
    }, 200);
}

// Create floating heart animation
function createFloatingHeart(element) {
    const heart = document.createElement('div');
    heart.innerHTML = '💕';
    heart.style.cssText = `
        position: absolute;
        font-size: 20px;
        pointer-events: none;
        z-index: 1000;
        animation: heartFloat 2s ease-out forwards;
    `;
    
    // Position relative to the like button
    const rect = element.getBoundingClientRect();
    heart.style.left = (rect.left + Math.random() * 40 - 20) + 'px';
    heart.style.top = (rect.top + Math.random() * 40 - 20) + 'px';
    
    document.body.appendChild(heart);
    
    // Remove heart after animation
    setTimeout(() => {
        heart.remove();
    }, 2000);
}

// File upload preview and validation
function initializeFileUpload() {
    const fileInput = document.getElementById('cat_image');
    const fileLabel = document.querySelector('.file-input-label');
    
    if (fileInput && fileLabel) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            
            if (file) {
                const filename = file.name.toLowerCase();
                
                // Check for prohibited extensions
                const prohibitedExtensions = ['.html', '.py', '.js', '.css', '.json', '.php', '.exe', '.bat', '.sh', '.sql', '.xml', '.txt', '.md'];
                const isProhibited = prohibitedExtensions.some(ext => filename.endsWith(ext));
                
                if (isProhibited) {
                    showErrorModal('Invalid File Type', 'This file type is not allowed. Please upload only image files (jpg, png, gif, etc.).');
                    this.value = '';
                    fileLabel.innerHTML = `
                        <span class="icon icon-camera"></span>
                        Choose a cat photo
                    `;
                    return;
                }
                
                // Check for allowed image extensions
                const allowedExtensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg'];
                const isAllowed = allowedExtensions.some(ext => filename.endsWith(ext));
                
                if (!isAllowed) {
                    showErrorModal('Invalid File Type', 'Please select a valid image file (jpg, png, gif, etc.).');
                    this.value = '';
                    fileLabel.innerHTML = `
                        <span class="icon icon-camera"></span>
                        Choose a cat photo
                    `;
                    return;
                }
                
                // Validate file type using MIME type as well
                if (!file.type.startsWith('image/')) {
                    showErrorModal('Invalid File Type', 'Please select an image file.');
                    this.value = '';
                    fileLabel.innerHTML = `
                        <span class="icon icon-camera"></span>
                        Choose a cat photo
                    `;
                    return;
                }
                
                // Validate file size (max 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    showErrorModal('File Too Large', 'Image file size should be less than 5MB. Please choose a smaller image.');
                    this.value = '';
                    fileLabel.innerHTML = `
                        <span class="icon icon-camera"></span>
                        Choose a cat photo
                    `;
                    return;
                }
                
                // Update label text
                fileLabel.innerHTML = `
                    <span class="icon icon-camera"></span>
                    ${file.name}
                `;
                
                // Show preview (optional enhancement)
                showImagePreview(file);
                
                // Show success feedback
                showToast('Great choice! Ready to share 📸', 'success', 2000);
            }
        });
    }
}

// Show image preview before upload
function showImagePreview(file) {
    const reader = new FileReader();
    reader.onload = function(e) {
        // Remove existing preview
        const existingPreview = document.querySelector('.upload-preview');
        if (existingPreview) {
            existingPreview.remove();
        }
        
        // Create preview container
        const preview = document.createElement('div');
        preview.className = 'upload-preview';
        preview.style.cssText = `
            margin-top: 12px;
            text-align: center;
        `;
        
        // Create preview image
        const img = document.createElement('img');
        img.src = e.target.result;
        img.style.cssText = `
            max-width: 200px;
            max-height: 200px;
            border-radius: 8px;
            border: 1px solid #dbdbdb;
        `;
        
        preview.appendChild(img);
        document.querySelector('.upload-section').appendChild(preview);
    };
    reader.readAsDataURL(file);
}

// Post animations on scroll
function initializePostAnimations() {
    const posts = document.querySelectorAll('.post');
    
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeIn 0.5s ease-out forwards';
            }
        });
    }, observerOptions);
    
    posts.forEach(post => {
        observer.observe(post);
    });
}

// Smooth navigation
function initializeNavigation() {
    // Smooth scroll for internal links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Utility function for smooth scroll to upload
function scrollToUpload() {
    const uploadSection = document.getElementById('upload-section');
    if (uploadSection) {
        uploadSection.scrollIntoView({ 
            behavior: 'smooth',
            block: 'center'
        });
    }
}

// Show loading state for forms
function showLoadingState(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = 'Loading...';
    }
}

// Double-click to like functionality (Instagram-like)
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.post-image').forEach(img => {
        img.addEventListener('dblclick', function(e) {
            e.preventDefault();
            
            // Find the like form for this post
            const post = this.closest('.post');
            const likeForm = post.querySelector('form[action*="like"]');
            
            if (likeForm) {
                // Trigger like action
                handleLikeAction(likeForm);
                
                // Show heart animation at click position
                showHeartAnimation(e.clientX, e.clientY);
            }
        });
        
        // Prevent text selection on double-click
        img.addEventListener('selectstart', function(e) {
            e.preventDefault();
        });
    });
});

// Show floating heart animation on double-click
function showHeartAnimation(x, y) {
    const heart = document.createElement('div');
    heart.innerHTML = '♥';
    heart.style.cssText = `
        position: fixed;
        left: ${x - 15}px;
        top: ${y - 15}px;
        font-size: 30px;
        color: #ed4956;
        pointer-events: none;
        z-index: 10000;
        animation: heartFloat 1s ease-out forwards;
    `;
    
    // Add animation keyframes if not already added
    if (!document.querySelector('#heart-animation-styles')) {
        const style = document.createElement('style');
        style.id = 'heart-animation-styles';
        style.textContent = `
            @keyframes heartFloat {
                0% {
                    opacity: 1;
                    transform: scale(0.8) translateY(0);
                }
                100% {
                    opacity: 0;
                    transform: scale(1.2) translateY(-50px);
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(heart);
    
    // Remove heart after animation
    setTimeout(() => {
        heart.remove();
    }, 1000);
}
