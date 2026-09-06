'use strict';
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
const menuButton = document.querySelector('.menu-toggle');
const mobileMenu = document.querySelector('#mobile-menu');
function closeMenu(restoreFocus = false) {
  if (!menuButton || !mobileMenu) return;
  menuButton.setAttribute('aria-expanded', 'false');
  mobileMenu.hidden = true;
  if (restoreFocus) menuButton.focus();
}
menuButton?.addEventListener('click', () => {
  const opening = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(opening));
  mobileMenu.hidden = !opening;
});
mobileMenu?.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && menuButton?.getAttribute('aria-expanded') === 'true') closeMenu(true); });
document.addEventListener('click', event => { if (!event.target.closest('.site-header')) closeMenu(); });
window.matchMedia('(min-width: 761px)').addEventListener('change', event => { if (event.matches) closeMenu(); });

const explorer = document.querySelector('.system-explorer');
if (explorer) {
  const links = [...explorer.querySelectorAll('[data-system]')];
  const panels = [...explorer.querySelectorAll('.system-panels article')];
  const activate = id => {
    links.forEach(link => link.setAttribute('aria-current', String(link.dataset.system === id)));
    panels.forEach(panel => { panel.hidden = panel.id !== id; });
  };
  explorer.classList.add('enhanced');
  activate(panels.some(panel => '#'+panel.id === location.hash) ? location.hash.slice(1) : panels[0].id);
  links.forEach(link => link.addEventListener('click', event => {
    event.preventDefault();
    activate(link.dataset.system);
  }));
  window.addEventListener('hashchange', () => { if (panels.some(panel => '#'+panel.id === location.hash)) activate(location.hash.slice(1)); });
}

const gallery = document.querySelector('#credential-gallery');
if (gallery) {
  const cards = [...gallery.querySelectorAll('.credential-card')];
  const filters = [...document.querySelectorAll('[data-filter]')];
  const status = document.querySelector('.credential-status');
  const previous = document.querySelector('[data-gallery-prev]');
  const next = document.querySelector('[data-gallery-next]');
  const updateControls = () => {
    previous.disabled = gallery.scrollLeft <= 2;
    next.disabled = gallery.scrollLeft >= gallery.scrollWidth - gallery.clientWidth - 2;
  };
  filters.forEach(button => button.addEventListener('click', () => {
    filters.forEach(filter => filter.setAttribute('aria-pressed', String(filter === button)));
    cards.forEach(card => { card.hidden = button.dataset.filter !== 'all' && card.dataset.group !== button.dataset.filter; });
    gallery.scrollTo({left:0, behavior:'instant'});
    const count = cards.filter(card => !card.hidden).length;
    status.textContent = `${count} credentials · Names supplied in résumé; verification links and dates to be added.`;
    requestAnimationFrame(updateControls);
  }));
  const advance = direction => gallery.scrollBy({left:direction * (gallery.querySelector('.credential-card:not([hidden])').getBoundingClientRect().width + 25), behavior:reducedMotion.matches ? 'instant' : 'smooth'});
  previous.addEventListener('click', () => advance(-1));
  next.addEventListener('click', () => advance(1));
  gallery.addEventListener('scroll', updateControls, {passive:true});
  new ResizeObserver(updateControls).observe(gallery);
  updateControls();
}
const progress = document.querySelector('.reading-progress');
if (progress) {
  let scheduled = false;
  const update = () => {
    const range = document.documentElement.scrollHeight - innerHeight;
    progress.style.width = `${range > 0 ? Math.min(100, Math.max(0, scrollY / range * 100)) : 0}%`;
    scheduled = false;
  };
  window.addEventListener('scroll', () => { if (!scheduled && !reducedMotion.matches) { scheduled = true; requestAnimationFrame(update); } }, {passive:true});
  window.addEventListener('resize', update);
  update();
}
document.querySelectorAll('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
