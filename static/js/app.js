// Client-side filter
const filter = document.getElementById('filter');
const rows = document.getElementById('rows');

filter?.addEventListener('input', () => {
  const q = filter.value.toLowerCase();
  for (const tr of rows.querySelectorAll('tr')) {
    const name = tr.querySelector('.name')?.textContent.toLowerCase() || '';
    const category = tr.querySelector('.category')?.textContent.toLowerCase() || '';
    const quantity = tr.querySelector('.quantity')?.textContent.toLowerCase() || '';
    const price = tr.querySelector('.price')?.textContent.toLowerCase() || '';
    const description = tr.querySelector('.description')?.textContent.toLowerCase() || '';

    tr.style.display = (name.includes(q) || category.includes(q) || quantity.includes(q) || price.includes(q) || description.includes(q)) ? '' : 'none';
  }
});

// Edit modal populate
const editModal = document.getElementById('editModal');
editModal?.addEventListener('show.bs.modal', (ev) => {
  const btn = ev.relatedTarget;
  document.getElementById('edit-id').value         = btn.getAttribute('data-id');
  document.getElementById('edit-name').value       = btn.getAttribute('data-name');
  document.getElementById('edit-category').value   = btn.getAttribute('data-category');
  document.getElementById('edit-quantity').value   = btn.getAttribute('data-quantity');
  document.getElementById('edit-price').value      = btn.getAttribute('data-price');
  document.getElementById('edit-description').value= btn.getAttribute('data-description');
});
  document.getElementById('edit-Model Name').value  = activator.getAttribute('data-Model Name');
  document.getElementById('edit-Faction').value = activator.getAttribute('data-Faction');
});
