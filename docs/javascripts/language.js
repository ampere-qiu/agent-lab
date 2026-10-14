// Link to the same section on the public lesson when the section exists here.
function updateTranslationSection() {
  const fragment = window.location.hash;
  const heading = fragment ? document.getElementById(decodeURIComponent(fragment.slice(1))) : null;
  document.querySelectorAll('[data-course-translate]').forEach((link) => {
    const translationUrl = new URL(link.href);
    const publicPage = new URL(translationUrl.searchParams.get('u'));
    publicPage.hash = heading ? fragment : '';
    translationUrl.searchParams.set('u', publicPage.href);
    link.href = translationUrl.href;
  });
}
updateTranslationSection();
window.addEventListener('hashchange', updateTranslationSection);
