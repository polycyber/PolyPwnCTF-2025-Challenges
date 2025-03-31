<template>
  <div class="hello mb-80">

    <h2>Page not found.</h2>
    <p>
      Sowwy, the URL you wrote does not exist.
      <br><br><b><a href="/">Back to main page Owo</a></b>
    </p>

  </div>
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
h2 {
  /* Use a different font, and larger lettring */
  font-family: 'Courier New', Courier, monospace;
  font-size: 1.5em;
  /* Add a border to the bottom of the heading */
  border-bottom: 0.5px solid #363;
  /* Add some margin to the bottom of the heading */
  margin: 20px 0 50px 0;
}
a {
  color: #42b983;
}
</style>
