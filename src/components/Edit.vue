<template>
  <form>
    <!-- Player Name and Position -->
    <MDBRow class="mb-4">
      <MDBCol>
        <MDBInput
          type="text"
          label="Player Name"
          id="form6PlayerName"
          v-model="playerForm.player_name"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="text"
          label="Position"
          id="form6Position"
          v-model="playerForm.position"
        />
      </MDBCol>
    </MDBRow>

    <!-- Games, At-bat, Runs, Hits -->
    <MDBRow class="mb-2">
      <MDBCol>
        <MDBInput
          type="number"
          label="Games"
          id="form6Games"
          v-model="playerForm.games"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="At-bat"
          id="form6AtBat"
          v-model="playerForm.at_bat"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Runs"
          id="form6Runs"
          v-model="playerForm.runs"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Hits"
          id="form6Hits"
          v-model="playerForm.hits"
        />
      </MDBCol>
    </MDBRow>

    <!-- Doubles, Third Baseman, Home Runs, RBIs -->
    <MDBRow class="mb-2">
      <MDBCol>
        <MDBInput
          type="number"
          label="Double (2B)"
          id="form6Double"
          v-model="playerForm.double_2b"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Third Baseman"
          id="form6ThirdBaseman"
          v-model="playerForm.third_baseman"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Home Run"
          id="form6HomeRun"
          v-model="playerForm.home_run"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Run Batted In"
          id="form6RBI"
          v-model="playerForm.run_batted_in"
        />
      </MDBCol>
    </MDBRow>

    <!-- Walks, Strikeouts, Stolen Base, Caught Stealing -->
    <MDBRow class="mb-2">
      <MDBCol>
        <MDBInput
          type="number"
          label="A Walk"
          id="form6Walk"
          v-model="playerForm.a_walk"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Strikeouts"
          id="form6Strikeouts"
          v-model="playerForm.strikeouts"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Stolen Base"
          id="form6StolenBase"
          v-model="playerForm.stolen_base"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Caught Stealing"
          id="form6CaughtStealing"
          v-model="playerForm.caught_stealing"
        />
      </MDBCol>
    </MDBRow>

    <!-- AVG, OBP, SLG, OPS -->
    <MDBRow class="mb-2">
      <MDBCol>
        <MDBInput
          type="number"
          label="AVG"
          id="form6AVG"
          v-model="playerForm.avg"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="On-base Percentage"
          id="form6OnBasePercentage"
          v-model="playerForm.on_base_percentage"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Slugging Percentage"
          id="form6SluggingPercentage"
          v-model="playerForm.slugging_percentage"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="On-base Plus Slugging"
          id="form6OPS"
          v-model="playerForm.on_base_plus_slugging"
        />
      </MDBCol>
    </MDBRow>

    <!-- Notes and Submit -->
    <MDBRow class="mb-4">
      <MDBCol>
        <MDBTextarea 
          rows="4"
          label="Notes"
          id="form6Notes"
          v-model="playerForm.notes"
        />
      </MDBCol>
    </MDBRow>

    <MDBBtn color="primary" block class="mb-4">
      Submit Player Data
    </MDBBtn>
  </form>
</template>

<script setup lang="ts">
import {
  MDBRow,
  MDBCol,
  MDBInput,
  MDBTextarea,
  MDBBtn
} from "mdb-vue-ui-kit";
import { ref, defineProps, watch } from 'vue';

// Unified object matching playerData structure
const playerForm = ref({
  player_name: '',
  position: '',
  games: 0,
  at_bat: 0,
  runs: 0,
  hits: 0,
  double_2b: 0,
  third_baseman: 0,
  home_run: 0,
  run_batted_in: 0,
  a_walk: 0,
  strikeouts: 0,
  stolen_base: 0,
  caught_stealing: 0,
  avg: 0,
  on_base_percentage: 0,
  slugging_percentage: 0,
  on_base_plus_slugging: 0,
  notes: ''
});
// Watch for changes in playerData prop
const props = defineProps({
  playerData: {
    type: Object,
    required: true
  }
});
// Update playerForm with initial playerData
watch(() => props.playerData, (newData) => {
  playerForm.value = { ...newData };
}, { immediate: true });
// Emit event when form is submitted
const emit = defineEmits(['submitPlayerData']);

</script>
