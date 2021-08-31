
// Loads the data object associated with this page
//  (accessed via ?format=json)

/* AS OF 2021/08/31, the structure is:

  {
    browse_json_url: "/browse.json",
    browse_logged_in: true,
    info_image_url: "/static/images/info.png",
    redesign_citations_url: "/redesign_citations/",
    user_is_authenticated: true
  }

*/

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

