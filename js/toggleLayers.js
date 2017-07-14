L.mapbox.accessToken = 'pk.eyJ1IjoiZGhlY2h0IiwiYSI6ImNqNHRueTVyeDA3ZmYyd3FuY2NmYW9tNmoifQ.FetU2-IBDcrhTmSKBpFIfA';
     var layers = document.getElementById('menu-ui');

     // addLayer(L.mapbox.tileLayer('mapbox.traffic-night-v2'), 'Night View', 1);
     addLayer(L.mapbox.tileLayer('mapbox.oneway'), 'High-Demand Areas', 1);
     addLayer(L.mapbox.tileLayer('mapbox.rail-metro'), 'Public Transport Stations', 2);

     function addLayer(layer, name, zIndex) {
         layer
             .setZIndex(zIndex)
             .addTo(map);

         // Create a simple layer switcher that
         // toggles layers on and off.
         var link = document.createElement('a');
             link.href = '#';
             link.className = 'active';
             link.innerHTML = name;

         link.onclick = function(e) {
             e.preventDefault();
             e.stopPropagation();

             if (map.hasLayer(layer)) {
                 map.removeLayer(layer);
                 this.className = '';
             } else {
                 map.addLayer(layer);
                 this.className = 'active';
             }
         };

    layers.appendChild(link);
}
