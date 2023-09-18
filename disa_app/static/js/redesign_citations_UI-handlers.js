

// Go to Source's edit form

function openSourceEditPage(sourceId) {
  window.location.href = `./${sourceId}`;
}

// NOT USED: Set up handler for "show details"

function initToggleTableDetailsButton(table) {
  const showDetailsSwitch = document.getElementById('show-details'),
      showOnlyCurrentUserSwitch = document.getElementById('current-user-only');
  showDetailsSwitch.addEventListener('change', function() {
      const colOp = showDetailsSwitch.checked ? 'showColumn' : 'hideColumn';
      table[colOp]('id');
      table[colOp]('date');
      if (!showOnlyCurrentUserSwitch.checked) {
          table[colOp]('editor');
      }
  });
  showDetailsSwitch.dispatchEvent(new Event('change'));
}

// Set up handler for "show current user" --
//  sets "editor" filter field & hides editor column

function initShowOnlyCurrentUserButton(table, editorFilterElem) {
  const userEmail = window.sr.userEmail;
  const showOnlyCurrentUserButton = document.getElementById('current-user-only');
  showOnlyCurrentUserButton.addEventListener('change', function() {
      if (showOnlyCurrentUserButton.checked) {
          editorFilterElem.value = userEmail;
          editorFilterElem.parentNode.hidden = true;
          table.hideColumn('editor');
          editorFilterElem.dispatchEvent(new Event('input'));
      } else {
          editorFilterElem.value = '';
          editorFilterElem.parentNode.hidden = false;
          table.showColumn('editor');
          editorFilterElem.dispatchEvent(new Event('input'));
      }
  });
  showOnlyCurrentUserButton.checked = true;
  showOnlyCurrentUserButton.dispatchEvent(new Event('change'));
}

export { openSourceEditPage, initShowOnlyCurrentUserButton }