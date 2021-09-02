
// Loads the SR data

async function getStolenRelationsData(url) {
  const data = await fetch(url).then(response => {
    if (!response.ok) {
      throw new Error("Couldn't load Stolen Relations data");
    } else {
      return response.json();
    }
  })
  .catch(error => {
    console.error("Couldn't load Stolen Relations data", error);
  });
  return data;
}

export { getStolenRelationsData }

