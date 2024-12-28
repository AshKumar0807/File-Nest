document.querySelectorAll('[id^="dots-menu-"]').forEach(button => {
    button.addEventListener('click', function () {
        const menuId = this.id.replace('dots-menu-', 'dropdown-menu-');
        const menu = document.getElementById(menuId);
        menu.classList.toggle('hidden');
    });
});