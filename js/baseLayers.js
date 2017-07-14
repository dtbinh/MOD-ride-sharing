L.mapbox.accessToken = 'pk.eyJ1IjoiZGhlY2h0IiwiYSI6ImNqNHRueTVyeDA3ZmYyd3FuY2NmYW9tNmoifQ.FetU2-IBDcrhTmSKBpFIfA';

  var layers = {
      Streets: L.mapbox.tileLayer('mapbox.streets'),
      Outdoors: L.mapbox.tileLayer('mapbox.outdoors'),
      
  };

  layers.Streets.addTo(map);
  L.control.layers(layers).addTo(map);
