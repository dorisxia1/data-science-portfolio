<template>
  <div style="padding: 0 20px; width: 100%; margin: 0 auto; text-align: center;">
    <img alt="dementia logo" src="../assets/memory-loss.png" width="200" height="200" />
    <h1 style="color: #2c5282; margin-bottom: 0px;">Visualizing the Dementia Population</h1>
    <span style="font-size: 0.8em"><strong>Team VizRD: </strong>
    <strong>V</strong>easna T. Pusateri, 
    <strong>R</strong>ichard Gallardo, 
    <strong>D</strong>oris Xia, 
    <strong>D</strong>amita Gomez</span>
  </div>
  <div style="padding: 20px 0 0; width: 75%; margin: 0 auto; text-align: center;">
    <div style="text-align: center;">
      <NestedAccordion />
    </div>
  </div>
</template>

<script>
import NestedAccordion from "@/components/HomeView/NestedAccordion.vue";

export default {
  name: "HomeView",
  components: {
    NestedAccordion,
  },
};
</script>