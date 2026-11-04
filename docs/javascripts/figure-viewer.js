/* Shared figures retain their original files; ordinary links also work without JS. */
(() => {
  const ja = document.documentElement.lang.startsWith('ja');
  const labels = ja
    ? { title: '図を拡大', in: '拡大 ＋', out: '縮小 −', fit: '全体を表示', original: '元の画像を開く', close: '閉じる' }
    : { title: 'Enlarge figure', in: 'Zoom in +', out: 'Zoom out −', fit: 'Fit image', original: 'Open original image', close: 'Close' };
  let dialog, stage, picture, original, caption, status, zoom = 1, baseWidth = 0, opener;

  function resize() {
    picture.style.width = `${Math.round(baseWidth * zoom)}px`;
    status.textContent = `${Math.round(zoom * 100)}%`;
  }

  function fit() {
    baseWidth = Math.max(1, Math.min(picture.naturalWidth || 900, stage.clientWidth - 24));
    zoom = 1;
    resize();
    stage.scrollTop = stage.scrollLeft = 0;
  }

  function createViewer() {
    dialog = document.createElement('dialog');
    dialog.className = 'course-figure-viewer';
    dialog.setAttribute('aria-labelledby', 'course-figure-caption');
    const header = document.createElement('header');
    caption = document.createElement('h2');
    caption.id = 'course-figure-caption';
    header.append(caption);
    const controls = document.createElement('div');
    controls.className = 'course-figure-controls';
    const button = (label, action) => {
      const element = document.createElement('button');
      element.type = 'button';
      element.textContent = label;
      element.addEventListener('click', action);
      controls.append(element);
      return element;
    };
    button(labels.out, () => { zoom = Math.max(0.5, zoom - 0.25); resize(); });
    status = document.createElement('output');
    status.setAttribute('aria-live', 'polite');
    controls.append(status);
    button(labels.in, () => { zoom = Math.min(4, zoom + 0.25); resize(); });
    button(labels.fit, fit);
    original = document.createElement('a');
    original.textContent = labels.original;
    controls.append(original);
    const close = button(labels.close, () => dialog.close());
    close.autofocus = true;
    stage = document.createElement('div');
    stage.className = 'course-figure-stage';
    stage.tabIndex = 0;
    stage.setAttribute('aria-label', ja ? '拡大した図。矢印キーでスクロールできます。' : 'Enlarged figure. Use arrow keys to scroll.');
    picture = document.createElement('img');
    picture.addEventListener('load', fit);
    stage.append(picture);
    dialog.append(header, controls, stage);
    dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
    dialog.addEventListener('close', () => { if (opener) opener.focus(); });
    document.body.append(dialog);
  }

  function init() {
    const figures = new Map();
    document.querySelectorAll('a.course-figure-link').forEach(link => {
      const img = link.querySelector('img');
      if (img) {
        figures.set(link.href, img);
        link.title = labels.title;
      }
    });
    if (!figures.size) return;
    document.querySelectorAll('.md-content a[href]').forEach(link => {
      const source = figures.get(link.href);
      if (!source) return;
      link.addEventListener('click', event => {
        if (event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        if (typeof HTMLDialogElement === 'undefined') return;
        event.preventDefault();
        if (!dialog) createViewer();
        opener = link;
        caption.textContent = source.alt || labels.title;
        original.href = link.href;
        picture.alt = source.alt;
        picture.src = link.href;
        dialog.showModal();
        if (picture.complete) fit();
      });
    });
    window.addEventListener('resize', () => { if (dialog && dialog.open) fit(); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();
})();
