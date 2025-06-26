<template>
  <MDBContainer class="py-4">
    <h2 class="mb-4 text-center">Player Details</h2>

    <div v-if="playerData">
      <!-- Player Name Full Width -->
      <MDBRow class="mb-3">
        <MDBCol>
          <h4><strong>Player Name:</strong> {{ playerData['Player name'] }}</h4>
        </MDBCol>
      </MDBRow>

      <!-- Two Column Stats Layout -->
      <MDBRow>
        <MDBCol md="6">
          <p><strong>Position:</strong> {{ playerData.position }}</p>
          <p><strong>Games:</strong> {{ playerData.Games }}</p>
          <p><strong>At-bat:</strong> {{ playerData['At-bat'] }}</p>
          <p><strong>Runs:</strong> {{ playerData.Runs }}</p>
          <p><strong>Hits:</strong> {{ playerData.Hits }}</p>
          <p><strong>Double (2B):</strong> {{ playerData['Double (2B)'] }}</p>
          <p><strong>Third Baseman:</strong> {{ playerData['third baseman'] }}</p>
          <p><strong>Home Run:</strong> {{ playerData['home run'] }}</p>
        </MDBCol>

        <MDBCol md="6">
          <p><strong>Run Batted In:</strong> {{ playerData['run batted in'] }}</p>
          <p><strong>A Walk:</strong> {{ playerData['a walk'] }}</p>
          <p><strong>Strikeouts:</strong> {{ playerData.Strikeouts }}</p>
          <p><strong>Stolen Base:</strong> {{ playerData['stolen base'] }}</p>
          <p><strong>Caught Stealing:</strong> {{ playerData['Caught stealing'] }}</p>
          <p><strong>AVG:</strong> {{ playerData.AVG }}</p>
          <p><strong>On-base Percentage:</strong> {{ playerData['On-base Percentage'] }}</p>
          <p><strong>Slugging Percentage:</strong> {{ playerData['Slugging Percentage'] }}</p>
          <p><strong>On-base Plus Slugging:</strong> {{ playerData['On-base Plus Slugging'] }}</p>
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
  playerData.value = newData;
});
</script>
