<!-- CirclePackingPlot.vue -->
<template>
  <div id="medicare-view-container"  class="container-fluid">
      <div class="row justify-content-center">
          <div class="col-lg-8 col-md-10 col-sm-12">
              <h1>Medicare Insurance Types for Dementia Patients</h1>
              <p>
                Medicare is federal health insurance coverage for people in the United States that are 65 years of age
                or older. Medicare Advantage (MA) and Traditional Medicare (fee-for-service) are common options for dementia
                and Alzheimer's patients. In 2020, Medicare Advantage had an overall enrollment of 42% of Medicare enrollees,
                but this number has grown steadily since. <a href="https://schaeffer.usc.edu/research/does-ma-deliver-better-care-dementia-than-ta/" target="_blank">Studies</a> have compared the two options for their demographic splits and what they
                offer for dementia patients. Understanding the role of insurance in how dementia patients
                receive the care that they need is vital, especially since Medicare options can vary
                <a href="https://www.macpac.gov/subtopic/medicare-advantage-dual-eligible-special-needs-plans-aligned-with-medicaid-managed-long-term-services-and-supports/#:~:text=Dual%20eligible%20special%20needs%20plans%20(D%2DSNPs)%20are%20a,beneficiaries%20enrolled%20(CMS%202022)." target="_blank">across the country</a> and
                enrollment can look <a href="https://www.commonwealthfund.org/publications/issue-briefs/2021/oct/medicare-advantage-vs-traditional-medicare-beneficiaries-differ#5" target="_blank">different by demographic</a>.
                <br />
                <br />
                This visualization offers a side-by-side comparison of looking at Medicare coverage for different aggregates
                of Alzheimer's disease and related dementias patients (ADRD) from 2020-2024. Explore the difference in
                dementia prevalence across insurance types by hovering or clicking on the circles below. You can also look
                at the data from a regional point of view and normalize the data by population.
              </p>
              <br />
              <div class="d-flex justify-content-center">
                  <div class="chart-wrapper">
                      <svg ref="circlePackingContainer"></svg>
                  </div>
              </div>
              <div id="year-slider-container">
                <label for="year">Year: {{ selectedYear }}</label>
                <input
                  type="range"
                  id="year"
                  :min="minYear"
                  :max="maxYear"
                  :value="selectedYear"
                  @input="updateSelectedYear($event.target.value)"
                  class="slider"
                />
              </div>
              <h2>Select your view:</h2>
              <div id="circle-type-selector">
                  <input type="radio" id="insurance" value="insurance" v-model="selectedChart" checked/>
                  <label for="insurance">By Insurance</label>
                  <input type="radio" id="region" value="region" v-model="selectedChart" />
                  <label for="region">By Region</label>
              </div>
              <div id="normalization-selector" v-if="selectedChart === 'region'">
                <input type="checkbox" id="normalize" value="normalize" v-model="normalizeByPopulation" />
                <label for="normalize">Normalize Prevalence by Population</label>
              </div>              
          </div>
      </div>
      <div ref="tooltip" class="tooltip" :style="tooltipStyle" v-html="tooltipContent"></div>
  </div>
</template>

<script>
import * as d3 from 'd3';
const width = 700;
const height = width;

export default {
  name: 'MedicareView',
  data() {
      return {
          selectedChart: 'insurance',
          rawData: null,
          data: null,
          codebook: null,
          regionData: {
              'Alabama': { region: 'South', subregion: 'East South Central' },
              'Alaska': { region: 'West', subregion: 'Pacific' },
              'Arizona': { region: 'West', subregion: 'Mountain' },
              'Arkansas': { region: 'South', subregion: 'West South Central' },
              'California': { region: 'West', subregion: 'Pacific' },
              'Colorado': { region: 'West', subregion: 'Mountain' },
              'Connecticut': { region: 'North East', subregion: 'New England' },
              'Delaware': { region: 'South', subregion: 'South Atlantic' },
              'District of Columbia': { region: 'South', subregion: 'South Atlantic' },
              'Florida': { region: 'South', subregion: 'South Atlantic' },
              'Georgia': { region: 'South', subregion: 'South Atlantic' },
              'Hawaii': { region: 'West', subregion: 'Pacific' },
              'Idaho': { region: 'West', subregion: 'Mountain' },
              'Illinois': { region: 'Midwest', subregion: 'East North Central' },
              'Indiana': { region: 'Midwest', subregion: 'East North Central' },
              'Iowa': { region: 'Midwest', subregion: 'West North Central' },
              'Kansas': { region: 'Midwest', subregion: 'West North Central' },
              'Kentucky': { region: 'South', subregion: 'East South Central' },
              'Louisiana': { region: 'South', subregion: 'West South Central' },
              'Maine': { region: 'North East', subregion: 'New England' },
              'Maryland': { region: 'South', subregion: 'South Atlantic' },
              'Massachusetts': { region: 'North East', subregion: 'New England' },
              'Michigan': { region: 'Midwest', subregion: 'East North Central' },
              'Minnesota': { region: 'Midwest', subregion: 'West North Central' },
              'Mississippi': { region: 'South', subregion: 'East South Central' },
              'Missouri': { region: 'Midwest', subregion: 'West North Central' },
              'Montana': { region: 'West', subregion: 'Mountain' },
              'Nebraska': { region: 'Midwest', subregion: 'West North Central' },
              'Nevada': { region: 'West', subregion: 'Mountain' },
              'New Hampshire': { region: 'North East', subregion: 'New England' },
              'New Jersey': { region: 'North East', subregion: 'Middle Atlantic' },
              'New Mexico': { region: 'West', subregion: 'Mountain' },
              'New York': { region: 'North East', subregion: 'Middle Atlantic' },
              'North Carolina': { region: 'South', subregion: 'South Atlantic' },
              'North Dakota': { region: 'Midwest', subregion: 'West North Central' },
              'Ohio': { region: 'Midwest', subregion: 'East North Central' },
              'Oklahoma': { region: 'South', subregion: 'West South Central' },
              'Oregon': { region: 'West', subregion: 'Pacific' },
              'Pennsylvania': { region: 'North East', subregion: 'Middle Atlantic' },
              'Puerto Rico': { region: 'Other Regions', subregion: 'U.S. Territories' },
              'Rhode Island': { region: 'North East', subregion: 'New England' },
              'South Carolina': { region: 'South', subregion: 'South Atlantic' },
              'South Dakota': { region: 'Midwest', subregion: 'West North Central' },
              'Tennessee': { region: 'South', subregion: 'East South Central' },
              'Texas': { region: 'South', subregion: 'West South Central' },
              'Utah': { region: 'West', subregion: 'Mountain' },
              'Vermont': { region: 'North East', subregion: 'New England' },
              'U.S. Virgin Islands': { region: 'Other Regions', subregion: 'U.S. Territories' },
              'Virginia': { region: 'South', subregion: 'South Atlantic' },
              'Washington': { region: 'West', subregion: 'Pacific' },
              'West Virginia': { region: 'South', subregion: 'South Atlantic' },
              'Wisconsin': { region: 'Midwest', subregion: 'East North Central' },
              'Wyoming': { region: 'West', subregion: 'Mountain' },
              'Africa': { region: 'Other Regions', subregion: 'Rest of the World' },
              'Asia': { region: 'Other Regions', subregion: 'Rest of the World' },
              'Canada and Islands': { region: 'Other Regions', subregion: 'Rest of the World' },
              'Central America and West Indies': { region: 'Other Regions', subregion: 'Rest of the World' },
              'Europe': { region: 'Other Regions', subregion: 'Rest of the World' },
              'Mexico': { region: 'Other Regions', subregion: 'Rest of the World' },
              'Oceania': { region: 'Other Regions', subregion: 'Rest of the World' },
              'Philippines': { region: 'Other Regions', subregion: 'Rest of the World' },
              'South America': { region: 'Other Regions', subregion: 'Rest of the World' },
              'U.S. Possessions': { region: 'Other Regions', subregion: 'U.S. Territories' },
              'American Samoa': { region: 'Other Regions', subregion: 'U.S. Territories' },
              'Guam': { region: 'Other Regions', subregion: 'U.S. Territories' },
              'Commonwealth of the Northern Mariana Islands': { region: 'Other Regions', subregion: 'U.S. Territories' }
          },
          transformedData: null,
          populationData: null,
          normalizeByPopulation: false,
          tooltipStyle: {
              opacity: 0,
              position: 'absolute',
              background: 'white',
              border: '1px solid #ccc',
              padding: '5px',
              pointerEvents: 'none',
          },
          tooltipContent: '',
          minYear: null,
          maxYear: null,
          selectedYear: null,
          focusNode: null,
          currentTransform: null,
          chartInitialized: false // Add this flag
      };
  },
  mounted() {
      this.loadData();
  },
  watch: {
    selectedChart: function() {
      if (this.chartInitialized) { // Check the flag
        this.renderChart(false);
      }
    },
    normalizeByPopulation: function() {
      if (this.chartInitialized) {
        this.renderChart(false);
      }
    },
    data: function() {
       if (this.chartInitialized) {
        this.renderChart(false);
       }
    }
  },
  methods: {
      async loadData() {
          this.rawData = await d3.csv('data/cleaned/circlePackingData_withSyntheticYears.csv');
          this.codebook = await d3.csv('data/cleaned/fips_states_codebook.csv');
          this.populationData = await d3.csv('data/cleaned/population.csv');
          this.setYearRange();
          this.filterDataByYear(this.minYear);
          this.renderChart(false);
          this.chartInitialized = true; // Set the flag after initial render
      },
      setYearRange() {
          if (this.rawData && this.rawData.length > 0) {
              const years = this.rawData.map(d => parseInt(d.YEAR)).filter(year => !isNaN(year));
              this.minYear = d3.min(years);
              this.maxYear = d3.max(years);
              this.selectedYear = this.minYear;
          }
      },
      filterDataByYear(year) {
          this.data = this.rawData.filter(d => parseInt(d.YEAR) === parseInt(year));
          this.transformData();
      },
      updateSelectedYear(year) {
          this.selectedYear = year;
          this.filterDataByYear(year);
          this.renderChart(true);
      },
      transformData() {
          let fipsToState = {};
          this.codebook.forEach(element => {
              const normalizedFIPS = this.padFIPS(element.Code);
              fipsToState[normalizedFIPS] = element.State
          });

          const raceCats = {
              '0.0': 'Unkown',
              '1.0': 'White',
              '2.0': 'African-American',
              '3.0': 'Other',
              '4.0': 'Asian/Pacific Islander',
              '5.0': 'Hispanic',
              '6.0': 'American Indian/Alaskan Native',
              '.': 'All'
          }

          const insuranceLabels = {
              '1.0': 'Fee for Service',
              '2.0': 'Medicare Advantage',
              '.': 'Both'
          }

          this.transformedData = this.data.filter(d => (d['INSURANCE'] != '.') && (d['RACECAT'] != '.')).map(row => {
              const normalizedFIPS = this.padFIPS(`${Math.floor(row['FIPS_STATE'])}`);
              const stateName = fipsToState[normalizedFIPS];
              const regionInfo = this.regionData[stateName];
              const insuranceInfo = insuranceLabels[`${row['INSURANCE']}`];
              const populationEntry = this.populationData.find(p => p.State === stateName);
              let normalizedPrevalence;
              if (populationEntry && populationEntry.Population) {
                  normalizedPrevalence = (parseFloat(+row['prev_cnt']) / parseInt(populationEntry.Population)) * 100;
              } else {
                  normalizedPrevalence = undefined;
              }
              
              return {
                  ...row,
                  stateName,
                  region: regionInfo ? regionInfo.region : 'Unknown',
                  subregion: regionInfo ? regionInfo.subregion : 'Unknown',
                  prevalence: +row['prev_cnt'],
                  mortality: +row['mort_cnt'],
                  insuranceLabel: insuranceInfo ? insuranceInfo : 'Unknown',
                  raceLabel: raceCats[`${row['RACECAT']}`],
                  normalizedPrevalence: normalizedPrevalence
              };
          });
      },
      renderChart(isYearUpdate = false) {
          if (!this.transformedData) return;
          const svg = d3.select(this.$refs.circlePackingContainer);
          svg.selectAll('*').remove();

          if (this.selectedChart === 'insurance') {
              this.createInsuranceChart(this.transformedData, isYearUpdate);
          } else if (this.selectedChart === 'region') {
              this.createRegionChart(this.transformedData, isYearUpdate);
          }
      },
      createInsuranceChart(data, isYearUpdate) {
          console.log('Preparing Insurance Plot');
          const root = d3.hierarchy(
              this.convertRollup(d3.rollup(
                  data,
                  v => [
                      { name: 'Prevalence', value: d3.sum(v, d => d.prevalence) },
                      { name: 'Mortality', value: d3.sum(v, d => d.mortality) }
                  ],
                  d => d.insuranceLabel,
                  d => d.raceLabel
              )),
              d => d.children
          ).sum(d => d.value || 0);

          const pack = d3.pack()
              .size([width, height])
              .padding(3);

          const nodes = pack(root).descendants();

          this.createCircles(nodes, root, 'insurance', isYearUpdate);
          console.log('Insurance plot successfully rendered!');
      },
      createRegionChart(data, isYearUpdate) {
          console.log('Preparing Region Plot');

          let root;

          if (this.normalizeByPopulation) {
              const normalizedData = data.filter(d => d.normalizedPrevalence !== undefined);

              root = d3.hierarchy(
                  this.convertRollup(d3.rollup(
                      normalizedData,
                      v => [
                          { name: 'Prevalence', value: d3.sum(v, d => d.normalizedPrevalence) }
                      ],
                      d => d.region,
                      d => d.subregion,
                      d => d.stateName,
                      d => d.insuranceLabel
                  )),
                  d => d.children
              ).sum(d => d.value || 0);
          } else {
              root = d3.hierarchy(
                  this.convertRollup(d3.rollup(
                      data,
                      v => [
                          { name: 'Prevalence', value: d3.sum(v, d => d.prevalence) },
                          { name: 'Mortality', value: d3.sum(v, d => d.mortality) }
                      ],
                      d => d.region,
                      d => d.subregion,
                      d => d.stateName,
                      d => d.insuranceLabel
                  )),
                  d => d.children
              ).sum(d => d.value || 0);
          }

          const pack = d3.pack()
              .size([width, height])
              .padding(3);

          const nodes = pack(root).descendants();

          this.createCircles(nodes, root, 'region', isYearUpdate);
          console.log('Region Plot successfully rendered!');
      },
      createCircles(nodes, root, chartType, isYearUpdate) {
          console.log('isYearUpdate:', isYearUpdate);
          let colorScale;
          if (chartType === 'insurance') {
              colorScale = d3.scaleSequential(d3.interpolateBlues)
                              .domain([d3.max(nodes, d => d.depth), 0]);
          } else {
              colorScale = d3.scaleSequential(d3.interpolateOrRd)
                              .domain([d3.max(nodes, d => d.depth), 0]);
          }

          const svg = d3.select(this.$refs.circlePackingContainer)
                          .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
                          .attr("width", '100%')
                          .attr("style", `max-width: 100%; height: auto; display: block; margin: 0 -14px; cursor: pointer;`);

          const svgGroup = svg.append("g");

          const circle = svgGroup.selectAll('circle')
                          .data(nodes)
                          .join('circle')
                          .style('fill', d => colorScale(d.depth))
                          .attr("pointer-events", d => !d.children ? "none" : null)
                          .on("mouseover", this.handleMouseOver)
                          .on("mouseout", this.handleMouseOut)
                          .on("click", (event, d) => focus !== d && (zoom(event, d), event.stopPropagation()));

          const labels = svgGroup.selectAll('text')
                          .data(nodes)
                          .join('text')
                          .attr('text-anchor', 'middle')
                          .attr('class', 'responsive-label')
                          .style('font-family', 'Arial, Helvetica, sans-serif')
                          .style("fill-opacity", d => d.parent === root ? 1 : 0)
                          .style("fill", "#292c38")
                          .style("font-weight", "600")
                          .style("display", d => d.parent === root ? "inline" : "none")
                          .text(d => d.data.name);

          svgGroup.on("click", (event) => zoom(event, root));
          let focus = this.focusNode || root;
          let view = this.currentTransform ? [0,0,width] : [focus.x, focus.y, focus.r * 2];

          const self = this;

          function zoomTo(v) {
              if (!Array.isArray(v) || v.length !== 3 || v.some(isNaN)) {
                    console.error('Invalid zoomTo value:', v);
                    return;
              }
              const k = width / v[2];
              view = v;

              labels.attr("transform", d => {
                const x = (d.x - v[0]) * k;
                const y = (d.y - v[1]) * k;
                if (isNaN(x) || isNaN(y)) {
                  console.error('Invalid label transform:', d, v, k);
                  return `translate(0,0)`;
                }
                return `translate(${x},${y})`;
              });
              circle.attr("transform", d => {
                const x = (d.x - v[0]) * k;
                const y = (d.y - v[1]) * k;
                 if (isNaN(x) || isNaN(y)) {
                    console.error('Invalid circle transform:', d, v, k);
                    return `translate(0,0)`;
                 }
                return `translate(${x},${y})`;
              });
              circle.attr("r", d => d.r * k);
              self.currentTransform = [v[0], v[1], k]; // Store for zoom on year change
              // Update label visibility here as well
              labels.style("display", d => {
                  const distance = Math.sqrt(Math.pow(d.x - view[0], 2) + Math.pow(d.y - view[1], 2));
                  return (d.parent === focus || distance < view[2] / 2) ? "inline" : "none";
              });
          }

          function zoom(event, d) {
              focus = d;
              const transition = svgGroup.transition()
                  .duration(event.altKey ? 7500 : 750)
                  .tween("zoom", () => {
                      const i = d3.interpolateZoom(view, [focus.x, focus.y, focus.r * 2]);
                      return t => zoomTo(i(t));
                  });
              labels
                .filter(function(d) { return d.parent === focus || this.style.display === "inline"; })
                .transition(transition)
                    .style("fill-opacity", d => d.parent === focus ? 1 : 0)
                    .on("start", function(d) { if (d.parent === focus) this.style.display = "inline"; })
                    .on("end", function(d) { if (d.parent !== focus) this.style.display = "none"; });

              self.focusNode = focus;
              self.currentTransform = [view[0], view[1], width / view[2]];
              
          }

          if (!isYearUpdate ) {
              zoomTo([focus.x, focus.y, focus.r * 2]);
          } else if (this.currentTransform) {
            zoomTo([this.currentTransform[0], this.currentTransform[1], width / this.currentTransform[2]]);
          }
          else {
             zoomTo([focus.x, focus.y, focus.r * 2]);
          }
          //this.currentTransform = d3.zoomTransform(svgGroup.node());
      },
      padFIPS(fips) {
          if (fips.length === 1) {
              return '0' + fips;
          }
          return fips;
      },
      convertRollup(rollupData) {
          if (rollupData instanceof Map) {
              const result = { children: [] };
              rollupData.forEach((value, key) => {
                  result.children.push({ name: key, ...this.convertRollup(value) });
              });
              return result;
          } else {
              return { children: rollupData };
          }
      },
      handleMouseOver(event, d, chartType) {
          d3.select(event.currentTarget).attr("stroke", "#000");

          if (d.depth === 0) return;

          let prevalence = 0;
          if (!this.normalizeByPopulation || (this.selectedChart === 'insurance')) {
            let mortality = 0;

            if (((d.depth === 4) && (chartType === 'insurance')) || ((d.depth === 5) && (chartType === 'region'))) {
                if (d.data.name === 'Prevalence') {
                    prevalence = d.value;
                } else {
                    mortality = d.value;
                }
            } else {
                d.descendants().forEach(node => {
                    if (node.data && node.data.name === 'Prevalence') {
                        prevalence += node.value;
                    } else if (node.data && node.data.name === 'Mortality') {
                        mortality += node.value;
                    }
                });
            }

            const mortalityRate = prevalence > 0 ? (mortality / prevalence) * 100 : 0;
            this.tooltipContent = `Prevalence: ${prevalence.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",")}<br>Mortality Rate: ${mortalityRate.toFixed(2)}%`;
          } else {
            if (d.depth === 5) {
                prevalence = d.value;
            } else {
                d.descendants().forEach(node => {
                    prevalence += node.value;
                });
            }
            
            this.tooltipContent = `Prevalence: ${prevalence.toFixed(2)}`;
          }

          this.tooltipStyle.opacity = 1;
          this.tooltipStyle.left = `${event.pageX + 10}px`;
          this.tooltipStyle.top = `${event.pageY + 10}px`;
      },
      handleMouseOut(event) {
          d3.select(event.currentTarget).attr("stroke", null);
          this.tooltipStyle.opacity = 0;
      }
  }
};
</script>


<style scoped>
#medicare-view-container {
  width: 100%;
  /* Dynamically calculate margin-left based on viewport width */
  margin-left: calc(var(--main-content-margin-left, 0px)); /* Use a CSS variable */
  /* Center the content within the adjusted container */
  display: flex;
  flex-direction: column; /* Stack items vertically */
  align-items: center; /* Center items horizontally */
}

#circle-type-selector {
  margin-bottom: 20px;
}

#circle-type-selector label {
  font-size: large;
}

/* Add any custom styling for your plot container */
.circle-label {
  font-family: Arial, Helvetica, sans-serif;
}

.tooltip {
  position: absolute;
  background: white;
  border: 1px solid #ccc;
  padding: 5px;
  pointer-events: none;
  opacity: 0;
}

.chart-wrapper {
  width: 100%; /* Make the wrapper take the full width of the column */
  margin: 0 auto;
}

svg {
  width: 100%;
  height: auto;
  display: block;
}

#normalization-selector {
  margin-top: 10px;
  font-size: large;
}

#year-slider-container {
  margin-top: 20px;
  display: flex;
  flex-direction: column; /* Stack label and slider vertically */
  align-items: center; /* Center items horizontally */
  gap: 15px;
}

#year-slider-container label {
  font-size: large;
}

#year-slider-container .slider {
  flex-grow: 0;
  max-width: 300px; /* Or your desired max-width */
  width: 100%; /* Allow it to shrink within its container */
}

svg text {
  /* Default font size (for very small screens or as a fallback) */
  font-size: clamp(12px, 4vw, 16px); /* Example default range */
}

/* Small screens (up to 576px - typical mobile) */
@media (max-width: 576px) {
  svg text {
    font-size: clamp(12px, 4vw, 18px); /* Slightly larger min and preferred for better mobile readability */
  }
}

/* Medium screens (577px to 992px - typical tablets) */
@media (min-width: 577px) and (max-width: 992px) {
  svg text {
    font-size: clamp(12px, 3vw, 24px); /* Good balance for tablets */
  }
}

/* Large screens (993px and above - typical desktops/laptops) */
@media (min-width: 993px) {
  svg text {
    font-size: clamp(14px, 2vw, 32px); /* Larger max to prevent excessive size on big screens */
  }
}
</style>