// Both authored editions share stable heading IDs, so switching keeps your section.
function updateLanguageSection() {
  document.querySelectorAll('[data-course-language]').forEach((link) => {
    const target = new URL(link.getAttribute('href'), window.location.href);
    target.hash = window.location.hash;
    link.href = target.href;
  });
}
updateLanguageSection();
window.addEventListener('hashchange', updateLanguageSection);
