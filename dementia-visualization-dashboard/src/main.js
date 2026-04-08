import { createApp } from 'vue'
import App from './App.vue'
import 'mapbox-gl/dist/mapbox-gl.css';
import router from './router';
import 'bootstrap/dist/css/bootstrap-grid.min.css'
import '@fortawesome/fontawesome-free/js/all'

createApp(App).use(router).mount('#app');
