require([
    "esri/Map",
    "esri/layers/TileLayer",
    "esri/layers/FeatureLayer",
    "esri/layers/VectorTileLayer",
    "esri/geometry/Point",
    "esri/WebMap",
    "esri/views/MapView",
    "esri/widgets/Swipe",
    "esri/widgets/Legend"
  ], (Map, TileLayer,FeatureLayer,VectorTileLayer,WebMap, Point,MapView, Swipe, Legend) => {
    let swipes;

    const scroller = document.querySelector(".scroller");
    const content = scroller.querySelector(".content");

    // initiate layers
    var vtlLayer = new TileLayer({
    url: "https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/clt_history_annual/MapServer",
    spatialReference: 27700
    });
    
    var vtlLayer2 = new TileLayer({
    url: "https://tiles.arcgis.com/tiles/SfF67lOzKAmtSACX/arcgis/rest/services/pr_1980_spring/MapServer",
    spatialReference: 27700
    });
    
    // Create featurelayer from feature service
    const boundary_lyr = new FeatureLayer({
        // URL to the service
        url: "https://services1.arcgis.com/SfF67lOzKAmtSACX/arcgis/rest/services/GBR_adm1/FeatureServer"
        // labelingInfo: [labelClass],
    });

    var fealayer = new FeatureLayer({
        // URL to the vector tile service
        url: "https://services1.arcgis.com/SfF67lOzKAmtSACX/arcgis/rest/services/socio_eco_uk/FeatureServer"
    });

    var fealayer3 = new FeatureLayer({
        // URL to the vector tile service
        url: "https://services1.arcgis.com/SfF67lOzKAmtSACX/arcgis/rest/services/all_residents/FeatureServer"
    });

    var vtlLayer_GB = new VectorTileLayer({
        // URL to the vector tile service
        url: "https://uomanchester.maps.arcgis.com/sharing/rest/content/items/796bcd7e487b416ba3420d1ffc8649d7/resources/styles/root.json"
    });

    // initialize the map
    var map = new Map({
        basemap: {
          portalItem: {
            id: "a118075240bc4e4f8062265ecdad0e7e" // Open Grey
          }
        },
        layers: [vtlLayer,boundary_lyr,fealayer,vtlLayer_GB]
      });
  
      var view = new MapView({
        spatialReference: 27700, 
        container: "viewDiv",
        map: map,
        center: new Point({x: 350000, y: 500000, spatialReference: 27700}),
        zoom: 4
      });
  

    // map
    //   .load()
    //   .then(() => {
    //     // create the view
    //     view = new MapView({
    //         spatialReference: 27700, 
    //         container: "viewDiv",
    //         map: map,
    //         center: new Point({x: 350000, y: 500000, spatialReference: 27700}),
    //         zoom: 4
    //     });

    //     // get the layers from the webmap
    //     const layers = map.layers;

    //     // create a swipe widget for each layer
    //     swipes = layers.map((layer) => {
    //       return new Swipe({
    //         view: view,
    //         disabled: true,
    //         position: 100,
    //         direction: "vertical",
    //         trailingLayers: [layer],
    //         visibleElements: {
    //           handle: false,
    //           divider: true
    //         }
    //       });
    //     });

    //     // create a legend for each layer and add it to the map
    //     layers.forEach((layer) => {
    //       const slide = document.createElement("div");
    //       slide.className = "slide";
    //       const legendDiv = document.createElement("div");
    //       legendDiv.className = "legend";
    //       const legend = new Legend({
    //         container: legendDiv,
    //         view: view,
    //         style: "card",
    //         layerInfos: [
    //           {
    //             layer: layer
    //           }
    //         ]
    //       });
    //       slide.appendChild(legendDiv);
    //       content.appendChild(slide);
    //     });

    //     return view.when();
    //   })
    //   .then(() => {
    //     let height = 0;

    //     function updateSize() {
    //       height = view.height * swipes.length;
    //       setScroll(scroller.scrollTop);
    //       content.style.height = height + "px";
    //     }

    //     function clamp(value, min, max) {
    //       return Math.min(max, Math.max(min, value));
    //     }

    //     let scroll = 0;
    //     let ticking = false;
    //     function setScroll(value) {
    //       scroll = value;

    //       if (!ticking) {
    //         requestAnimationFrame(() => {
    //           ticking = false;

    //           let pageRatio = scroll / view.height;

    //           swipes.forEach((swipe, index, swipes) => {
    //             // add each swipe to the view UI
    //             view.ui.add(swipe);

    //             let position = (index - pageRatio) * 100;

    //             // To achieve this infinite scroll effect we need to swap the layers:
    //             //   The layer starts at the bottom, the divider goes up
    //             //   Then the next layer starts to show up, so we put back the divider at the bottom and swap the layers.
    //             if (position < 0 && swipe.trailingLayers.length) {
    //               swipe.leadingLayers.addMany(swipe.trailingLayers);
    //               swipe.trailingLayers.removeAll();
    //             } else if (position >= 0 && swipe.leadingLayers.length) {
    //               swipe.trailingLayers.addMany(swipe.leadingLayers);
    //               swipe.leadingLayers.removeAll();
    //             }

    //             if (position < 0) {
    //               position += 100;
    //             }

    //             swipe.position = clamp(position, 0, 100);
    //           });
    //         });

    //         ticking = true;
    //       }
    //     }

    //     view.watch("height", updateSize);
    //     updateSize();

    //     // show layer legends after map has loaded
    //     const legendDivs = document.getElementsByClassName("legend");
    //     for (let i = 0; i < legendDivs.length; i++) {
    //       legendDivs[i].style.visibility = "visible";
    //     }

    //     // stop default scroll
    //     scroller.addEventListener("wheel", (event) => {
    //       event.stopImmediatePropagation();
    //     });

    //     scroller.addEventListener("scroll", (event) => {
    //       setScroll(scroller.scrollTop);
    //     });
    //   })
    //   .catch((error) => {
    //     console.error(error);
    //   });

  });