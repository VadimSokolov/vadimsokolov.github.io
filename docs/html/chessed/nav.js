// Load shared navigation
async function loadNavigation() {
    try {
        const response = await fetch('nav.html');
        const navHTML = await response.text();
        
        // Insert navigation into header
        const header = document.querySelector('header .container');
        if (header) {
            header.innerHTML = navHTML;
        }
        
        // Highlight active page
        highlightActivePage();
        
    } catch (error) {
        console.error('Error loading navigation:', error);
    }
}

// Highlight the active page in navigation
function highlightActivePage() {
    const currentPage = window.location.pathname.split('/').pop();
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        // Remove any existing active styles
        link.style.background = '';
        link.style.color = '';
        
        const href = link.getAttribute('href');
        
        // Check if this link matches the current page
        if (href === currentPage || 
            (currentPage === 'index.html' && href === 'index.html') ||
            (currentPage === 'chess-camps.html' && href === 'chess-camps.html') ||
            (currentPage === 'school-programs.html' && href === 'school-programs.html') ||
            (currentPage === 'tournaments.html' && href === 'tournaments.html') ||
            (currentPage === '' && href === 'index.html') ||
            (href.includes('#') && href.split('#')[0] === currentPage)) {
            
            // Apply active styles
            link.style.background = 'rgba(255,255,255,0.2)';
            link.style.color = '#f39c12';
        }
    });
}

// Load navigation when page loads
document.addEventListener('DOMContentLoaded', loadNavigation); 