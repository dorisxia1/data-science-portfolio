<template>
  <h1 style="margin-bottom: 0.2rem;">Environmental Risks on Dementia Across America</h1>
  <h3 style="margin-top: 0;">How where we live can impact how we age</h3>
  <div class="text-container mb-3">
    <p style="padding-left: 7rem; padding-right: 7rem; text-align: left;">
      The natural and built environments have a significant impact on health and well-being and may also affect cognitive functioning. 
      This page aims to inform about environmental contributors to dementia and explore the relationship between dementia outcomes and environmental risk factors across U.S. counties. 
      Use the dropdowns to explore different measures of dementia (prevalence, incidence, mortality) and environmental exposures, including both physical factors (e.g., air pollution, extreme heat) and social factors (e.g., social isolation, food insecurity).
    </p>
  </div>
    <div class="row g-0">
      <div class="col-md-6">
        <h5>Select a dementia-related outcome:</h5>
        <ChoroplethMap
          v-if="csvData && geoData"
          id="map1"
          :measures="measures1"
          :csvData="csvData"
          :geoData="geoData"
          v-model="selectedMeasure1"
          colorScheme="schemeBuPu"
          :forceZeroMin="true"
        />
      </div>
      <div class="col-md-6">
        <h5>Select an environmental-risk factor:</h5>
        <ChoroplethMap
          v-if="csvData && geoData"
          id="map2"
          :measures="measures2"
          :csvData="csvData"
          :geoData="geoData"
          v-model="selectedMeasure2"
          colorScheme="schemeBuPu"
          :forceZeroMin="false"
        />
      </div>
    </div>
    <div class="text-container mb-3" style="padding-top: 2rem;">
    <p style="padding-left: 7rem; padding-right: 7rem; text-align: left;">
      Below are bivariate visualizations that illustrate the relationship between the <strong>{{ selectedMeasure1 }} of dementia</strong> and the environmental risk factor, <strong>{{ selectedMeasure2 }}</strong>.<br>
      <small style="font-size: 0.7em; font-style: italic; ">
              Use the two dropdowns above the choropleth maps to change the measures of interest.
            </small>
    </p>
  </div>
    <div class="row g-0">
      <div class="col-md-12">
        <EnvironmentalSpike
          v-if="csvData && geoData"
          :csvData="csvData"
          :geoData="geoData"
          :measureA="selectedMeasure1"
          :measureB="selectedMeasure2"
        />
      </div>
    </div>
    <div class="row g-0">
      <div class="col-md-1"></div>
      <div class="col-md-10">
        <EnvironmentalScatter
          v-if="csvData && selectedMeasure1 && selectedMeasure2"
          :csvData="csvData"
          :measureA="selectedMeasure1"
          :measureB="selectedMeasure2"
        />
      </div>
    </div>
  
</template>

<script>
import * as d3 from "d3";
import * as topojson from "topojson-client";
import ChoroplethMap from "@/components/EnvironmentalView/environmental_choropleth.vue";
import EnvironmentalSpike from "@/components/EnvironmentalView/environmental_spike.vue";
import EnvironmentalScatter from "@/components/EnvironmentalView/environmental_scatter.vue";

export default {
  name: "EnvironmentalView",
  components: {
    ChoroplethMap,
    EnvironmentalSpike,
    EnvironmentalScatter,
  },
  data() {
    return {
      measures1: { "Dementia Outcomes": ["Prevalence rate", "Incidence rate", "Mortality rate"] }, // Grouped under a single category
      measures2: [],
      csvData: null,
      geoData: null,
      selectedMeasure1: null,
      selectedMeasure2: null,
    };
  },
  async mounted() {
    try {
      const [csvData, geoData] = await Promise.all([
        d3.csv("data/cleaned/EnvironmentalViewData.csv"),
        d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/counties-10m.json"),
      ]);

      this.csvData = csvData;
      this.geoData = topojson.feature(geoData, geoData.objects.counties);

      const groupedMeasures = csvData
        .filter((row) => row.Category !== "Dementia")
        .reduce((acc, row) => {
          if (!acc[row.Category]) {
            acc[row.Category] = [];
          }
          if (!acc[row.Category].includes(row.Measure)) {
            acc[row.Category].push(row.Measure);
          }
          return acc;
        }, {});

      this.measures2 = groupedMeasures;

      if (!this.selectedMeasure1) {
        const firstCategory = Object.keys(this.measures1)[0];
        this.selectedMeasure1 = this.measures1[firstCategory][0];
      }
      if (!this.selectedMeasure2) {
        const firstCategory = Object.keys(this.measures2)[0];
        this.selectedMeasure2 = this.measures2[firstCategory][0];
      }
    } catch (err) {
      console.error("Failed to load data:", err);
    }
  },
};
</script>

