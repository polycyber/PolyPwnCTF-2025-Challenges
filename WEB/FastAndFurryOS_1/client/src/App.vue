<template>
  <NavBar />
  <main>
    <RouterView />
  </main>
  <BottomBar />
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import BottomBar from '@/components/BottomBar.vue'
export default {
  name: 'App',
  components: {
    NavBar,
    BottomBar
  }
}
</script>

<style>
@import './style.css';
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  /* color: #2c3e50; */
  /* margin-top: 60px; */
}
</style>
