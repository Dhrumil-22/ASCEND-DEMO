// ASCEND - Main JavaScript File

// Toast Notification System
class ToastManager {
    constructor() {
        this.container = this.createContainer();
    }

    createContainer() {
        let container = document.querySelector('.toast-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'toast-container';
            document.body.appendChild(container);
        }
        return container;
    }

    show(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `toast alert-${type}`;
        toast.textContent = message;

        this.container.appendChild(toast);

        // Auto remove after 5 seconds
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 5000);
    }
}

const toastManager = new ToastManager();

// Form Validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;

    const inputs = form.querySelectorAll('[required]');
    let isValid = true;

    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
            input.classList.add('is-valid');
        }
    });

    return isValid;
}

// Real-time input validation
document.addEventListener('DOMContentLoaded', () => {
    const requiredInputs = document.querySelectorAll('[required]');

    requiredInputs.forEach(input => {
        input.addEventListener('blur', () => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            }
        });

        input.addEventListener('input', () => {
            if (input.classList.contains('is-invalid') && input.value.trim()) {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            }
        });
    });
});

// Confirmation Dialogs
function confirmAction(message) {
    return confirm(message);
}

// Search/Filter functionality
function filterList(searchInputId, listClass) {
    const searchInput = document.getElementById(searchInputId);
    if (!searchInput) return;

    searchInput.addEventListener('input', (e) => {
        const searchTerm = e.target.value.toLowerCase();
        const items = document.querySelectorAll(`.${listClass}`);

        items.forEach(item => {
            const text = item.textContent.toLowerCase();
            if (text.includes(searchTerm)) {
                item.style.display = '';
            } else {
                item.style.display = 'none';
            }
        });
    });
}

// Auto-save draft functionality
class DraftManager {
    constructor(formId, storageKey) {
        this.form = document.getElementById(formId);
        this.storageKey = storageKey;

        if (this.form) {
            this.init();
        }
    }

    init() {
        // Load saved draft
        this.loadDraft();

        // Auto-save on input
        const inputs = this.form.querySelectorAll('input, textarea, select');
        inputs.forEach(input => {
            input.addEventListener('input', () => this.saveDraft());
        });

        // Clear draft on submit
        this.form.addEventListener('submit', () => this.clearDraft());
    }

    saveDraft() {
        const formData = new FormData(this.form);
        const data = {};

        formData.forEach((value, key) => {
            data[key] = value;
        });

        localStorage.setItem(this.storageKey, JSON.stringify(data));
        console.log('Draft saved');
    }

    loadDraft() {
        const savedData = localStorage.getItem(this.storageKey);
        if (!savedData) return;

        const data = JSON.parse(savedData);

        Object.keys(data).forEach(key => {
            const input = this.form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
            }
        });

        toastManager.show('Draft loaded', 'info');
    }

    clearDraft() {
        localStorage.removeItem(this.storageKey);
    }
}

// Character counter for textareas
function addCharacterCounter(textareaId, maxLength = null) {
    const textarea = document.getElementById(textareaId);
    if (!textarea) return;

    const counter = document.createElement('small');
    counter.className = 'form-text text-right';
    textarea.parentElement.appendChild(counter);

    function updateCounter() {
        const length = textarea.value.length;
        if (maxLength) {
            counter.textContent = `${length} / ${maxLength} characters`;
            if (length > maxLength) {
                counter.style.color = 'var(--danger-color)';
            } else {
                counter.style.color = 'var(--text-secondary)';
            }
        } else {
            counter.textContent = `${length} characters`;
        }
    }

    textarea.addEventListener('input', updateCounter);
    updateCounter();
}

// Loading overlay
function showLoading() {
    const overlay = document.createElement('div');
    overlay.className = 'loading-overlay';
    overlay.id = 'loading-overlay';
    overlay.innerHTML = '<div class="spinner"></div>';
    document.body.appendChild(overlay);
}

function hideLoading() {
    const overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// Smooth scroll to element
function scrollToElement(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Copy to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        toastManager.show('Copied to clipboard!', 'success');
    }).catch(() => {
        toastManager.show('Failed to copy', 'danger');
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    // Add character counters to textareas
    document.querySelectorAll('textarea').forEach(textarea => {
        if (textarea.hasAttribute('maxlength')) {
            addCharacterCounter(textarea.id, textarea.getAttribute('maxlength'));
        }
    });

    // Initialize draft managers for specific forms
    if (document.getElementById('ask-question-form')) {
        new DraftManager('ask-question-form', 'ascend_question_draft');
    }

    if (document.getElementById('answer-form')) {
        new DraftManager('answer-form', 'ascend_answer_draft');
    }

    // Add confirmation to delete/dangerous actions
    document.querySelectorAll('[data-confirm]').forEach(element => {
        element.addEventListener('click', (e) => {
            const message = element.getAttribute('data-confirm');
            if (!confirmAction(message)) {
                e.preventDefault();
            }
        });
    });

    // Flash message auto-hide
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 500);
        });
    }, 5000);
});

// Export for use in other scripts
window.ASCEND = {
    toast: toastManager,
    validateForm,
    confirmAction,
    filterList,
    showLoading,
    hideLoading,
    scrollToElement,
    copyToClipboard
};
