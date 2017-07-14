// Overlays image based on coordinates of corners


L.mapbox.accessToken = 'pk.eyJ1IjoiZGhlY2h0IiwiYSI6ImNqNHRueTVyeDA3ZmYyd3FuY2NmYW9tNmoifQ.FetU2-IBDcrhTmSKBpFIfA';
      var imageUrl = '/Users/dhecht/Desktop/sim.png',
            // This is the trickiest part - you'll need accurate coordinates for the
            // corners of the image. You can find and create appropriate values at
            // http://maps.nypl.org/warper/ or
            // http://www.georeferencer.org/
      imageBounds = L.latLngBounds([
        [40.6994, -73.9064],
        [40.8782, -74.0190]]);

      var tiles = L.tileLayer('https://api.mapbox.com/styles/v1/mapbox/traffic-day-v2/tiles/256/{z}/{x}/{y}?access_token=pk.eyJ1IjoiZGhlY2h0IiwiYSI6ImNqNHRueTVyeDA3ZmYyd3FuY2NmYW9tNmoifQ.FetU2-IBDcrhTmSKBpFIfA')
      
      var map = L.mapbox.map('map')
        .fitBounds(imageBounds);
        .addLayer(tiles)
             // See full documentation for the ImageOverlay type:
             // http://leafletjs.com/reference.html#imageoverlay
      var overlay = L.imageOverlay(imageUrl, imageBounds)
         .addTo(map);




