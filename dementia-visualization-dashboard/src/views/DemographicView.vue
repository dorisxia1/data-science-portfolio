<template>
  <div>
    <h1 style="margin-bottom: 0.2rem;">Demographic Patterns of Dementia Prevalence</h1>
    <h3 style="margin-top: 0;">Who is most affected, and how can we explore the data more deeply?</h3>
    <div class="text-container mb-3">
    <p style="padding-left: 7rem; padding-right: 7rem; text-align: left;">
      This page focuses on how dementia prevalence varies across demographic dimensions. Research
      has shown that dementia prevalence is highest in the south<sup>1</sup>. The interactive bar chart contains a default view of
      dementia prevalence by state, <strong>highlighting the southern states</strong> to show whether results from the NORC Datahub also show the 
      same pattern.
    </p>

    <p style="padding-left: 7rem; padding-right: 7rem; text-align: left;">
      For additional usability, users have the option to further drill down and explore the data across other dimensions
      based on region, state, race, gender, and age.
    </p>

    <p style="padding-left: 7rem; padding-right: 7rem; text-align: left;">
      Using the interactive bar chart, users can:
    </p>
    
    <ul style="padding-left: 9rem; padding-right: 7rem; text-align: left;">
      <li>Click on a bar to drill down into the next demographic level.</li>
      <li>Use the dropdown menu to select the order of demographic levels for drill-down.</li>
      <li>Hover over bars to see detailed information about the data.</li>
      <li>Click the "Back" button to return to the previous view.</li>
    </ul>

    <p style="padding-left: 7rem; padding-right: 7rem; text-align: left;">
      The chart is designed to help users understand the complex relationships between different demographic factors and dementia prevalence, making it easier to identify at-risk populations and inform public health strategies.
    </p>
  </div>

    <DemographicBar />
  </div>

  <!-- Citation as a reference -->
  <div class="citation">
      <p style="font-size: 0.8em;">
        <sup>1</sup>Zacher, M., Brady, S., & Short, S. E. (2023). 
          <em>Geographic patterns of dementia in the United States: Variation by place of residence, place of birth, and subpopulation.</em>
          The Journals of Gerontology: Series B, 78(7), 1192–1203.
          <a href="https://doi.org/10.1093/geronb/gbad045" target="_blank" rel="noopener">https://doi.org/10.1093/geronb/gbad045</a>
      </p>
  </div>

</template>

<script>
import DemographicBar from "@/components/DemographicView/demographic_bar.vue";

export default {
  name: "DemographicView",
  components: {
    DemographicBar
  }
};
</script>

<style scoped>
.text-container {
  margin-bottom: 2rem;
}
</style>
