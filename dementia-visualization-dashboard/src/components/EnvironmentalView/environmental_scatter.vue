<template>
    <div class="row g-0">
        <div class="text-container mb-3"></div>
        <div id="scatter-container" class="col-md-8">
            <svg ref="scatterSvg"></svg>
        </div>
        <div class="col-md-4 d-flex flex-column justify-content-center align-items-center">
            <div class="text-container mt-3">
                <p style="text-align: left;">
                    <small>
                        This scatterplot better demonstrates the range of the selected measures and the magnitude of their relationship. 
                        It can be utilized to focus on a specific state and pinpoint counties that are outliers with increased environmental risk affecting the dementia population.
                    </small>
                </p>
            </div>
            <label for="selectedState"><small>Filter to specific state:</small></label>
            <select v-model="selectedState" @change="drawScatter">
                <option value="(All States)">(All States)</option>
                <option v-for="state in uniqueStates" :key="state" :value="state">{{ state }}</option>
            </select>
            <div class="scatter-legend">
                <svg ref="legendSvg"></svg>
            </div>
        </div>
    </div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "EnvironmentalScatter",
  props: {
    csvData: Array,
    measureA: String,
    measureB: String,
  },
  data() {
    return {
      margin: { top: 20, right: 30, bottom: 70, left: 70 },
      selectedState: "(All States)",
    };
  },
  computed: {
    uniqueStates() {
      return Array.from(new Set(this.csvData.map((d) => d.STATE))).sort();
    },
  },
  watch: {
    csvData: "drawScatter",
    measureA: "drawScatter",
    measureB: "drawScatter",
  },
  mounted() {
    window.addEventListener("resize", this.drawScatter);
    this.drawScatter();
  },
  beforeUnmount() {
    window.removeEventListener("resize", this.drawScatter);
  },
  methods: {
    drawScatter() {
      const container = this.$refs.scatterSvg.parentElement;
      const width = container.offsetWidth;
      const height = (width * 3) / 4; // Maintain a 4:3 aspect ratio

      const svg = d3.select(this.$refs.scatterSvg);
      svg.selectAll("*").remove();
      svg.attr("width", width).attr("height", height);

      const { margin } = this;
      const plotWidth = width - margin.left - margin.right;
      const plotHeight = height - margin.top - margin.bottom;

      const data = this.csvData.filter(
        (d) =>
          (d.Measure === this.measureA || d.Measure === this.measureB) &&
          (this.selectedState === "(All States)" || d.STATE === this.selectedState)
      );

      const groupedData = d3.group(data, (d) => `${d.COUNTY_NAME}-${d.STATE}`);
      const scatterData = Array.from(groupedData, ([key, values]) => ({
        COUNTY_STATE: key,
        COUNTY_NAME: values[0].COUNTY_NAME,
        STATE: values[0].STATE,
        valueA: +values.find((d) => d.Measure === this.measureA)?.Value || 0,
        valueB: +values.find((d) => d.Measure === this.measureB)?.Value || 0,
      })).filter((d) => d.valueA > 0 && d.valueB > 0); // Exclude missing values

      const x = d3
        .scaleLinear()
        .domain(d3.extent(scatterData, (d) => d.valueA))
        .range([0, plotWidth]);

      const y = d3
        .scaleLinear()
        .domain(d3.extent(scatterData, (d) => d.valueB))
        .range([plotHeight, 0]);

      const valuesA = scatterData.map((d) => d.valueA);
      const valuesB = scatterData.map((d) => d.valueB);

      const quantileScaleA = d3.scaleQuantile().domain(valuesA).range(d3.range(1, 4));
      const quantileScaleB = d3.scaleQuantile().domain(valuesB).range(d3.range(1, 4));

      const colorScale = d3
        .scaleThreshold()
        .domain([1.0, 1.5, 2.0, 2.5, 3.0])
        .range(["#efad94", "#e77961", "#de442e", "#c71515", "#5b231e"]);

      const g = svg
        .append("g")
        .attr("transform", `translate(${margin.left},${margin.top})`);

      g.append("g")
        .attr("transform", `translate(0,${plotHeight})`)
        .call(d3.axisBottom(x))
        .append("text")
        .attr("x", plotWidth / 2)
        .attr("y", 40)
        .attr("fill", "black")
        .attr("text-anchor", "middle")
        .text("Dementia " + this.measureA + " (%)");

      g.append("g")
        .call(d3.axisLeft(y))
        .append("text")
        .attr("transform", "rotate(-90)")
        .attr("x", -plotHeight / 2)
        .attr("y", -50)
        .attr("fill", "black")
        .attr("text-anchor", "middle")
        .text(this.measureB);

      const tooltip = d3
        .select("#scatter-container")
        .append("div")
        .style("position", "absolute")
        .style("visibility", "hidden")
        .style("background", "#fff")
        .style("border", "1px solid #ccc")
        .style("padding", "5px")
        .style("border-radius", "5px")
        .style("pointer-events", "none")
        .attr("id", "scatter-tooltip");

      const scatter = g.append("g");

      scatter
        .selectAll("circle")
        .data(scatterData)
        .enter()
        .append("circle")
        .attr("cx", (d) => x(d.valueA) + (Math.random() - 0.5) * 10) // Add jitter to x
        .attr("cy", (d) => y(d.valueB) + (Math.random() - 0.5) * 10) // Add jitter to y
        .attr("r", 5)
        .style("fill", (d) => {
          const quantileA = quantileScaleA(d.valueA);
          const quantileB = quantileScaleB(d.valueB);
          const combinedQuantile = (quantileA + quantileB) / 2;
          return colorScale(combinedQuantile);
        })
        .style("opacity", 0.5)
        .on("mouseover", (event, d) => {
          tooltip
            .style("visibility", "visible")
            .html(
              `<strong>State:</strong> ${d.STATE}<br><strong>County:</strong> ${d.COUNTY_NAME}<br><strong>Dementia ${this.measureA} (%):</strong> ${d.valueA.toFixed(1)}<br><strong>${this.measureB}:</strong> ${d.valueB.toFixed(1)}`
            );
        })
        .on("mousemove", (event) => {
          tooltip
            .style("top", `${event.pageY + 10}px`)
            .style("left", `${event.pageX + 10}px`); // Adjusted to position tooltip to the right of the pointer
        })
        .on("mouseout", () => {
          tooltip.style("visibility", "hidden");
        });

      // Add legend
      const legendSvg = d3.select(this.$refs.legendSvg);
      legendSvg.selectAll("*").remove(); // Clear previous legend

      const legendWidth = 300;
      const legendHeight = 100;
      legendSvg.attr("width", legendWidth).attr("height", legendHeight);

      const legendData = [
        { label: `Low Dementia ${this.measureA.replace(" rate", "")} + Low Environmental Risk`, quantile: 1 },
        { label: "", quantile: 2 },
        { label: `High Dementia ${this.measureA.replace(" rate", "")} + High Environmental Risk`, quantile: 3 },
      ];

      const legendGroup = legendSvg.append("g").attr("transform", `translate(10, 10)`);

      legendGroup
        .selectAll("circle")
        .data(legendData)
        .join("circle")
        .attr("cx", 10)
        .attr("cy", (d, i) => i * 30 + 10) // Adjust vertical spacing
        .attr("r", 7)
        .attr("fill", (d) => colorScale(d.quantile))
        .attr("stroke", (d) => colorScale(d.quantile))
        .attr("stroke-width", 0.5);

      legendGroup
        .selectAll("text")
        .data(legendData)
        .join("text")
        .attr("x", 25)
        .attr("y", (d, i) => i * 30 + 15) // Match vertical spacing
        .attr("text-anchor", "start")
        .attr("font-size", "10px")
        .text((d) => d.label);
    },
  },
};
</script>

<style scoped>
#scatter-tooltip {
  font-size: 12px;
  pointer-events: none;
}

.scatter-legend {
  margin-top: 1em;
  text-align: center;
}
</style>
