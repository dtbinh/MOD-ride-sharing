var data =[
  {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": null,
      "properties": {
        "vendor_id": "CMT",
        "trip_distance": "0.59999999999999998",
        "rate_code": "1",
        "dropoff_longitude": "-73.962042999999994",
        "pickup_latitude": "40.786090999999999",
        "tolls_amount": "0",
        "tip_amount": "0",
        "payment_type": "CSH",
        "fare_amount": "4.5",
        "pickup_longitude": "-73.968862000000001",
        "passenger_count": "4",
        "store_and_fwd_flag": "N",
        "extra": null,
        "dropoff_datetime": "2014-03-29T17:06:32.000",
        "imp_surcharge": "0",
        "total_amount": "5",
        "pickup_datetime": "2014-03-29T17:03:28.000",
        "dropoff_latitude": "40.779451999999999",
        "mta_tax": "0.5"
      }
    }
];

// Create the GeoJSON Layer

//array to store layers for each feature type
var mapLayerGroups = [];

//draw GEOJSON - don't add the GEOJSON layer to the map here
L.geoJson(data, {onEachFeature: onEachFeature})//.addTo(map);

/*
 for all features create a layerGroup for each feature type and add the feature to the layerGroup
*/
function onEachFeature(feature, featureLayer) {

    //does layerGroup already exist? if not create it and add to map
    var lg = mapLayerGroups[feature.properties.type];

    if (lg === undefined) {
        lg = new L.layerGroup();
        //add the layer to the map
        lg.addTo(map);
        //store layer
        mapLayerGroups[feature.properties.type] = lg;
    }

    //add the feature to the layer
    lg.addLayer(featureLayer);      
}

//call Leaflet map.addLayer/removeLayer functions 

//Show layerGroup with feature of "type1"
showLayer("type1");

 // show/hide layerGroup   

function showLayer(id) {
    var lg = mapLayerGroups[id];
    map.addLayer(lg);   
}
function hideLayer(id) {
    var lg = mapLayerGroups[id];
    map.removeLayer(lg);   
}
