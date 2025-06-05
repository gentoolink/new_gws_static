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