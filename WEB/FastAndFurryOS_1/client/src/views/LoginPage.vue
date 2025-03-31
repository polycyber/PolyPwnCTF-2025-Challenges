<template>
  <div class="hello mb-24">
    <h1>The Fast and Furious Inventory and Missions Dashboard</h1>
    <p>
      TEMPORARY LOGIN CONSOLE, FOR REQUESTING ACCESS TO THE SECRET FURRYOS UNDER DEVELOPMENT.
    </p>

    <form @submit.prevent="login" class="p-4">
      <div>
        <label for="fursonna">Fursonna:</label>
        <input type="text" id="fursonna" v-model="fursonna" required>
      </div>
      <div>
        <label for="password">Password:</label>
        <input v-model="password" type="password" required>
      </div>
      <button class="btn m-2" type="submit">Get Credentials</button>
    </form>
    <p v-if="data">Server confirmation: {{ data }}</p>

  </div>
</template>

<script>
export default {
  name: 'MainPage',
  props: {
    msg: String
  },
  methods: {
    async login() {
      const response = await fetch("http://ctf.polycyber.io:20304/secret_tmp_login", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          user_name: this.fursonna,
          password: this.password
        })
      });
      console.log(this.fursonna, " ", this.password);
      this.data = await response.json();
      return "aaa";
    }
  },
  data() {
    return {
      data: null,
    };
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h1 {
  /* Use a different font, and larger lettring */
  font-family: 'Courier New', Courier, monospace;
  font-size: 2em;
  /* Add a border to the bottom of the heading */
  border-bottom: 1px solid #333;
  /* Add some margin to the bottom of the heading */
  margin: 20px 0 50px 0;
}
h3 {
  margin: 40px 0 0;
}
label, input {
  margin: 20px 10px;
}
</style>
