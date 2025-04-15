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
