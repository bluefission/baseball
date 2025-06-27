<template>
  <Header />

  <MDBContainer>

     <Details 
      v-if="showDetails" 
      :playerData="selectedPlayer" 
      @closeDetails="showDetails = false"
      @editPlayer="handleEditPlayer"  />
    <Edit
      v-if="showEdit && selectedPlayer" 
      :playerData="selectedPlayer" 
      @closeDetails="showDetails = false"
      @submitPlayerData="handleSubmitPlayerData" />

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
const showEdit = ref(false);

const handleSelectPlayer = (player) => {
  // Set selected player data
  console.log("Selected player:", player);
  let player2 = player;

  if (player.notes === null || player.notes == '') {
    const { data: player2, isFetching } = useFetch('http://localhost:8000/api/player/'+player.player_id).get().json();

    if (isFetching.value) {
      console.log("Loading player details...");
    }

    // set selected player data when fetch is complete
    selectedPlayer.value = player2;
    showDetails.value = true;

  } else {
    selectedPlayer.value = player;
    showDetails.value = true;
  }
};

const handleEditPlayer = (player) => {
  // Set selected player data for editing
  selectedPlayer.value = player;
  showDetails.value = false;
  showEdit.value = true;
};

const handleSubmitPlayerData = (updatedPlayer) => {
  // submit updated player data to the API
  console.log("Submitting updated player data:", updatedPlayer);

  // Account for CORS warnings
  fetch(`http://localhost:8000/api/player/${updatedPlayer.player_id}`, {
    method: 'PUT',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(updatedPlayer),
  });

  // Update the tableData with the updated player data
  const index = tableData.value.findIndex(player => player.player_id === updatedPlayer.player_id);
  if (index !== -1) {
    tableData.value[index] = updatedPlayer;
  }
  // Close the details view
  showDetails.value = false;
};

// Watch for changes in tableData prop
watch(() => tableData.value, (newData) => {
  tableData.value = newData;
});
</script>
