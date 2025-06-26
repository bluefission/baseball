<template>
  <!-- display player information in an organized layout -->
  <div class="details-container">
    <h2>Player Details</h2>
    <div v-if="playerData" class="player-details">
      <p><strong>Player Name:</strong> {{ playerData['Player name'] }}</p>
      <p><strong>Position:</strong> {{ playerData.position }}</p>
      <p><strong>Games:</strong> {{ playerData.Games }}</p>
      <p><strong>At-bat:</strong> {{ playerData['At-bat'] }}</p>
      <p><strong>Runs:</strong> {{ playerData.Runs }}</p>
      <p><strong>Hits:</strong> {{ playerData.Hits }}</p>
      <p><strong>Double (2B):</strong> {{ playerData['Double (2B)'] }}</p>
      <p><strong>Third Baseman:</strong> {{ playerData['third baseman'] }}</p>
      <p><strong>Home Run:</strong> {{ playerData['home run'] }}</p>
      <p><strong>Run Batted In:</strong> {{ playerData['run batted in'] }}</p>
      <p><strong>A Walk:</strong> {{ playerData['a walk'] }}</p>
      <p><strong>Strikeouts:</strong> {{ playerData.Strikeouts }}</p>
      <p><strong>Stolen Base:</strong> {{ playerData['stolen base'] }}</p>
      <p><strong>Caught Stealing:</strong> {{ playerData['Caught stealing'] }}</p>
      <p><strong>AVG:</strong> {{ playerData.AVG }}</p>
      <p><strong>On-base Percentage:</strong> {{ playerData['On-base Percentage'] }}</p>
      <p><strong>Slugging Percentage:</strong> {{ playerData['Slugging Percentage'] }}</p>
      <p><strong>On-base Plus Slugging:</strong> {{ playerData['On-base Plus Slugging'] }}</p>
    </div>
    <button @click="$emit('closeDetails')">Close</button>
  </div>
</template>
<script setup lang="ts">
import { ref, defineProps } from 'vue';

const props = defineProps({
  playerData: {
    type: Object,
    required: true
  }
});
const playerData = ref(props.playerData);
// Watch for changes in playerData prop
watch(() => props.playerData, (newData) => {
  playerData.value = newData;
});
</script>