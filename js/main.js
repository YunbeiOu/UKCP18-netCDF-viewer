// require(["esri/config","esri/Map", "esri/views/MapView"], function (esriConfig,Map, MapView) {

//     esriConfig.apiKey = "AAPK1ecd870c1d4e4bcfac2352462e92a51e8eqBgiOJkh37AbrcXWy2rMnSSxumpX-fgm_CxI3gGYZ0j_iKq4EnGmIoK-P-Vs1O";

//     const map = new Map({
//       basemap: "arcgis-light-gray" // Basemap layer service
//     });

//     const view = new MapView({
//       map: map,
//       center: [-2.244644,53.483959], // Longitude, latitude
//       zoom: 5, // Zoom level
//       container: "viewDiv" // Div element
//     });

//   });

require([
    "esri/config",
    "esri/Map",

    "esri/layers/TileLayer",

    "esri/views/MapView"

  ], function (esriConfig,Map, TileLayer, MapView) {

    esriConfig.apiKey = "AAPK1ecd870c1d4e4bcfac2352462e92a51e8eqBgiOJkh37AbrcXWy2rMnSSxumpX-fgm_CxI3gGYZ0j_iKq4EnGmIoK-P-Vs1O";

    const map = new Map({

      basemap: "arcgis-light-gray",

    });

    const view = new MapView({
      container: "viewDiv",
      center: [-2.244644,53.483959],
      zoom: 5,
      container: "viewDiv" 
    });

    // Add layer to map
    const layer = new TileLayer({
        url: "https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/clt_1980/MapServer"
      });

  });