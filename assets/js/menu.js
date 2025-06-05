// Menu toggle functionality
let menuEventListener = null;

function toggleMenu() {
    const menu = document.querySelector('.mobile-menu');
    menu.classList.toggle('active');
    
    // Remove existing event listener if any
    if (menuEventListener) {
        document.removeEventListener('click', menuEventListener);
    }
    
    // Add new event listener
    menuEventListener = function closeMenu(e) {
        if (!menu.contains(e.target) && !e.target.closest('button')) {
            menu.classList.remove('active');
            document.removeEventListener('click', menuEventListener);
            menuEventListener = null;
        }
    };
    
    // Add event listener with a small delay to prevent immediate trigger
    setTimeout(() => {
        document.addEventListener('click', menuEventListener);
    }, 100);
}

// Function to get current page path
function getCurrentPage() {
    return window.location.pathname.split('/').pop() || 'index.html';
}

// Function to check if a link is active
function isActiveLink(href) {
    const currentPage = getCurrentPage();
    return href === currentPage || (currentPage === '' && href === 'index.html');
}

// Function to update active states
function updateActiveStates() {
    const links = document.querySelectorAll('.nav-links a, .mobile-menu a');
    links.forEach(link => {
        if (isActiveLink(link.getAttribute('href'))) {
            link.setAttribute('aria-current', 'page');
            link.classList.add('active');
        } else {
            link.removeAttribute('aria-current');
            link.classList.remove('active');
        }
    });
}

// Initialize menu on page load
document.addEventListener('DOMContentLoaded', () => {
    updateActiveStates();
}); 