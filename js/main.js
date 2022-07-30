require([
  "esri/Map",
  "esri/layers/TileLayer",
  "esri/geometry/Point",
  "esri/views/MapView",
   "esri/Basemap",
], function(Map, TileLayer,Point, MapView,Basemap) {

let url_head = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/';

let url_end = '_1980_spring/MapServer';

var lyr_url = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/tas_1980_spring/MapServer';
  
function show_lyr() {
  var select = document.getElementById('var');
  var value = select.options[select.selectedIndex].value;
  console.log(value); // en
  lyr_url = (url_head.concat(value)).concat(url_end);
console.log(lyr_url);
  
  var vtlLayer = new TileLayer({
url: lyr_url,
spatialReference: 27700
});

  map.layers.add(vtlLayer);
  
}

document.getElementById('var').addEventListener("click",show_lyr);  
 
  
var vtlLayer = new TileLayer({
url: lyr_url,
spatialReference: 27700
});
  
let map = new Map({
  basemap: {
    portalItem: {
      // id: "0bd3a4a6fd674a90a7d0a9e5f36fb59b" // OS Open Carto
      id: "a118075240bc4e4f8062265ecdad0e7e" // Open Grey
    }
  },
  
  layers: [vtlLayer]
});

let view = new MapView({
  spatialReference: 27700, 
  container: "viewDiv",
  map: map,
  center: new Point({x: 500000, y: 500000, spatialReference: 27700}),
  zoom: 4
});

});


