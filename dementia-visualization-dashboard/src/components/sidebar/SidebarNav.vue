<script>
import SidebarLink from './SidebarLink'
import { collapsed, toggleSidebar, sidebarWidth } from './state'

export default {
  props: {},
  components: { SidebarLink },
  setup() {
    return { collapsed, toggleSidebar, sidebarWidth }
  }
}
</script>

<template>
  <div class="sidebar" :style="{ width: sidebarWidth }">
    <h1>
      <span v-if="collapsed">
         <!-- Placeholder if we want something here -->
      </span>
      <span v-else>Team VizRD</span>
    </h1>

    <SidebarLink to="/" icon="fas fa-home">
      <span style="font-size: 0.8em;">Overview</span>
    </SidebarLink>
    <SidebarLink to="/risk-hotspots" icon="fas fa-map-location">
      <span style="font-size: 0.8em;">Risk Factor Hotspots</span>
    </SidebarLink>
    <SidebarLink to="/demographic-patterns" icon="fas fa-people-group">
      <span style="font-size: 0.8em;">Demographic Patterns</span>
    </SidebarLink>
    <SidebarLink to="/medicare-coverage" icon="fas fa-file-medical">
      <span style="font-size: 0.8em;">Medicare Coverage</span>
    </SidebarLink>
    <SidebarLink to="/environmental-risks" icon="fas fa-tree-city">
      <span style="font-size: 0.8em;">Environmental Risks</span>
    </SidebarLink>

    <span
      class="collapse-icon"
      :class="{ 'rotate-180': collapsed }"
      @click="toggleSidebar"
    >
      <i class="fas fa-angle-double-left" />
    </span>
  </div>
</template>

<style>
:root {
  --sidebar-bg-color: #2a4365;
  --sidebar-item-hover: #2c5282;
  --sidebar-item-active: #1a365d;
}
</style>

<style scoped>
.sidebar {
  color: white;
  background-color: var(--sidebar-bg-color);

  float: left;
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  padding: 0.5em;

  transition: 0.3s ease;

  display: flex;
  flex-direction: column;
}

.sidebar h1 {
  height: 2.5em;
}

.collapse-icon {
  position: absolute;
  bottom: 0;
  padding: 0.75em;

  color: rgba(255, 255, 255, 0.7);

  transition: 0.2s linear;
}

.rotate-180 {
  transform: rotate(180deg);
  transition: 0.2s linear;
}
</style>