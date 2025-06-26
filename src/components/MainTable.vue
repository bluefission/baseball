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
          {{ item['Player name'] }} 
          <!-- <span class="text-muted">(Click for details)</span> -->
        </td>
        <td>{{ item.position }}</td>
        <td>{{ item.Games }}</td>
        <td>{{ item['At-bat'] }}</td>
        <td>{{ item.Runs }}</td>
        <td>{{ item.Hits }}</td>
        <td>{{ item['Double (2B)'] }}</td>
        <td>{{ item['third baseman'] }}</td>
        <td>{{ item['home run'] }}</td>
        <td>{{ item['run batted in'] }}</td>
        <td>{{ item['a walk'] }}</td>
        <td>{{ item.Strikeouts }}</td>
        <td>{{ item['stolen base'] }}</td>
        <td>{{ item['Caught stealing'] }}</td>
        <td>{{ item.AVG }}</td>
        <td>{{ item['On-base Percentage'] }}</td>
        <td>{{ item['Slugging Percentage'] }}</td>
        <td>{{ item['On-base Plus Slugging'] }}</td>
      </tr>
    </tbody>
  </MDBTable>
</template>
<script setup lang="ts">
import { 
  MDBTable
} from "mdb-vue-ui-kit";
import { ref } from "vue";

const props = defineProps({
  tableData: {
    type: Array,
    required: true
  }
});
// ]);
</script>
