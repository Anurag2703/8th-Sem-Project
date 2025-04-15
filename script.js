const navbarLinks = document.querySelectorAll('.navbar-link');

navbarLinks.forEach(link => {
    link.addEventListener('mouseenter', () => {
        navbarLinks.forEach(otherLink => {
            if (otherLink !== link) {
                otherLink.classList.add('blur');
            }
        });
    });

    link.addEventListener('mouseleave', () => {
        navbarLinks.forEach(otherLink => {
            otherLink.classList.remove('blur');
        });
    });
});


// HAM BURGER MENU
document.addEventListener('DOMContentLoaded', () => {
    const hamburger = document.getElementById('hamburger');
    const navbarList = document.getElementById('navbar-list');

    hamburger.addEventListener('click', () => {
        navbarList.classList.toggle('active');
    });
});