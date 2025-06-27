<template>
  <MDBContainer class="py-4">
    <h2 class="mb-4 text-center">Player Details</h2>

    <div v-if="playerData">
      <!-- Player Name Full Width -->
      <MDBRow class="mb-3">
        <MDBCol>
          <h4><strong>Player Name:</strong> {{ playerData.player_name }}</h4>
        </MDBCol>
      </MDBRow>

      <MDBRow class="mb-8">
        <MDBCol>
          <!-- notes area -->
          <p><strong>Notes:</strong> {{ playerData.notes || 'No notes available.' }}</p>
        </MDBCol>
      </MDBRow>

      <!-- Two Column Stats Layout -->
      <MDBRow>
        <MDBCol md="6">
          <p><strong>Position:</strong> {{ playerData.position }}</p>
          <p><strong>Games:</strong> {{ playerData.games }}</p>
          <p><strong>At-bat:</strong> {{ playerData.at_bat }}</p>
          <p><strong>Runs:</strong> {{ playerData.runs }}</p>
          <p><strong>Hits:</strong> {{ playerData.hits }}</p>
          <p><strong>Hits Per Game:</strong> {{ playerData.hits_per_game }}</p>
          <p><strong>Double (2B):</strong> {{ playerData.double_2b }}</p>
          <p><strong>Third Baseman:</strong> {{ playerData.third_baseman }}</p>
          <p><strong>Home Run:</strong> {{ playerData.home_run }}</p>
        </MDBCol>

        <MDBCol md="6">
          <p><strong>Run Batted In:</strong> {{ playerData.run_batted_in }}</p>
          <p><strong>A Walk:</strong> {{ playerData.a_walk }}</p>
          <p><strong>Strikeouts:</strong> {{ playerData.strikeouts }}</p>
          <p><strong>Stolen Base:</strong> {{ playerData.stolen_base }}</p>
          <p><strong>Caught Stealing:</strong> {{ playerData.caught_stealing }}</p>
          <p><strong>AVG:</strong> {{ playerData.avg }}</p>
          <p><strong>On-base Percentage:</strong> {{ playerData.on_base_percentage }}</p>
          <p><strong>Slugging Percentage:</strong> {{ playerData.slugging_percentage }}</p>
          <p><strong>On-base Plus Slugging:</strong> {{ playerData.on_base_plus_slugging }}</p>
        </MDBCol>
      </MDBRow>

      <!-- Action Buttons -->
      <MDBRow class="mt-4">
        <MDBCol class="d-flex justify-content-end gap-2">
          <MDBBtn color="secondary" @click="$emit('editPlayer', playerData)">Edit Player</MDBBtn>
          <MDBBtn color="danger" @click="$emit('closeDetails')">Close</MDBBtn>
        </MDBCol>
      </MDBRow>
    </div>
  </MDBContainer>
</template>

<script setup lang="ts">
import { ref, defineProps, watch } from 'vue';
import { MDBContainer, MDBRow, MDBCol, MDBBtn } from "mdb-vue-ui-kit";

const props = defineProps({
  playerData: {
    type: Object,
    required: true
  }
});

const playerData = ref(props.playerData);

// Keep playerData reactive to prop updates
watch(() => props.playerData, (newData) => {
  // hits per game calculation
  if (newData.games > 0) {
    newData.hits_per_game = (newData.hits / newData.games).toFixed(2);
  } else {
    newData.hits_per_game = 0;
  }

  playerData.value = newData;
});
</script>
