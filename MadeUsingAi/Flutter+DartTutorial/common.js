// Common JavaScript for all chapter pages
// Provides platform detection and toggle functionality

function detectAndSetOS() {
    const ua = navigator.userAgent;
    if (ua.indexOf('Win') > -1) {
        document.body.classList.add('user-os-windows');
    } else if (ua.indexOf('Mac') > -1) {
        document.body.classList.add('user-os-macos');
    } else {
        document.body.classList.add('user-os-windows');
    }
}

function togglePlatform(platform) {
    document.body.classList.remove('user-os-windows', 'user-os-macos');
    document.body.classList.add(`user-os-${platform}`);
}

// Run OS detection when page loads
document.addEventListener('DOMContentLoaded', () => {
    detectAndSetOS();
});
