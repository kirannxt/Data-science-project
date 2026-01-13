// Main JavaScript for Sleep Stress Detection App

document.addEventListener('DOMContentLoaded', function() {
    console.log('Sleep Stress Detection App Loaded');
    initializeApp();
});

function initializeApp() {
    // Initialize mobile menu toggle
    initMobileMenu();
    
    // Initialize form validation
    initFormValidation();
}

function initMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
}

function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add custom validation if needed
            console.log('Form submitted');
        });
    });
}

// Sleep form specific validation
function validateSleepForm() {
    const sleepDuration = parseFloat(document.getElementById('sleep_duration')?.value || 0);
    const sleepQuality = parseInt(document.getElementById('sleep_quality')?.value || 0);
    const sleepCycles = parseInt(document.getElementById('sleep_cycles')?.value || 0);
    
    if (sleepDuration < 0 || sleepDuration > 12) {
        alert('Sleep duration must be between 0 and 12 hours');
        return false;
    }
    
    if (sleepQuality < 1 || sleepQuality > 10) {
        alert('Sleep quality must be between 1 and 10');
        return false;
    }
    
    if (sleepCycles < 3 || sleepCycles > 6) {
        alert('Sleep cycles must be between 3 and 6');
        return false;
    }
    
    return true;
}

// API call for prediction
async function makePrediction(data) {
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Prediction failed');
        }
    } catch (error) {
        console.error('Error:', error);
        return { error: error.message };
    }
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'error' ? '#f44336' : '#4caf50'};
        color: white;
        border-radius: 8px;
        z-index: 1000;
        animation: slideIn 0.3s ease-in;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 3000);
}

function formatDate(date) {
    return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
}

function getStressColor(stressLevel) {
    const colors = {
        'Low Stress': '#4caf50',
        'Medium Stress': '#ff9800',
        'High Stress': '#f44336'
    };
    return colors[stressLevel] || '#999';
}

// Export functions if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        makePrediction,
        showNotification,
        formatDate,
        getStressColor
    };
}
