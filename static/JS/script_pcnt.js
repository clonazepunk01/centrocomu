function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const contentArea = document.querySelector('.content-area');
    
    sidebar.classList.toggle('active');
    contentArea.classList.toggle('collapsed');
}
