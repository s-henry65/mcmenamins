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
  const alertPlaceholder = document.getElementById('liveAlertPlaceholder')

  const alert = (message, type) => {
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')
  
    alertPlaceholder.append(wrapper)
  }
  
  const alertTrigger = document.getElementById('liveAlertBtn')
  if (alertTrigger) {
    alertTrigger.addEventListener('click', () => {
      alert('Order added to your cart')
    })
  }