// This control offers instructions; translation is controlled by the browser.
document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') {
    const menu = document.querySelector('.course-language[open]');
    if (menu) {
      menu.open = false;
      menu.querySelector('summary').focus();
    }
  }
});
document.addEventListener('click', (event) => {
  const menu = document.querySelector('.course-language[open]');
  if (menu && !menu.contains(event.target)) menu.open = false;
});
