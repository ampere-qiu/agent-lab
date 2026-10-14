// Keep the same section when switching languages. Headings share stable IDs.
document.querySelectorAll('[data-course-language]').forEach((link) => {
  if (window.location.hash) link.hash = window.location.hash;
});
document.addEventListener('hashchange', () => {
  document.querySelectorAll('[data-course-language]').forEach((link) => {
    link.hash = window.location.hash;
  });
});
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
