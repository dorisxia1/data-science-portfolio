<template>
  <div style="padding: 0 0px;">
    <div v-for="(section, index) in sections" :key="index" class="accordion-section">
      <button @click="toggleSection(index)" class="accordion-header">
        {{ activeSection === index ? '▼' : '▶' }} {{ section.title }}
      </button>
      <div v-if="activeSection === index" class="accordion-content">
        <div v-if="!section.nested">
          <p v-html="section.description"></p> <!-- Enable HTML rendering -->
        </div>
        <div v-else>
          <p v-if="section.title === 'Data Sources'" style="margin-bottom: 5px; text-align: left;">
            The Data That Informed Our Work:
          </p>
          <p v-else style="margin-bottom: 5px; text-align: left;">
            What Do You Want to Explore?:
          </p>
          <div v-for="(item, subIndex) in section.nested" :key="subIndex" class="nested-item">
            <button @click="toggleNested(index, subIndex)" class="nested-header">
              <template v-if="section.title === 'Data Sources'">
                {{ activeNested[index] === subIndex ? '▼' : '▶' }}
              </template>
              <i :class="item.icon" style="margin-right: 8px;"></i> {{ item.title }}
            </button>
            <div v-if="activeNested[index] === subIndex" class="nested-content">
              <p v-html="item.description" style="text-align: left;"></p> <!-- Left-justify text -->
              <button
                v-if="section.title !== 'Data Sources'"
                @click="navigateTo(item.link)"
                style="color: #2c5282; text-decoration: underline; background: none; border: none; cursor: pointer;"
              >
                Go to page
              </button> <!-- Use router navigation -->
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useRouter } from "vue-router"; // Import useRouter to access the router instance

export default {
  name: "NestedAccordion",
  data() {
    return {
      activeSection: 0, // Set the first section ("Background & Purpose") to be initially open
      activeNested: {}, // Initialize as an empty object
      sections: [
        {
          title: "Background & Purpose",
          description: `
            <strong>Understanding the Challenge</strong><br>
            <div style="text-align: left;">
              Dementia, including Alzheimer's disease, is a growing public health crisis affecting millions of older adults in the United States. As the population ages, the burden of dementia is expected to rise sharply—impacting families, healthcare systems, and communities. However, the factors that contribute to dementia risk and disparities in care remain complex and unevenly distributed across the country.
            </div>
            <br><br>
            <strong>Our Solution</strong><br>
            <div style="text-align: left;">
              This interactive tool was developed to explore the spatial and contextual dimensions of dementia in the U.S. By combining prevalence estimates with data on demographics, health risk factors, Medicare coverage, and physical environmental / socioeconomic risks, the tool identifies where the burden is greatest and what factors may be driving it. Users can interactively explore a variety of measures such as age, race, comorbidities, environmental risks and other factors relate to dementia risk—supporting research, healthcare planning, and informed policymaking.
            </div>`,
        },
        {
          title: "Sections at a Glance",
          nested: [
            { title: "Risk Factor Hotspots", icon: "fas fa-map-location", description: "This page includes a map that highlights U.S. counties where dementia prevalence is unexpectedly high or low based on known risk factors like stroke, diabetes, and cognitive disability. By comparing observed and predicted rates, the Mismatch Index reveals areas where dementia burden is greater—or less—than expected, helping identify regions that may need deeper investigation or targeted interventions.", link: "/risk-hotspots" },
            { title: "Demographic Patterns", icon: "fas fa-people-group", description: "This page explores how dementia prevalence varies across key demographic factors such as age, race, gender, and region. It features an interactive bar chart which you can use to drill down into different demographic levels, sort by value or age, and uncover trends in how specific populations are affected by dementia. This tool aims to help users identify at-risk groups and better understand the complex relationships between demographic factors and dementia prevalence.", link: "/demographic-patterns" },
            { title: "Medicare Coverage", icon: "fas fa-file-medical", description: "This page examines patterns in Medicare coverage among dementia patients, focusing on whether certain racial or ethnic groups are more likely to opt for Medicare Advantage over Traditional Medicare. Featuring a zoomable circle packing visualization, users can explore the distribution of insurance types, with node colors representing different categories and sizes highlighting trends in enrollment. This providing a clear, interactive way to uncover insights about insurance choices and their relationship to dementia care.", link: "/medicare-coverage" },
            { title: "Environmental Risks", icon: "fas fa-tree-city", description: "This page allows users to explore the relationship between dementia outcomes and environmental risk factors at the county level. It features choropleth maps for dementia and environmental factors, followed by bivariate visualizations (spike map and scatter plot) to identify areas with high risk. The interactive design makes it easy to analyze patterns and correlations across regions.", link: "/environmental-risks" },
          ],
        },
        {
          title: "Data Sources",
          nested: [
            {
              title: "NORC Dementia DataHub",
                description: "The 2020 Dementia Data Hub dataset provides detailed estimates of dementia-related health outcomes across the United States at the national, state, and county levels. It includes data on Medicare beneficiaries, stratified by insurance type (Fee-for-Service or Medicare Advantage), age group, sex, race/ethnicity, and dementia diagnosis status. Key measures include the number of beneficiaries, dementia prevalence and incidence, COVID-19 cases among those with dementia, and dementia-related deaths.<br><br>" +
                "<small><strong>Data source:</strong> NORC at the University of Chicago. (2024). Dementia Datahub Public Use File (2020 Data). Retrieved from <a href='https://dementiadatahub.org' target='_blank'>dementiadatahub.org</a></small>",
            },
            {
              title: "CDC PLACES Dataset",
              description: "The CDC PLACES dataset provides model-based estimates of chronic disease measures, including health outcomes, behaviors, and prevention practices at the county level. The risk factor page integrated these county-level prevalence estimates of chronic conditions like stroke, diabetes, and cognitive disability with dementia prevalence data to identify areas where dementia burden deviates from expected levels based on known risk factors. Additionally, the dataset was used to analyze environmental risk factors (both physical- and social-environmental factors) for dementia, such as housing insecurity, transportation access, physical inactivity, and social isolation, offering insights of the relationship of these factors to cognitive health outcomes.<br><br>" +
                "<small><strong>Data source:</strong> Centers for Disease Control and Prevention. PLACES: Local Data for Better Health. Retrieved from <a href='https://cdc.gov/places' target='_blank'>cdc.gov/places</a></small>",
            },
            {
              title: "Annual AQI by County",
              description: "This dataset contains air quality index (AQI) data for U.S. counties in 2020, including metrics such as median air quality index scores (AQI) and pollutant-specific measures like ozone and PM2.5. Metrics on physical environmental risk factors are included in this project due to previous research suggesting links between prolonged exposure to pollutants like ozone and PM2.5 and an increased risk of cognitive decline and dementia. <br><br>" +
                "<small><strong>Data source:</strong> United States Environmental Protection Agency. Annual AQI Summary Data by County (2020 Data). <a href='https://www.epa.gov/outdoor-air-quality-data' target='_blank'>Retrieved from epa.gov</a></small>",
            },
            {
              title: "US County Temperatures and Precipitation",
              description: "Two datasets, which include annual temperature and precipitation data for U.S. counties, provides insights into environmental conditions that may influence dementia risk. Extreme temperatures can pose health risks for individuals with dementia, as the condition may impair the body's ability to regulate temperature, increasing vulnerability to heatstroke or hypothermia. Additionally, precipitation may limit outdoor mobility for older adults, potentially reducing social engagement and physical activity.<br><br>" +
                "<small><strong>Data source:</strong> National Centers for Environmental Information. (2024). Climate at a Glance (2020 County Data). Retrieved from <a href='https://www.ncei.noaa.gov/access/monitoring/climate-at-a-glance/' target='_blank'>ncdc.noaa.gov</a></small>",
            },
          ],
        },
      ],
    };
  },
  setup() {
    const router = useRouter(); // Get the router instance
    const navigateTo = (path) => {
      router.push(path); // Use router.push for navigation
    };

    return {
      navigateTo, // Expose the navigateTo method to the template
    };
  },
  methods: {
    toggleSection(index) {
      this.activeSection = this.activeSection === index ? null : index;
    },
    toggleNested(sectionIndex, nestedIndex) {
      if (!Object.prototype.hasOwnProperty.call(this.activeNested, sectionIndex)) {
        this.activeNested[sectionIndex] = null; // Initialize if undefined
      }
      this.activeNested[sectionIndex] =
        this.activeNested[sectionIndex] === nestedIndex ? null : nestedIndex;
    },
  },
};
</script>

<style>
.accordion-header {
  background-color: #2c5282;
  color: white;
  padding: 10px;
  border: none;
  text-align: left;
  width: 100%;
  cursor: pointer;
  font-size: 1.2em;
  margin-bottom: 10px; /* Add space between sections */
  border-radius: 8px; /* Rounded corners */
}

.accordion-content {
  padding: 10px;
  background-color: #f1f1f1;
  margin-bottom: 10px; /* Add space below content */
  border-radius: 8px; /* Rounded corners */
}

.nested-header {
  background-color: #3b6998;
  color: white;
  padding: 8px;
  border: none;
  text-align: left;
  width: 100%;
  cursor: pointer;
  font-size: 1em;
  margin-bottom: 5px; /* Add space between nested items */
  display: flex;
  align-items: center;
  border-radius: 8px; /* Rounded corners */
}

.nested-content {
  padding: 8px;
  background-color: #e8f4ff;
  margin-bottom: 5px; /* Add space below nested content */
  border-radius: 8px; /* Rounded corners */
}
</style>