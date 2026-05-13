/*
SCRIPT.JS - Resume AI Builder JavaScript
========================================

Basic client-side interactivity and utilities.
Keep it simple and vanilla JavaScript (no jQuery needed).
*/

/*=====================================
   UTILITY FUNCTIONS
  ===================================== */

/**
 * Show a notification to the user
 */
function showNotification(message, type = 'info') {
    const notif = document.createElement('div');
    notif.className = `notification ${type}`;
    notif.textContent = message;
    notif.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 16px;
        background: ${type === 'error' ? '#ff6b6b' : type === 'success' ? '#28a745' : '#007bff'};
        color: white;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease;
    `;
    document.body.appendChild(notif);
    
    setTimeout(() => {
        notif.remove();
    }, 3000);
}

/**
 * Format a date string to readable format
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString(undefined, options);
}

/**
 * Copy text to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        showNotification('Copied: ' + text, 'success');
    }).catch(() => {
        // Fallback for older browsers
        const textarea = document.createElement('textarea');
        textarea.value = text;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showNotification('Copied: ' + text, 'success');
    });
}

/*=====================================
   FORM VALIDATION
  ===================================== */

/**
 * Validate email format
 */
function isValidEmail(email) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

/**
 * Validate password strength
 */
function validatePassword(password) {
    const requirements = {
        length: password.length >= 8,
        uppercase: /[A-Z]/.test(password),
        special: /[!@#$%^&*()_+\-=\[\]{};:'"",.<>?/\\|`~]/.test(password),
        numbers: (password.match(/\d/g) || []).length >= 2
    };
    
    return {
        valid: Object.values(requirements).every(r => r),
        requirements
    };
}

/*=====================================
   FILE UPLOAD HANDLING
  ===================================== */

/**
 * Setup drag and drop for file uploads
 */
function setupFileUpload(containerId, inputId) {
    const container = document.getElementById(containerId);
    const input = document.getElementById(inputId);
    
    if (!container || !input) return;
    
    container.addEventListener('dragover', (e) => {
        e.preventDefault();
        container.classList.add('dragover');
    });
    
    container.addEventListener('dragleave', () => {
        container.classList.remove('dragover');
    });
    
    container.addEventListener('drop', (e) => {
        e.preventDefault();
        container.classList.remove('dragover');
        input.files = e.dataTransfer.files;
        input.dispatchEvent(new Event('change'));
    });
    
    container.addEventListener('click', () => {
        input.click();
    });
}

/*=====================================
   TAB SWITCHING
  ===================================== */

/**
 * Switch between tabs
 */
function switchTab(tabName) {
    // Hide all tabs
    const tabs = document.querySelectorAll('[class*="tab-content"]');
    tabs.forEach(tab => {
        tab.style.display = 'none';
    });
    
    // Show selected tab
    const selectedTab = document.getElementById(`tab-${tabName}`);
    if (selectedTab) {
        selectedTab.style.display = 'block';
    }
    
    // Update active button
    const buttons = document.querySelectorAll('[class*="tab-button"]');
    buttons.forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.tab === tabName) {
            btn.classList.add('active');
        }
    });
}

/*=====================================
   FORM SUBMISSION
  ===================================== */

/**
 * Add confirmation to form submissions
 */
function confirmSubmit(formId, message = 'Are you sure?') {
    const form = document.getElementById(formId);
    if (!form) return;
    
    form.addEventListener('submit', (e) => {
        if (!confirm(message)) {
            e.preventDefault();
        }
    });
}

/*=====================================
   REAL-TIME FORM UPDATES
  ===================================== */

/**
 * Update form field state in real-time
 */
function setupRealtimeValidation(fieldId, validationFn, feedbackElementId) {
    const field = document.getElementById(fieldId);
    const feedback = document.getElementById(feedbackElementId);
    
    if (!field || !feedback) return;
    
    field.addEventListener('input', () => {
        const result = validationFn(field.value);
        
        if (result.valid) {
            field.classList.remove('error');
            field.classList.add('valid');
            feedback.textContent = result.message || '✓';
            feedback.style.color = '#28a745';
        } else {
            field.classList.add('error');
            field.classList.remove('valid');
            feedback.textContent = result.message || '✗';
            feedback.style.color = '#ff6b6b';
        }
    });
}

/*=====================================
   SMOOTH SCROLL
  ===================================== */

/**
 * Add smooth scroll behavior to all links
 */
function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

/*=====================================
   KEYBOARD SHORTCUTS
  ===================================== */

/**
 * Add keyboard shortcuts
 */
function setupKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Alt + S: Focus on search
        if (e.altKey && e.key === 's') {
            e.preventDefault();
            const search = document.querySelector('[type="search"]');
            if (search) search.focus();
        }
        
        // Escape: Close modals
        if (e.key === 'Escape') {
            // Add modal closing logic here if needed
        }
    });
}

/*=====================================
   PAGE INITIALIZATION
  ===================================== */

/**
 * Initialize everything when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    // Add any page-specific initialization here
    console.log('Resume AI Builder initialized');
});

/*=====================================
   ACCESSIBILITY
  ===================================== */

/**
 * Add ARIA labels for better accessibility
 */
function improveAccessibility() {
    // Add aria-labels to interactive elements if missing
    document.querySelectorAll('button:not([aria-label])').forEach(btn => {
        if (!btn.textContent.trim()) {
            btn.setAttribute('aria-label', 'Button');
        }
    });
}

/*=====================================
   ANIMATIONS
  ===================================== */

// Add CSS animation for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes fadeIn {
        from {
            opacity: 0;
        }
        to {
            opacity: 1;
        }
    }
    
    input.valid {
        border-color: #28a745 !important;
    }
    
    input.error {
        border-color: #ff6b6b !important;
    }
`;
document.head.appendChild(style);

// Initialize accessibility improvements
improveAccessibility();

// Initialize chat widget only for logged-in users
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is logged in by checking if the logout button exists
    const logoutBtn = document.querySelector('.btn-logout');
    const isLoggedIn = logoutBtn !== null;
    
    // Initialize chat widget with login status
    const chatWidget = new ChatWidget(isLoggedIn);
});

