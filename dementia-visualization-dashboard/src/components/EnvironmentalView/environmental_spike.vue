<template>
  <div class="row g-0">
    <div class="col-md-9">
      <div ref="mapContainer" class="spike-map-container"></div>
    </div>
    <div class="col-md-3 d-flex flex-column justify-content-center align-items-center">
      <div class="text-container mb-3">
        <p>
          <small>
            The spike map can be used to identify regional disparities and reveal where environmental factors may have more impactful risk to dementia population.
            Taller and darker spikes highlight areas with higher values of both measures, revealing areas of concern where there are higher dementia {{ measureA.replace(" rate", "").toLowerCase() }} in an area with higher environmental risk.
          </small>
        </p>
      </div>
      <div class="spike-legend">
        <svg ref="legendSvg"></svg>
      </div>
    </div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { onMounted, ref, watch, onUnmounted } from "vue";

export default {
  name: "EnvironmentalSpike",
  props: {
    csvData: Array,
    geoData: Object,
    measureA: String,
    measureB: String,
  },
  setup(props) {
    const mapContainer = ref(null);

    // Watch for changes in csvData, geoData, or selected measures
    watch(
      [() => props.csvData, () => props.geoData, () => props.measureA, () => props.measureB],
      ([csvData, geoData, measureA, measureB]) => {
        if (csvData && geoData && geoData.features && measureA && measureB) {
          updateSpikeMap();
        }
      },
      { immediate: true }
    );

    function updateSpikeMap() {
      if (!props.csvData || !props.geoData || !props.geoData.features || !mapContainer.value) {
        console.warn("Missing data or map container, spike map will not render yet.");
        return;
      }

      const container = mapContainer.value;
      const { width, height } = container.getBoundingClientRect();

      const svgId = "spike-map-svg";
      d3.select(`#${svgId}`).remove(); // Remove previous map if it exists

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

      // Prepare data for quantile calculation
      const measureDataA = {};
      const measureDataB = {};
      const stateLookup = {};
      props.csvData.forEach((row) => {
        if (row.Measure === props.measureA) {
          measureDataA[row.FIPS_CODE] = +row.Value;
        }
        if (row.Measure === props.measureB) {
          measureDataB[row.FIPS_CODE] = +row.Value;
        }
        stateLookup[row.FIPS_CODE] = row.STATE; // Map FIPS_CODE to STATE
      });

      const valuesA = Object.values(measureDataA).filter((v) => v !== undefined);
      const valuesB = Object.values(measureDataB).filter((v) => v !== undefined);

      const quantileScaleA = d3.scaleQuantile().domain(valuesA).range(d3.range(1, 4));
      const quantileScaleB = d3.scaleQuantile().domain(valuesB).range(d3.range(1, 4));

      const spikeData = props.geoData.features
        .map((feature) => {
          const fips = feature.id.toString().padStart(5, "0");
          const valueA = measureDataA[fips];
          const valueB = measureDataB[fips];
          const state = stateLookup[fips]; // Fetch state from the lookup
          const county = feature.properties.name; // Use properties.name for county
          if (valueA !== undefined && valueB !== undefined) {
            const quantileA = quantileScaleA(valueA);
            const quantileB = quantileScaleB(valueB);
            const combinedQuantile = (quantileA + quantileB) / 2;
            return {
              fips,
              state,
              county,
              valueA,
              valueB,
              coordinates: d3.geoCentroid(feature),
              combinedQuantile,
            };
          }
          return null;
        })
        .filter((d) => d !== null);

      const heightScale = d3.scaleLinear().domain([1, 5]).range([0, 50]);

      const colorScale = d3.scaleThreshold()
        .domain([1.0, 1.5, 2.0, 2.5, 3.0])
        .range(["#efad94", "#e77961", "#de442e", "#c71515", "#5b231e"]);

      const spike = (length, width = 7) => `M${-width / 2},0L0,${-length}L${width / 2},0`;

      svg
        .append("g")
        .selectAll("path")
        .data(props.geoData.features)
        .join("path")
        .attr("d", path)
        .attr("fill", "#ccc")
        .attr("stroke", "#333")
        .attr("stroke-width", 0.1);

      svg
        .append("g")
        .selectAll("path")
        .data(spikeData)
        .join("path")
        .attr("transform", (d) => `translate(${projection(d.coordinates)})`)
        .attr("d", (d) => spike(heightScale(d.combinedQuantile)))
        .attr("fill", (d) => colorScale(d.combinedQuantile))
        .attr("fill-opacity", 0.3)
        .attr("stroke", (d) => colorScale(d.combinedQuantile))
        .attr("stroke-width", 0.5)
        .append("title")
        .text(
          (d) =>
            `State: ${d.state}\nCounty: ${d.county}\n${props.measureA}: ${d.valueA.toFixed(1)}%\n${props.measureB}: ${d.valueB.toFixed(1)}`
        );

      // Add legend
      const legendSvg = d3.select(mapContainer.value.parentNode.parentNode).select(".spike-legend svg");
      legendSvg.selectAll("*").remove(); // Clear previous legend

      const legendWidth = 300;
      const legendHeight = 150; // Adjust height for better visibility
      legendSvg
        .attr("width", legendWidth)
        .attr("height", legendHeight);

      const legendData = [
        { label: `Low Dementia ${props.measureA.replace(" rate", "")} + Low Environmental Risk`, quantile: 1 },
        { label: "", quantile: 2 },
        { label: `High Dementia ${props.measureA.replace(" rate", "")} + High Environmental Risk`, quantile: 3 },
      ];

      const legendGroup = legendSvg
        .append("g")
        .attr("transform", `translate(10, 10)`);

      legendGroup
        .selectAll("path")
        .data(legendData)
        .join("path")
        .attr("d", (d) => spike(heightScale(d.quantile)))
        .attr("fill", (d) => colorScale(d.quantile))
        .attr("stroke", (d) => colorScale(d.quantile))
        .attr("stroke-width", 0.5)
        .attr("transform", (d, i) => `translate(-5, ${i * 45})`); // Adjust spacing

      legendGroup
        .selectAll("text")
        .data(legendData)
        .join("text")
        .attr("x", 5)
        .attr("y", (d, i) => i * 40 + 5) // Match spacing
        .attr("text-anchor", "start")
        .attr("font-size", "10px")
        .text((d) => d.label);
    }

    function handleResize() {
      updateSpikeMap();
    }

    onMounted(() => {
      if (mapContainer.value) {
        updateSpikeMap();
        window.addEventListener("resize", handleResize);
      } else {
        console.warn("Map container is not available yet.");
      }
    });

    onUnmounted(() => {
      window.removeEventListener("resize", handleResize);
    });

    return {
      mapContainer,
    };
  },
};
</script>

<style scoped>
.spike-map-container {
  margin-top: 1em;
  position: relative;
  width: 100%;
  height: 0;
  padding-bottom: 50%; /* Maintain aspect ratio (16:9) */
}

.col-md-3 {
  display: flex;
  flex-direction: column;
  justify-content: center; /* Center content vertically */
  align-items: center;
}

.spike-legend {
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.text-container {
  text-align: left; /* Change to left-justified */
  width: 100%; /* Ensure it spans the full width */
}
</style>