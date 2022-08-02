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
  "esri/widgets/TimeSlider",
  "esri/widgets/Home"
], function(Map, TileLayer,FeatureLayer,VectorTileLayer,Point, MapView,Basemap,Search,Expand,Legend,Swipe,TimeSlider,Home) {

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
  
    // https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/wsgmax10m_future_autumn/MapServer

    let url_head = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/';

    let url_end = '/MapServer';

    var lyr_url = 'https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/clt_history_annual/MapServer';

    var legend_dict = {
      'clt': 'Cloud cover (%)',
      'flashrate': 'Lightning (No. of flashes)',
      'hurs': 'Relative humidity (%)',
      'huss': 'Specific humidity (%)',
      'pr': 'Precipitation (mm/day)',
      'prsn': 'Snow: snowfall amount (mm)',
      'psl': 'Sea level pressure (hPa)',
      'rls': 'Radiation, net long wave (Wm-2)',
      'rss': 'Radiation, net short wave (Wm-2)',
      'sfcWind': 'Wind speed (m/s)',
      'snw': 'Snow: lying snow amount (mm)',
      'tas': 'Temperature, Mean (°C)',
      'tasmax': 'Temperature, maximum (°C)',
      'tasmin': 'Temperature, minimum (°C)',
      'uas': 'Wind speed eastwards (m/s)',
      'vas': 'Wind speed northwards (m/s)',
      'wsgmax10m': 'Wind gusts (m/s)'
    };
  
    function show_lyr() {
      var radios = document.getElementsByName('var');
      var var_value;
      for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
          // do whatever you want with the checked radio
          var_value = radios[i].value;
          console.log(var_value)
          
          // only one radio can be logically checked, don't check the rest
          break;
        }
      }

      radios = document.getElementsByName('per');
      var per_value;
      for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
          // do whatever you want with the checked radio
          per_value = radios[i].value;
          
          // only one radio can be logically checked, don't check the rest
          break;
        }
      }

      radios = document.getElementsByName('sea');
      var sea_value;
      for (var i = 0, length = radios.length; i < length; i++) {
        if (radios[i].checked) {
          // do whatever you want with the checked radio
          sea_value = radios[i].value;
          
          // only one radio can be logically checked, don't check the rest
          break;
        }
      }

      layer_name = var_value + '_' + per_value + '_' + sea_value

      lyr_url = (url_head.concat(layer_name)).concat(url_end);
  
      var vtlLayer = new TileLayer({
      url: lyr_url,
      spatialReference: 27700
      });

      map.removeAll();

      map.layers.add(vtlLayer);
      map.layers.add(fealayer);
      map.layers.add(vtlLayer_GB);

      // view.ui.remove(legend);

      view.ui.empty("bottom-right");

      

      view.ui.add(new Legend({
        view: view,
        layerInfos: [
          {
            layer: vtlLayer,
            title: legend_dict[var_value]
          }
        ]
      }), "bottom-right");

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

    let fealayer2 = new FeatureLayer({
      // URL to the vector tile service
      url: "https://services1.arcgis.com/SfF67lOzKAmtSACX/arcgis/rest/services/GBR_adm2/FeatureServer"
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
      center: new Point({x: 350000, y: 500000, spatialReference: 27700}),
      zoom: 4
    });

 
    // // time slider widget initialization
    // const timeSlider = new TimeSlider({
    //   container: "timeSlider",
    //   view: view,
    //   timeVisible: true, // show the time stamps on the timeslider
    //   loop: true
    // });

    const searchWidget = new Search({
    view: view
    });

    // Add the search widget to the top right corner of the view
    view.ui.add(searchWidget, {
      position: "top-right",
      index:2,
    });

    // Add legend
    const activeLayer = map.layers.getItemAt(0);

    const legend = new Legend({
      view: view,
      layerInfos: [
        {
          layer: activeLayer,
          title: "Cloud cover (%)"
        }
      ]
    });

    // Add widget to the bottom right corner of the view
    view.ui.add(legend, "bottom-right");

    // Add home button
    const homeBtn = new Home({
      view: view
    });

    view.ui.add(homeBtn, "top-left");


    // Add button behaviors
    var radios = document.getElementsByName('var');
    for (var i = 0, length = radios.length; i < length; i++) {
      var id_name = 'var_opt'+ (i+1);
      document.getElementById(id_name).addEventListener("click",show_lyr);
    }

    for (var i = 0, length = 3; i<length; i++) {
      var id_name = 'per_opt'+ (i+1);
      console.log(id_name)
      document.getElementById(id_name).addEventListener("click",show_lyr);
    }

    for (var i = 0, length = 5; i<length; i++) {
      var id_name = 'sea_opt'+ (i+1);
      console.log(id_name)
      document.getElementById(id_name).addEventListener("click",show_lyr);
    }


});


