/* Progressive enhancement: native folders remain usable without JavaScript. */
(() => {
  const explorer = document.querySelector('.skills-explorer');
  if (!explorer) return;

  const toggle = explorer.querySelector('[data-tree-toggle]');
  const branches = [...explorer.querySelectorAll('.skill-branch')];
  if (!toggle || !branches.length) return;

  const ru = toggle.querySelector('.ru');
  const en = toggle.querySelector('.en');
  const sync = () => {
    const anyOpen = branches.some(branch => branch.open);
    ru.textContent = anyOpen ? 'Свернуть всё' : 'Развернуть всё';
    en.textContent = anyOpen ? 'Collapse all' : 'Expand all';
  };

  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    const shouldOpen = !branches.some(branch => branch.open);
    branches.forEach(branch => { branch.open = shouldOpen; });
    sync();
  });
  branches.forEach(branch => branch.addEventListener('toggle', sync));
  sync();
})();
