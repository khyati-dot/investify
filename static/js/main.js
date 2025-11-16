// Main JavaScript file for Investify
// This file contains common JavaScript functionality

console.log('Investify app loaded successfully!');

// Common utility functions
function showMessage(message, type = 'info') {
    // Function to show messages to users
    console.log(`${type.toUpperCase()}: ${message}`);
}

// Add any global JavaScript functionality here
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, Investify ready!');
});
