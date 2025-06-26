<template>
  <header>
    <!-- Navbar -->
    <MDBNavbar expand="lg" light bg="white" container>
      <MDBNavbarToggler
        target="#navbarExample01"
        @click="collapse1 = !collapse1"
      ></MDBNavbarToggler>
      <MDBCollapse id="#navbarExample01" v-model="collapse1">
        <MDBNavbarNav class="mb-2 mb-lg-0">
          <MDBNavbarItem to="#" active> Baseball Stats </MDBNavbarItem>
        </MDBNavbarNav>
      </MDBCollapse>
    </MDBNavbar>
    <!-- Navbar -->
  </header>
</template>
<script setup lang="ts">
  import {
    MDBNavbar,
    MDBNavbarToggler,
    MDBCollapse,
    MDBNavbarNav,
    MDBNavbarItem
  } from "mdb-vue-ui-kit";

</script>