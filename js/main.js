require([
  "esri/Map",
  "esri/layers/TileLayer",
  "esri/layers/FeatureLayer",
  "esri/layers/VectorTileLayer",
  "esri/geometry/Point",
  "esri/views/MapView",
   "esri/Basemap",
  "esri/widgets/Search",
  "esri/widgets/Expand",
  "esri/widgets/Legend",
  "esri/widgets/Swipe",
  "esri/widgets/TimeSlider"
], function(Map, TileLayer,FeatureLayer,VectorTileLayer,Point, MapView,Basemap,Search,Expand,Legend,Swipe,TimeSlider) {

   const labelClass = {
          // autocasts as new LabelClass()
          symbol: {
            type: "text", // autocasts as new TextSymbol()
            color: "white",
            font: {
              // autocast as new Font()
              family: "Playfair Display",
              size: 10,
              weight: "bold"
            }
          },
          labelPlacement: "above-center",
          labelExpressionInfo: {
            expression: "$feature.NAME_1"
          }
        };
  
    let url_head = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/';

    let url_end = '_1980_spring/MapServer';

    var lyr_url = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/clt_history_summer/MapServer';
  
    function show_lyr() {
      var radios = document.getElementsByName('var');
      var value;
      for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
          // do whatever you want with the checked radio
          value = radios[i].value;
          console.log(value)
          
          // only one radio can be logically checked, don't check the rest
          break;
        }
      }

      lyr_url = (url_head.concat(value)).concat(url_end);
      console.log(lyr_url);
  
      var vtlLayer = new TileLayer({
      url: lyr_url,
      spatialReference: 27700
      });

      map.layers.add(vtlLayer);
  
    }


 
  
    var vtlLayer = new TileLayer({
    url: "https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/clt_history_annual/MapServer",
    spatialReference: 27700
    });
  
    var vtlLayer2 = new TileLayer({
    url: "https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/pr_1980_spring/MapServer",
    spatialReference: 27700
    });
  
    // Create featurelayer from feature service
    const fealayer = new FeatureLayer({
      // URL to the service
      url: "https://services1.arcgis.com/SfF67lOzKAmtSACX/arcgis/rest/services/GBR_adm1/FeatureServer"
      // labelingInfo: [labelClass],
    });

    let vtlLayer_GB = new VectorTileLayer({
      // URL to the vector tile service
      url: "https://uomanchester.maps.arcgis.com/sharing/rest/content/items/796bcd7e487b416ba3420d1ffc8649d7/resources/styles/root.json"
    });
  
    let map = new Map({
      basemap: {
        portalItem: {
          // id: "0bd3a4a6fd674a90a7d0a9e5f36fb59b" // OS Open Carto
          id: "a118075240bc4e4f8062265ecdad0e7e" // Open Grey
        }
      },
      
      layers: [vtlLayer,fealayer,vtlLayer_GB]
    });

    let view = new MapView({
      spatialReference: 27700, 
      container: "viewDiv",
      map: map,
      center: new Point({x: 500000, y: 500000, spatialReference: 27700}),
      zoom: 4
    });

  
    const legend = new Legend({
    view: view,
      layerInfos: [
        {
          layer: vtlLayer2,
          title: "Precipitation(%)"
        }
      ]
    });

    const legendExpand = new Expand({
      expandIconClass: "esri-icon-legend",
      expandTooltip: "Legend",
      view: view,
      content: legend,
      expanded: false
    });

    view.ui.add(legendExpand, "top-left");



            
        // time slider widget initialization
        const timeSlider = new TimeSlider({
          container: "timeSlider",
          view: view,
          timeVisible: true, // show the time stamps on the timeslider
          loop: true
        });
  
  // document.getElementById('var').addEventListener("click",show_lyr);  
  
//  var checkedValue = document.querySelector('.selectopt:checked').value;
// console.log(checkedValue);

          const searchWidget = new Search({
          view: view
        });

        // Add the search widget to the top right corner of the view
        view.ui.add(searchWidget, {
          position: "top-right",
          index:2,
        });

document.getElementById('opt2').addEventListener("click",show_lyr);  
document.getElementById('opt1').addEventListener("click",show_lyr); 

});


