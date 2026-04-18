// FINNY Finance App - Frontend
// Handle form submission and display purchases from the backend

// Configuration
const API_URL = 'http://localhost:5000';

// DOM Elements
const form = document.getElementById('purchase-form');
const nameInput = document.getElementById('purchase-name');
const amountInput = document.getElementById('purchase-amount');
const categoryInput = document.getElementById('purchase-category');
const purchasesList = document.getElementById('purchases-list');
const totalAmount = document.getElementById('total-amount');
const totalSection = document.getElementById('total-section');
const errorMessage = document.getElementById('error-message');
const successMessage = document.getElementById('success-message');
const submitBtn = document.getElementById('submit-btn');
const spinner = submitBtn.querySelector('.spinner');
const buttonText = submitBtn.querySelector('.button-text');

// Initialize app - load purchases on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('FINNY App loaded');
    loadPurchases();
});

// Handle form submission
form.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    // Get form values
    const name = nameInput.value.trim();
    const amount = parseFloat(amountInput.value);
    const category = categoryInput.value || 'Other';
    
    // Validate inputs
    if (!name || !amount || amount <= 0) {
        showError('Please fill in all fields with valid data');
        return;
    }
    
    // Send POST request to backend
    await addPurchase(name, amount, category);
});

/**
 * Send a new purchase to the backend
 * @param {string} name - Purchase name
 * @param {number} amount - Purchase amount
 * @param {string} category - Purchase category
 */
async function addPurchase(name, amount, category) {
    try {
        // Show loading state
        submitBtn.disabled = true;
        spinner.style.display = 'block';
        buttonText.textContent = 'Adding...';
        hideError();
        hideSuccess();
        
        // Create request payload
        const purchaseData = {
            name: name,
            amount: amount,
            category: category
        };
        
        // Send POST request to backend
        const response = await fetch(`${API_URL}/compras`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(purchaseData)
        });
        
        // Parse response
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to add purchase');
        }
        
        // Show success message
        showSuccess(`Purchase "${name}" added successfully!`);
        
        // Clear form
        form.reset();
        
        // Reload purchases list
        await loadPurchases();
        
    } catch (error) {
        console.error('Error adding purchase:', error);
        showError(`Error: ${error.message}`);
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        spinner.style.display = 'none';
        buttonText.textContent = 'Add Purchase';
    }
}

/**
 * Load all purchases from the backend
 */
async function loadPurchases() {
    try {
        // Fetch purchases from backend
        const response = await fetch(`${API_URL}/compras`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        // Parse response
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || 'Failed to load purchases');
        }
        
        // Display purchases
        displayPurchases(data.purchases, data.total);
        
    } catch (error) {
        console.error('Error loading purchases:', error);
        purchasesList.innerHTML = '<li class="empty-message">Unable to load purchases. Check if the server is running.</li>';
        totalSection.style.display = 'none';
    }
}

/**
 * Display purchases on the page
 * @param {Array} purchases - List of purchase objects
 * @param {number} total - Total amount spent
 */
function displayPurchases(purchases, total) {
    // Clear the list
    purchasesList.innerHTML = '';
    
    if (purchases.length === 0) {
        // Show empty state
        purchasesList.innerHTML = '<li class="empty-message">No purchases yet. Add one to get started!</li>';
        totalSection.style.display = 'none';
        return;
    }
    
    // Create list items for each purchase
    purchases.forEach(purchase => {
        const listItem = document.createElement('li');
        listItem.className = 'purchase-item';
        listItem.innerHTML = `
            <div class="purchase-info">
                <div class="purchase-name">${escapeHtml(purchase.name)}</div>
                <div class="purchase-category">${purchase.category}</div>
            </div>
            <div class="purchase-amount">$${purchase.amount.toFixed(2)}</div>
        `;
        purchasesList.appendChild(listItem);
    });
    
    // Show and update total
    totalSection.style.display = 'block';
    totalAmount.textContent = `$${total.toFixed(2)}`;
}

/**
 * Show error message
 * @param {string} message - Error message to display
 */
function showError(message) {
    errorMessage.textContent = message;
    errorMessage.style.display = 'block';
    console.error('Error:', message);
}

/**
 * Hide error message
 */
function hideError() {
    errorMessage.style.display = 'none';
}

/**
 * Show success message
 * @param {string} message - Success message to display
 */
function showSuccess(message) {
    successMessage.textContent = message;
    successMessage.style.display = 'block';
    console.log('Success:', message);
    
    // Auto-hide success message after 3 seconds
    setTimeout(() => {
        successMessage.style.display = 'none';
    }, 3000);
}

/**
 * Hide success message
 */
function hideSuccess() {
    successMessage.style.display = 'none';
}

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} Escaped text
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
