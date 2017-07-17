

// Since featureLayer is an asynchronous method, we use the `.on('ready'`
// call to only use its marker data once we know it is actually loaded.

L.mapbox.featureLayer()
    .loadURL('https://www.mapbox.com/mapbox.js/assets/data/stations.geojson')
    .on('ready', function(e) {
    // create a new MarkerClusterGroup that will show special-colored
    // numbers to indicate the type of rail stations it contains
    function makeGroup(color) {
      return new L.MarkerClusterGroup({
        iconCreateFunction: function(cluster) {
          return new L.DivIcon({
            iconSize: [20, 20],
            html: '<div style="text-align:center;color:#fff;background:' +
            color + '">' + cluster.getChildCount() + '</div>'
          });
        }
      }).addTo(map);
    }
    // create a marker cluster group for each type of rail station
    var groups = {
      red: makeGroup('red'),
      green: makeGroup('green'),
      orange: makeGroup('orange'),
      blue: makeGroup('blue'),
      yellow: makeGroup('yellow')
    };
    e.target.eachLayer(function(layer) {
      // add each rail station to its specific group.
      groups[layer.feature.properties.line].addLayer(layer);
    });
});


