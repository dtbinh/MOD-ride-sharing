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
      var map = L.mapbox.map('map', 'mapbox.streets')
        .fitBounds(imageBounds);
             // See full documentation for the ImageOverlay type:
             // http://leafletjs.com/reference.html#imageoverlay
      var overlay = L.imageOverlay(imageUrl, imageBounds)
         .addTo(map);




