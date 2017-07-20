L.mapbox.accessToken = 'pk.eyJ1IjoiZGhlY2h0IiwiYSI6ImNqNHRueTVyeDA3ZmYyd3FuY2NmYW9tNmoifQ.FetU2-IBDcrhTmSKBpFIfA';
     
     
     var layers = document.getElementById('menu-ui');

     addLayer(L.mapbox.styleLayer('mapbox://styles/mapbox/traffic-day-v2'), 'Traffic Day',1); //traffic-night-v2
     addLayer(L.mapbox.styleLayer('mapbox://styles/mapbox/traffic-night-v2'), 'Traffic Night',2); //traffic-night-v2
     // addLayer(L.mapbox.featureLayer('mapbox.oneway'), 'One-Way Streets', 4);
     addLayer(L.mapbox.featureLayer('https://www.mapbox.com/mapbox.js/assets/data/stations.geojson'), 'Public Transport Stations', 3);
    

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
