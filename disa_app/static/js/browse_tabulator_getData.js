
// Loads the SR data

async function getStolenRelationsData(url) {

  const loadingModalElem = document.getElementById('loadingModal'),
        loadingModal = new bootstrap.Modal(loadingModalElem),
        hideModalOrSchedule = () => {
          if (loadingModal._isShown) { // Modal can only be hidden once
            loadingModal.hide();       //   it's finished showing
            window.setTimeout(hideModalOrSchedule, 500);
          }
        };

  loadingModal.show();

  const data = await fetch(url).then(response => {
    if (!response.ok) {
      throw new Error(`Status ${response.status} (${response.statusText})`);
    } else {
      hideModalOrSchedule();
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

