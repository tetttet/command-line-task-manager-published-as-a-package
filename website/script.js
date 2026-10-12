const contents = document.querySelector('.contents');
const mobile = window.matchMedia('(max-width: 800px)');
const links = [...document.querySelectorAll('.contents nav a')];
const sections = links.map(link => document.querySelector(link.getAttribute('href')));

function setContentsLayout() {
  contents.open = !mobile.matches;
}
setContentsLayout();
mobile.addEventListener('change', setContentsLayout);
for (const link of links) {
  link.addEventListener('click', () => {
    if (mobile.matches) contents.open = false;
  });
}

// Keep native anchors, browser history, and keyboard navigation intact.
let framePending = false;
function updateCurrentSection() {
  const offset = mobile.matches ? 115 : 100;
  let current = sections[0];
  for (const section of sections) {
    if (section.getBoundingClientRect().top <= offset) current = section;
  }
  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 4) {
    current = sections[sections.length - 1];
  }
  for (const link of links) {
    if (link.hash === `#${current.id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  }
  framePending = false;
}
function requestSectionUpdate() {
  if (!framePending) {
    framePending = true;
    requestAnimationFrame(updateCurrentSection);
  }
}
window.addEventListener('scroll', requestSectionUpdate, { passive: true });
window.addEventListener('resize', requestSectionUpdate);
window.addEventListener('load', requestSectionUpdate);
window.addEventListener('hashchange', requestSectionUpdate);
document.querySelectorAll('details').forEach(detail => detail.addEventListener('toggle', requestSectionUpdate));
updateCurrentSection();

let toastTimer;
for (const button of document.querySelectorAll('[data-copy]')) {
  button.hidden = false;
  button.addEventListener('click', async () => {
    const value = document.getElementById(button.dataset.copy).textContent;
    const status = document.querySelector('.copy-status');
    try {
      await navigator.clipboard.writeText(value);
      status.textContent = 'Commands copied.';
    } catch {
      status.textContent = 'Select the commands and copy them manually.';
    }
    clearTimeout(toastTimer);
    status.classList.add('visible');
    toastTimer = setTimeout(() => status.classList.remove('visible'), 3500);
  });
}
