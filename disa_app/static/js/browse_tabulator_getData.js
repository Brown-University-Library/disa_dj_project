
// Loads the SR data

async function getStolenRelationsData(url) {

  const loadingModalElem = document.getElementById('loadingModal'),
        loadingModal = new bootstrap.Modal(loadingModalElem);

  loadingModal.show();

  const data = await fetch(url).then(response => {
    if (!response.ok) {
      throw new Error(`Status ${response.status} (${response.statusText})`);
    } else {
      // Not sure why, but Bootstrap requires a delay here ...
      window.setTimeout(() => loadingModal.hide(), 1000);
      return response.json();
    }
  })
  .catch(error => {
    document.getElementById('loadingModalMessage').innerHTML = `
      Couldn't load Stolen Relations data<br />${error}
    `;
    console.error("Couldn't load Stolen Relations data", error);
  });

  return data;
}

export { getStolenRelationsData }

