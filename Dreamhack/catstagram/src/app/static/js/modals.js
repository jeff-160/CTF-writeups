// Modal and Flash Message System for Catstagram

document.addEventListener('DOMContentLoaded', function() {
    // Initialize flash message system
    initializeFlashMessages();
    
    // Initialize modal system
    initializeModals();
    
    // Auto-hide flash messages after 5 seconds
    autoHideFlashMessages();
});

// Flash message system
function initializeFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Add close button functionality
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                hideFlashMessage(message);
            });
        }
        
        // Make messages clickable to dismiss
        message.addEventListener('click', function(e) {
            if (e.target !== closeBtn) {
                hideFlashMessage(message);
            }
        });
    });
}

function hideFlashMessage(message) {
    message.classList.add('fade-out');
    setTimeout(() => {
        message.remove();
    }, 300);
}

function autoHideFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        setTimeout(() => {
            if (message.parentElement) {
                hideFlashMessage(message);
            }
        }, 5000); // Hide after 5 seconds
    });
}

// Modal system
function initializeModals() {
    // Close modal when clicking outside
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal')) {
            closeModal(e.target);
        }
    });
    
    // Close modal with close button
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('modal-close')) {
            const modal = e.target.closest('.modal');
            closeModal(modal);
        }
    });
    
    // Close modal with Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const openModal = document.querySelector('.modal.show');
            if (openModal) {
                closeModal(openModal);
            }
        }
    });
}

function showModal(type, title, message, buttons = null) {
    // Remove existing modal
    const existingModal = document.querySelector('.modal');
    if (existingModal) {
        existingModal.remove();
    }
    
    // Create modal HTML
    const modal = document.createElement('div');
    modal.className = 'modal';
    
    const iconMap = {
        'success': '✅',
        'error': '❌',
        'info': 'ℹ️',
        'warning': '⚠️'
    };
    
    const defaultButtons = buttons || [
        { text: 'OK', class: 'modal-btn-primary', action: 'close' }
    ];
    
    modal.innerHTML = `
        <div class="modal-content">
            <button class="modal-close">&times;</button>
            <div class="modal-icon ${type}">${iconMap[type] || 'ℹ️'}</div>
            <h3 class="modal-title">${title}</h3>
            <p class="modal-message">${message}</p>
            <div class="modal-buttons">
                ${defaultButtons.map(btn => 
                    `<button class="modal-btn ${btn.class}" data-action="${btn.action}">${btn.text}</button>`
                ).join('')}
            </div>
        </div>
    `;
    
    // Add to document
    document.body.appendChild(modal);
    
    // Show modal
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
    
    // Add button event listeners
    modal.querySelectorAll('.modal-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const action = this.dataset.action;
            
            if (action === 'close') {
                closeModal(modal);
            } else if (action === 'redirect') {
                const url = this.dataset.url;
                if (url) {
                    window.location.href = url;
                }
            } else if (action === 'reload') {
                window.location.reload();
            }
        });
    });
    
    return modal;
}

function closeModal(modal) {
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            modal.remove();
        }, 300);
    }
}

// Success modal
function showSuccessModal(title, message, redirectUrl = null) {
    const buttons = redirectUrl ? [
        { text: 'Continue', class: 'modal-btn-primary', action: 'redirect', url: redirectUrl }
    ] : [
        { text: 'OK', class: 'modal-btn-primary', action: 'close' }
    ];
    
    return showModal('success', title, message, buttons);
}

// Error modal
function showErrorModal(title, message) {
    return showModal('error', title, message, [
        { text: 'Try Again', class: 'modal-btn-primary', action: 'close' }
    ]);
}

// Confirmation modal
function showConfirmModal(title, message, onConfirm, onCancel = null) {
    const modal = showModal('warning', title, message, [
        { text: 'Cancel', class: 'modal-btn-secondary', action: 'close' },
        { text: 'Confirm', class: 'modal-btn-primary', action: 'confirm' }
    ]);
    
    // Add confirm action
    const confirmBtn = modal.querySelector('[data-action="confirm"]');
    confirmBtn.addEventListener('click', function() {
        closeModal(modal);
        if (onConfirm) onConfirm();
    });
    
    const cancelBtn = modal.querySelector('[data-action="close"]');
    cancelBtn.addEventListener('click', function() {
        closeModal(modal);
        if (onCancel) onCancel();
    });
    
    return modal;
}

// Toast notification (simpler alternative)
function showToast(message, type = 'info', duration = 3000) {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.animation = 'slideUp 0.3s ease-out reverse';
        setTimeout(() => {
            toast.remove();
        }, 300);
    }, duration);
    
    return toast;
}

// Form validation with modals
function validateForm(formElement) {
    const requiredFields = formElement.querySelectorAll('[required]');
    let isValid = true;
    let firstInvalidField = null;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('error');
            if (!firstInvalidField) {
                firstInvalidField = field;
            }
        } else {
            field.classList.remove('error');
        }
    });
    
    if (!isValid && firstInvalidField) {
        firstInvalidField.focus();
        showErrorModal('Form Error', 'Please fill in all required fields.');
        return false;
    }
    
    return true;
}

// Enhanced form submission with loading states
function handleFormSubmission(form, loadingText = 'Processing...') {
    const submitBtn = form.querySelector('button[type="submit"]');
    const originalText = submitBtn.textContent;
    
    // Show loading state
    submitBtn.disabled = true;
    submitBtn.textContent = loadingText;
    
    // Create a promise that resolves when form is submitted
    return new Promise((resolve, reject) => {
        // Restore button after a timeout (fallback)
        setTimeout(() => {
            submitBtn.disabled = false;
            submitBtn.textContent = originalText;
            resolve();
        }, 2000);
    });
}

// Global functions for easy access
window.showModal = showModal;
window.showSuccessModal = showSuccessModal;
window.showErrorModal = showErrorModal;
window.showConfirmModal = showConfirmModal;
window.showToast = showToast;
window.closeModal = closeModal;
