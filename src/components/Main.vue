<template>
  <Header />

  <MDBContainer>
    <MainTable 
      :tableData="tableData" />
  </MDBContainer>
</template>

<script setup lang="ts">
import { 
  MDBContainer
} from "mdb-vue-ui-kit";
import MainTable from "./MainTable.vue";
import Header from "./Header.vue";
import Details from "./Details.vue";
import { ref } from "vue";

// intiate table data
const tableData = ref([
    {"Player name":"B Bonds","position":"LF","Games":2986,"At-bat":9847,"Runs":2227,"Hits":2935,"Double (2B)":601,"third baseman":77,"home run":762,"run batted in":1996,"a walk":2558,"Strikeouts":1539,"stolen base":514,"Caught stealing":141,"AVG":0.298,"On-base Percentage":0.444,"Slugging Percentage":0.607,"On-base Plus Slugging":1.051},
    {"Player name":"H Aaron","position":"RF","Games":3298,"At-bat":12364,"Runs":2174,"Hits":3771,"Double (2B)":624,"third baseman":98,"home run":755,"run batted in":2297,"a walk":1402,"Strikeouts":1383,"stolen base":240,"Caught stealing":73,"AVG":0.305,"On-base Percentage":0.374,"Slugging Percentage":0.555,"On-base Plus Slugging":0.929},
    {"Player name":"B Ruth","position":"RF","Games":2504,"At-bat":8399,"Runs":2174,"Hits":2873,"Double (2B)":506,"third baseman":136,"home run":714,"run batted in":2213,"a walk":2062,"Strikeouts":1330,"stolen base":123,"Caught stealing":117,"AVG":0.342,"On-base Percentage":0.474,"Slugging Percentage":0.69,"On-base Plus Slugging":1.164}
]);
</script>
