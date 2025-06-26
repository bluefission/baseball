<template>
  <Header />

  <MDBContainer>

     <Details 
      v-if="showDetails" 
      :playerData="selectedPlayer" 
      @closeDetails="showDetails = false" />
    <Edit
      v-if="showDetails && selectedPlayer" 
      :playerData="selectedPlayer" 
      @closeDetails="showDetails = false" />

    <MainTable 
      :tableData="tableData"
      @selectPlayer="handleSelectPlayer" />

  </MDBContainer>
</template>

<script setup lang="ts">
import { 
  MDBContainer
} from "mdb-vue-ui-kit";
import MainTable from "./MainTable.vue";
import Header from "./Header.vue";
import Details from "./Details.vue";
import Edit from "./Edit.vue";
import { useFetch } from "@vueuse/core";

import { ref, watch } from "vue";

// intiate table data
// get all data from api (`api/players`)
const { data: tableData, isFetching } = useFetch('http://localhost:8000/api/players').get().json();

// show an alert when tableData loads
if (isFetching.value) {
  console.log("Loading player data...");
}

const selectedPlayer = ref(null);
const showDetails = ref(false);

const handleSelectPlayer = (player) => {
  // Set selected player data
  selectedPlayer.value = player;
  showDetails.value = true;
};

const handleEditPlayer = (player) => {
  // Set selected player data for editing
  selectedPlayer.value = player;
  showDetails.value = true;
};

// Watch for changes in tableData prop
watch(() => tableData.value, (newData) => {
  tableData.value = newData;
});
</script>
