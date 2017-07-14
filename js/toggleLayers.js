L.mapbox.accessToken = 'pk.eyJ1IjoiZGhlY2h0IiwiYSI6ImNqNHRueTVyeDA3ZmYyd3FuY2NmYW9tNmoifQ.FetU2-IBDcrhTmSKBpFIfA';
     
     
     var layers = document.getElementById('menu-ui');

     addLayer(L.mapbox.styleLayer('https://api.mapbox.com/v1/mapbox.traffic-day-v2.json'), 'Traffic Day',1); //traffic-night-v2
     addLayer(L.mapbox.styleLayer('https://api.mapbox.com/v1/mapbox.traffic-night-v2.json'), 'Traffic Night',2); //traffic-night-v2
     addLayer(L.mapbox.tileLayer('mapbox.oneway'), 'High-Demand Areas', 3);
     addLayer(L.mapbox.tileLayer('mapbox.rail-metro'), 'Public Transport Stations', 4);

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
