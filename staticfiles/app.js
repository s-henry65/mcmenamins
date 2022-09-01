let latX = null;
let lngX = null;

  window.addEventListener("DOMContentLoaded", (event) => {
    const propNum = document.getElementById("title");
    const propertyNum = propNum.getAttribute("prop_num");
    fetch(`http://127.0.0.1:8000/api/property/${propertyNum}`)
      .then((response) => response.json())
      .then((data) => {
        latX = data.latitude;
        lngX = data.longitude;
        googleMaps();
      });
  });

  function initMap() {
  const position = { lat: latX, lng: lngX };
  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 12,
    center: position,
  });
  const marker = new google.maps.Marker({
    position: position,
    map: map,
  });
}
  async function googleMaps() { 
    const res = await fetch("http://127.0.0.1:8000/static/key.json");
    const data = await res.json();
    let script = document.createElement("script");
    script.src = `https://maps.googleapis.com/maps/api/js?key=${data.key}`;
    document.body.append(script);
  }

