<template>
  <MDBTable class="align-middle mb-0 bg-white">
    <thead class="bg-light">
      <tr>
        <th>Player Name</th>
        <th>Position</th>
        <th>Games</th>
        <th>At-bat</th>
        <th>Runs</th>
        <th>Hits</th>
        <th>Hits Per Game</th>
        <th>Double (2B)</th>
        <th>Third Baseman</th>
        <th>Home Run</th>
        <th>Run Batted In</th>
        <th>A Walk</th>
        <th>Strikeouts</th>
        <th>Stolen Base</th>
        <th>Caught Stealing</th>
        <th>AVG</th>
        <th>On-base Percentage</th>
        <th>Slugging Percentage</th>
        <th>On-base Plus Slugging</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in tableData" :key="index">
        <td @click="$emit('selectPlayer', item)" 
            class="text-primary cursor-pointer">
          {{ item.player_name }} 
          <!-- <span class="text-muted">(Click for details)</span> -->
        </td>
        <td>{{ item.position }}</td>
        <td>{{ item.games }}</td>
        <td>{{ item.at_bat }}</td>
        <td>{{ item.runs }}</td>
        <td>{{ item.hits }}</td>
        <td>{{ item.hits_per_game }}</td>
        <td>{{ item.double_2b }}</td>
        <td>{{ item.third_baseman }}</td>
        <td>{{ item.home_run }}</td>
        <td>{{ item.run_batted_in }}</td>
        <td>{{ item.a_walk }}</td>
        <td>{{ item.strikeouts }}</td>
        <td>{{ item.stolen_base }}</td>
        <td>{{ item.caught_stealing }}</td>
        <td>{{ item.avg }}</td>
        <td>{{ item.on_base_percentage }}</td>
        <td>{{ item.slugging_percentage }}</td>
        <td>{{ item.on_base_plus_slugging }}</td>
      </tr>
    </tbody>
  </MDBTable>
</template>
<script setup lang="ts">
import { 
  MDBTable
} from "mdb-vue-ui-kit";
import { ref, watch } from "vue";

const props = defineProps({
  tableData: {
    type: Array,
    required: true
  }
});
// make sure component emits selectPlayer event when a player name is clicked to parent
// component
// to display player details in Details.vue component
const emit = defineEmits(['selectPlayer']);

const tableData = ref(props.tableData);
// Watch for changes in tableData prop
watch(() => props.tableData, (newData) => {

  // Calculate hits per game for each player
  newData.forEach(player => {
    if (player.games > 0) {
      player.hits_per_game = (player.hits / player.games).toFixed(2);
    } else {
      player.hits_per_game = 0;
    }
  });

  // Sort by hits per game
  newData.sort((a, b) => b.hits_per_game - a.hits_per_game);

  tableData.value = newData;
});
</script>
