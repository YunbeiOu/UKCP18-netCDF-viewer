library(leaflet)

library(rgdal)

# From http://data.okfn.org/data/datasets/geo-boundaries-world-110m
countries <- readOGR("https://rstudio.github.io/leaflet/json/countries.geojson")

pal <- colorNumeric(
  palette = "YlGnBu",
  domain = countries$gdp_md_est
)
map %>%
  addPolygons(stroke = FALSE, smoothFactor = 0.2, fillOpacity = 1,
              color = ~pal(gdp_md_est)
  ) %>%
  addLegend("bottomright", pal = pal, values = ~gdp_md_est,
            title = "Est. GDP (2010)",
            labFormat = labelFormat(prefix = "$"),
            opacity = 1
  )

pal <- colorNumeric(
  palette = "Blues",
  domain = "0-100")