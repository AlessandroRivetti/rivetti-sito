/* Funzioni comuni (home e pagina recensioni) */
window.RI = (function () {
  const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
  const words = t => String(t || '').trim().split(/\s+/).filter(Boolean).length;
  const stars = n => {
    n = Math.max(0, Math.min(5, Math.round(n)));
    return '<span class="stars" role="img" aria-label="' + n + ' stelle su 5">' + '★'.repeat(n) + '<span class="off">' + '★'.repeat(5 - n) + '</span></span>';
  };
  return { esc, words, stars };
})();
