<template>
  <form>
    <!-- Player Name and Position -->
    <MDBRow class="mb-4">
      <MDBCol>
        <MDBInput
          type="text"
          label="Player Name"
          id="form6PlayerName"
          v-model="playerForm['Player name']"
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
          v-model="playerForm.Games"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="At-bat"
          id="form6AtBat"
          v-model="playerForm['At-bat']"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Runs"
          id="form6Runs"
          v-model="playerForm.Runs"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Hits"
          id="form6Hits"
          v-model="playerForm.Hits"
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
          v-model="playerForm['Double (2B)']"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Third Baseman"
          id="form6ThirdBaseman"
          v-model="playerForm['third baseman']"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Home Run"
          id="form6HomeRun"
          v-model="playerForm['home run']"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Run Batted In"
          id="form6RBI"
          v-model="playerForm['run batted in']"
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
          v-model="playerForm['a walk']"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Strikeouts"
          id="form6Strikeouts"
          v-model="playerForm.Strikeouts"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Stolen Base"
          id="form6StolenBase"
          v-model="playerForm['stolen base']"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Caught Stealing"
          id="form6CaughtStealing"
          v-model="playerForm['Caught stealing']"
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
          v-model="playerForm.AVG"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="On-base Percentage"
          id="form6OnBasePercentage"
          v-model="playerForm['On-base Percentage']"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="Slugging Percentage"
          id="form6SluggingPercentage"
          v-model="playerForm['Slugging Percentage']"
        />
      </MDBCol>
      <MDBCol>
        <MDBInput
          type="number"
          label="On-base Plus Slugging"
          id="form6OPS"
          v-model="playerForm['On-base Plus Slugging']"
        />
      </MDBCol>
    </MDBRow>

    <!-- Notes and Submit -->
    <MDBRow class="mb-4">
      <MDBCol>
        <MDBInput
          type="text"
          label="Notes"
          id="form6Notes"
          v-model="playerForm.Notes"
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
  MDBBtn
} from "mdb-vue-ui-kit";
import { ref, defineProps, watch } from 'vue';

// Unified object matching playerData structure
const playerForm = ref({
  "Player name": '',
  position: '',
  Games: 0,
  "At-bat": 0,
  Runs: 0,
  Hits: 0,
  "Double (2B)": 0,
  "third baseman": 0,
  "home run": 0,
  "run batted in": 0,
  "a walk": 0,
  Strikeouts: 0,
  "stolen base": 0,
  "Caught stealing": 0,
  AVG: 0,
  "On-base Percentage": 0,
  "Slugging Percentage": 0,
  "On-base Plus Slugging": 0,
  Notes: ''
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
});
// Emit event when form is submitted
const emit = defineEmits(['submitPlayerData']);
</script>
