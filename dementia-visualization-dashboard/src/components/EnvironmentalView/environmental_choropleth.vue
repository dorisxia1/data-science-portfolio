<template>
  <div :id="id">
    <div class="row g-0">
        <div class="col-md-2"></div>
    <div class="col-md-6">
      <label for="measure-select"></label>
    <select id="measure-select" v-model="internalSelectedMeasure" style="width: 70%;">
      <template v-for="(measures, category) in measures" :key="category">
        <optgroup :label="category">
        <option v-for="measure in measures" :key="measure" :value="measure">
          {{ measure }}
        </option>
        </optgroup>
      </template>
    </select>
      <div class="info-icon-wrapper">
        <i
          class="info-icon"
          @mouseover="showTooltip = true"
          @mouseleave="showTooltip = false"
        >
          ℹ
        </i>
        <div
          v-if="showTooltip"
          :class="`info-tooltip-${id}`"
        >
          <span v-html="measureDescriptions[internalSelectedMeasure] || 'No description available.'" style="text-align: left; display: block;"></span>
        </div>
      </div>
    </div>
    <div class="col-md-3">
      <div ref="legendContainer" class="legend-container"></div>
    </div>
</div>
    <div ref="mapContainer" class="map-container"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { onMounted, ref, watch } from "vue";

export default {
  name: "ChoroplethMap",
  props: {
    id: String,
    measures: Object, // Updated to accept an object with categories as keys
    csvData: Array,
    geoData: Object,
    modelValue: String, // v-model binding for selectedMeasure
    colorScheme: {
      type: String,
      default: "schemeBlues", // Default color scheme
    },
    forceZeroMin: {
      type: Boolean,
      default: false, // Default to false if not provided
    },
  },
  emits: ["update:modelValue"], // Emit updates for v-model
  setup(props, { emit }) {
    const internalSelectedMeasure = ref(props.modelValue || props.measures[0]);
    const showTooltip = ref(false);

    const measureDescriptions = {
        // DEMENTIA DATASET
        "Prevalence rate": "Proportion of medicare beneficiaries that have dementia in year 2020.<br><br>" +
            "<small><strong>Data source:</strong> NORC at the University of Chicago. (2024). Dementia Datahub Public Use File (2020 Data). Retrieved from dementiadatahub.org</small>",
        "Incidence rate": "Proportion of medicare beneficiaries that was newly diagnosed with dementia in year 2020<br><br>" +
            "<small><strong>Data source:</strong> NORC at the University of Chicago. (2024). Dementia Datahub Public Use File (2020 Data). Retrieved from dementiadatahub.org</small>",
        "Mortality rate": "Proportion of prevelant dementia that have died in year 2020<br><br>" +
            "<small><strong>Data source:</strong> NORC at the University of Chicago. (2024). Dementia Datahub Public Use File (2020 Data). Retrieved from dementiadatahub.org</small>",
        // AQI DATASET
        'Median air quality index (AQI) score': 
            "Exposure to a high level of air pollution increases a person's risk of developing dementia.<br>"+
            "Research has been done looking at people's natural exposure to air pollution and their thinking<br>abilities."+
            "Some studies show those exposed to high levels of pollutants perform poorer<br>on thinking tests over time."+
            "<br><br>"+
            "<small><strong>Data source:</strong> United States Environmental Protection Agency. Annual AQI Summary Data by County (2020 Data). Retrieved from epa.gov</small>",
        '% of days with detectable Ozone': 
            "Exposure to a high level of air pollution increases a person's risk of developing dementia.<br>"+
            "Ozone has been identified as a potential exacerbator of neurodegenerative processes."+
            "<br><br>"+
            "<small><strong>Data source:</strong> United States Environmental Protection Agency. Annual AQI Summary Data by County (2020 Data). Retrieved from epa.gov</small>",
        '% of days with detectable PM2.5': 
            "Exposure to a high level of air pollution increases a person's risk of developing dementia.<br>"+
            "The strongest links between pollution and dementia were seen for PM2.5 from agriculture and wildfires."+
            "<br><br>"+
            "<small><strong>Data source:</strong> United States Environmental Protection Agency. Annual AQI Summary Data by County (2020 Data). Retrieved from epa.gov</small>",
        // WEATHER DATASETS
        'Annual mean temperature (°F in 2020)':
            "Dementia can impair the body's ability to regulate temperature, increasing risk of heatstroke and hypothermia.<br>"+
            "<br><br>"+
            "<small><strong>Data source:</strong> National Centers for Environmental Information. (2024). Climate at a Glance (2020 County Data). Retrieved from ncdc.noaa.gov</small>",
        'Historical mean temperature (°F in 1901-2000)': 
            "Dementia can impair the body's ability to regulate temperature, increasing risk of heatstroke and hypothermia.<br>"+
            "<br><br>"+
            "<small><strong>Data source:</strong> National Centers for Environmental Information. (2024). Climate at a Glance (2020 County Data). Retrieved from ncdc.noaa.gov</small>",
        'Annual mean precipitation (inches in 2020)':
            "Rain, snow, or ice may discourage older adults from leaving their homes with potential consequences for social<br>"+
            "isolation, decreased physical activity, and cognitive decline."+
            "<br><br>"+
            "<small><strong>Data source:</strong> National Centers for Environmental Information. (2024). Climate at a Glance (2020 County Data). Retrieved from ncdc.noaa.gov</small>",
        'Historical mean precipitation (inches in 1901-2000)':
            "Rain, snow, or ice may discourage older adults from leaving their homes with potential consequences for social<br>"+
            "isolation, decreased physical activity, and cognitive decline."+
            "<br><br>"+
            "<small><strong>Data source:</strong> National Centers for Environmental Information. (2024). Climate at a Glance (2020 County Data). Retrieved from ncdc.noaa.gov</small>",
        // CDC DATASET
        'Utility insecurity (prevalence %)':
            "Research found that individuals with housing instability have an elevated risk of developing Alzheimer's<br>"+
            "disease or a related dementia compared to those with stable housing."+
            "<br><br>"+
            "<small><strong>Data source:</strong> Center for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from cdc.gov/places</small>",
        'Housing insecurity (prevalence %)':
            "Research found that individuals with housing instability have an elevated risk of developing Alzheimer's<br>"+
            "disease or a related dementia compared to those with stable housing."+
            "<br><br>"+
            "<small><strong>Data source:</strong> Center for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from cdc.gov/places</small>",
        'Food insecurity (prevalence %)': 
            "Studies have shown food insecurity was associated with an increased estimated dementia risk.<br>"+
            "Food insecurity was also associated with lower memory scores and faster memory decline."+
            "<br><br>"+
            "<small><strong>Data source:</strong> Center for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from cdc.gov/places</small>",
        'Limited transportation access (prevalence %)':
            "Limited access to transportation is an infrastructure barrier that limits access to healthcare,<br>"+
            "social engagement, and physical activity, which are all protective factors against dementia."+
            "<br><br>"+
            "<small><strong>Data source:</strong> Center for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from cdc.gov/places</small>",
        'Social support insecurity (prevalence %)': 
            "Social engagement helps with resilience against the effects of Alzheimer's disease in the brain.<br>"+ 
            "It can also help promote healthy behaviours like exercise, and reduced stress and inflammation."+
            "<br><br>"+
            "<small><strong>Data source:</strong> Center for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from cdc.gov/places</small>",
        'Social isolation (prevalence %)': 
            "Social engagement helps with resilience against the effects of Alzheimer's disease in the brain.<br>"+ 
            "It can also help promote healthy behaviours like exercise, and reduced stress and inflammation."+
            "<br><br>"+
            "<small><strong>Data source:</strong> Center for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from cdc.gov/places</small>",
        'Physical inactivity (prevalence %)':
            "Lack of leisure time is often driven by built environment (lack of parks, unsafe streets, etc.).<br>"+ 
            "Research has shown that people who take regular exercise are less likely to develop dementia than those who don't."+
            "<br><br>"+
            "<small><strong>Data source:</strong> Center for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from cdc.gov/places</small>",
        'Sleep deprivation (prevalence %)': 
            "Sleep deprivation oftens reflect environmental stressors such as noise, overcrowding, housing quality, etc.<br>"+
            "Findings have shown that those who slept six hours or less per night in their 50s and 60s were more<br>"+"likely to develop dementia later in life."+
            "<br><br>"+
            "<small><strong>Data source:</strong> Center for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from cdc.gov/places</small>",
        // Add more mappings as needed
    };

    // Watch for changes in the internal selected measure and emit updates
    watch(internalSelectedMeasure, (newValue) => {
      emit("update:modelValue", newValue);
    });

    const mapContainer = ref(null);
    const legendContainer = ref(null);

    // Watch for changes in csvData, geoData, or selectedMeasure
    watch(
      [() => props.csvData, () => props.geoData, internalSelectedMeasure],
      ([csvData, geoData]) => {
        if (csvData && geoData && geoData.features) {
          updateMap();
        }
      },
      { immediate: true }
    );

    function updateMap() {
      const container = mapContainer.value;
      if (!container) {
        console.warn("Map container is not available. Skipping map update.");
        return;
      }

      const { width, height } = container.getBoundingClientRect();

      const svgId = `${props.id}-svg`;
      d3.select(`#${svgId}`).remove();

      const svg = d3
        .select(container)
        .append("svg")
        .attr("id", svgId)
        .attr("viewBox", `0 0 ${width} ${height}`)
        .attr("preserveAspectRatio", "xMidYMid meet");

      const projection = d3.geoAlbersUsa().fitSize([width, height], {
        type: "FeatureCollection",
        features: props.geoData.features,
      });

      const path = d3.geoPath().projection(projection);

      const measureData = {};
      props.csvData.forEach((row) => {
        if (row.Measure === internalSelectedMeasure.value) {
          measureData[row.FIPS_CODE] = {
            value: +row.Value,
            state: row.STATE,
            county: row.COUNTY_NAME,
          };
        }
      });

      const colorDomain = props.forceZeroMin
        ? [0, d3.max(Object.values(measureData).map((d) => d.value))]
        : d3.extent(Object.values(measureData).map((d) => d.value));

      const color = d3
        .scaleQuantize()
        .domain(colorDomain) // Use the conditional domain
        .range(d3[props.colorScheme][9]);

      // Add legend
      const legendContainerEl = legendContainer.value;
      const legendWidth = legendContainerEl.getBoundingClientRect().width; // Dynamically get width
      const legendHeight = 50;

      d3.select(legendContainerEl).selectAll("*").remove(); // Clear previous legend

      const legendSvg = d3
        .select(legendContainerEl)
        .append("svg")
        .attr("width", legendWidth)
        .attr("height", legendHeight);

      const legendScale = d3
        .scaleLinear()
        .domain(color.domain()) // Use the updated color domain
        .range([0, legendWidth - 20]);

      const legendAxis = d3.axisBottom(legendScale).ticks(5);

      const gradientId = `${props.id}-gradient`;

      legendSvg
        .append("defs")
        .append("linearGradient")
        .attr("id", gradientId)
        .selectAll("stop")
        .data(
          color.range().map((d, i, nodes) => ({
            offset: `${(i / (nodes.length - 1)) * 100}%`,
            color: d,
          }))
        )
        .join("stop")
        .attr("offset", (d) => d.offset)
        .attr("stop-color", (d) => d.color);

      legendSvg
        .append("rect")
        .attr("x", 10)
        .attr("y", 10)
        .attr("width", legendWidth - 20)
        .attr("height", 10)
        .style("fill", `url(#${gradientId})`);

      legendSvg
        .append("g")
        .attr("transform", `translate(10, 25)`)
        .call(legendAxis);

      const tooltip = d3
        .select(container)
        .append("div")
        .attr("class", "tooltip")
        .style("position", "absolute")
        .style("background", "white")
        .style("border", "1px solid #ccc")
        .style("padding", "5px")
        .style("border-radius", "4px")
        .style("pointer-events", "none")
        .style("opacity", 0);

      svg
        .append("g")
        .selectAll("path")
        .data(props.geoData.features)
        .join("path")
        .attr("d", path)
        .attr("fill", (d) => {
          const fips = d.id.toString().padStart(5, "0");
          return measureData[fips] ? color(measureData[fips].value) : "#ccc";
        })
        .attr("stroke", "#333")
        .attr("stroke-width", 0.1)
        .on("mouseover", (event, d) => {
          const fips = d.id.toString().padStart(5, "0");
          const data = measureData[fips];
          if (data) {
            tooltip
              .style("opacity", 1)
              .html(
                `<strong>State:</strong> ${data.state}<br>
                 <strong>County:</strong> ${data.county}<br>
                 <strong>${internalSelectedMeasure.value}:</strong> ${data.value.toFixed(1)}`
              );
          }
        })
        .on("mousemove", (event) => {
          const containerRect = container.getBoundingClientRect();
          tooltip
            .style("left", `${event.clientX - containerRect.left + 10}px`)
            .style("top", `${event.clientY - containerRect.top + 10}px`);
        })
        .on("mouseout", () => {
          tooltip.style("opacity", 0);
        });
    }

    function handleResize() {
      updateMap();
    }

    onMounted(() => {
      // Ensure the map container is available before updating the map
      if (mapContainer.value) {
        if (props.csvData && props.geoData && props.geoData.features) {
          updateMap();
        }
        window.addEventListener("resize", handleResize);
      } else {
        console.warn("Map container is not available yet.");
      }
    });

    return {
      internalSelectedMeasure,
      mapContainer,
      legendContainer,
      showTooltip,
      measureDescriptions,
    };
  },
};
</script>

<style scoped>
.map-container {
  margin-top: 1em;
  position: relative;
  width: 100%; /* Ensure it takes the full width of the Bootstrap container */
  height: 0;
  padding-bottom: 50%; /* Maintain aspect ratio (16:9) */
}

.tooltip {
  font-size: 12px;
  line-height: 1.4;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.info-icon-wrapper {
  display: inline-block;
  position: relative;
}

[class^="info-tooltip-"] {
  position: absolute;
  top: 100%; /* Position below the icon */
  left: 50%; /* Center horizontally relative to the icon */
  transform: translateX(-50%);
  background: white;
  border: 1px solid #ccc;
  padding: 5px;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  font-size: 12px;
  line-height: 1.4;
  z-index: 10;
  white-space: nowrap;
}

.info-icon {
  margin-left: 0.5em;
  cursor: pointer;
  font-size: 1.2em;
  color: #0918eb;
}

.legend-container {
  margin-top: 0em;
  margin-bottom: -5em;
  width: 100%;
  height: auto;
}
</style>