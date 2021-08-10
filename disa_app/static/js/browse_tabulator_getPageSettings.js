

const pageSettingsURL = `${window.location.pathname}?format=json`;

const srPageSettings = fetch(pageSettingsURL)
  .then(response => {
    if (!response.ok) {
      throw new Error('Network response was not ok');
    } else {
      return response.json();
    }
  })
  .catch(error => {
    console.error("Couldn't load SR settings", error);
  });

export default await srPageSettings;

