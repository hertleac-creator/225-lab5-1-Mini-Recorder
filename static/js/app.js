// ===============================================
// IMPERIAL DATA-SLATE: LOCAL TEXT FILTER
// Filters table rows by name or contact sigil
// ===============================================

const auspexFilter = document.getElementById('filter');
const dataRows = document.getElementById('rows');

auspexFilter?.addEventListener('input', () => {
  const query = auspexFilter.value.toLowerCase();

  for (const row of dataRows.querySelectorAll('tr')) {
    const designation = row.querySelector('.name')?.textContent.toLowerCase() || '';
    const vox = row.querySelector('.phone')?.textContent.toLowerCase() || '';

    // If the row does not match the search, it is purged from view
    row.style.display = (designation.includes(query) || vox.includes(query))
      ? ''
      : 'none';
  }
});


// ===============================================
// ADEPTUS ADMINISTRATUM: EDIT MODAL POPULATION
// Loads unit details into the modal for adjustment
// ===============================================

const editChamber = document.getElementById('editModal');

editChamber?.addEventListener('show.bs.modal', (ev) => {
  const activator = ev.relatedTarget;

  document.getElementById('edit-id').value    = activator.getAttribute('data-id');
  document.getElementById('edit-name').value  = activator.getAttribute('data-name');
  document.getElementById('edit-phone').value = activator.getAttribute('data-phone');
});
