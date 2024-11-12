document.addEventListener('DOMContentLoaded', function () {
    const sidebarToggleButton = document.getElementById('sidebarToggle');
    const sidebar = document.getElementById('sidebar');

    sidebarToggleButton.addEventListener('click', function () {
        sidebar.classList.toggle('active');
    });
});