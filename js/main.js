require([
  "esri/Map",
  "esri/layers/TileLayer",
  "esri/geometry/Point",
  "esri/views/MapView"
], function(Map, TileLayer,Point, MapView) {

var vtlLayer = new TileLayer({
url: 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/tas_1980_spring/MapServer',
spatialReference: 27700
});

let map = new Map({
  basemap: {
    portalItem: {
      id: "0bd3a4a6fd674a90a7d0a9e5f36fb59b" // OS Open Carto
    }
  },
  
  layers: [vtlLayer]
});

let view = new MapView({
  spatialReference: 27700, 
  container: "viewDiv",
  map: map,
  center: new Point({x: 500000, y: 500000, spatialReference: 27700}),
  zoom: 6
});
});