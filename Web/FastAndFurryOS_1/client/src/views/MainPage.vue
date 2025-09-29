<template>
  <div style="display: flex; justify-content: center;" class="m-4">
    <div class="hello">
      <h1>The Fast and Furryous Inventory and Missions Dashboard</h1>
      <p>
        We are a group of nice furr- people who love to design Operating Systems and apps!
      </p>
    </div>
    <div class="m-2 w-11/12">
      <img
      alt="A bridge. Yeah yeah it's fast and furious related."
      src="@/assets/nyc_bridge.png" />
    </div>
    </div>
    <p>
      Check out the other tabs of this website to learn more about us and what we do.
    </p>
</template>

<script>
export default {
  name: 'MainPage',
  props: {
    msg: String
  },
  methods: {
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
/* .hello {
  height: 70vh;
} */
div {
  padding: 1%;
}
p {
  margin-bottom: 5%;
}
h1 {
  /* Use a different font, and larger lettring */
  font-family: 'Courier New', Courier, monospace;
  font-size: 2em;
  /* Add a border to the bottom of the heading */
  border-bottom: 1px solid #333;
  /* Add some margin to the bottom of the heading */
  margin: 20px 0 50px 0;
}
/* h3 {
  margin: 40px 0 0;
} */
ul {
  list-style-type: none;
  padding: 0;
}
a {
  color: #42b983;
}
img {
  margin: 1%;
}
</style>
