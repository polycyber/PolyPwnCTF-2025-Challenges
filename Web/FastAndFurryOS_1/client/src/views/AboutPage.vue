<template>
  <div class="flex flex-row items-center justify-center">
    <div class="text w-1/2">
      <h3>About us</h3>
      <p>
        <b>Welcome to the Torettos' dashboard for car inventory and heist plans.</b>
        <br>
        There was a recent change in branding and... "management".
        Everything was totally approved by Dom. Totally! >.<
      </p>
      <p>
        Meet the new team developping the Fast and FurryOS web app, its FastAPI backend, and discover all the advantages you will have access to by using this app.
      </p>
    </div>
  </div>

  <div class="flex flex-row items-center justify-center">
  <!-- <div class="text"> -->
    <div class="text w-1/2">
      <h3>Our history</h3>
      <p>
        The history of Fast and FurryOS is still in the making!
        <br> What you see is a prototype of the dashboard we are building for Dom and his crew, but there will be more in the future.
      </p>
    </div>
  </div>

  <div class="flex flex-row items-center justify-center mb-8">
    <div>
        <h3>What we offer →</h3>
        <div class="carousel carousel-center bg-neutral rounded-box max-w-md space-x-4 p-4">
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p class="">The best app on the market.</p>
              <img
              src="@/assets/stock_image_person_0.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>The fast-est API of FastAPIs!</p>
              <img
              src="@/assets/stock_image_person_1.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>The furious-est OS of the tech world!</p>
              <img
              src="@/assets/stock_image_person_2.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>The greatest backend of backends!</p>
              <img
              src="@/assets/stock_image_person_3.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>No bugs at all!!</p>
              <img
              src="@/assets/stock_image_person_4.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>(Please check our bug bounties)</p>
              <img
              src="@/assets/stock_image_person_5.png"
              class="rounded-box" />
            </div>
          </div>  <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>(They're coming soon-ish)</p>
              <img
              src="@/assets/stock_image_person_6.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>anyways-</p>
              <img
              src="@/assets/stock_image_person_7.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>The best app on the black market!</p>
              <img
              src="@/assets/stock_image_person_8.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>The adjective-est thing of things!</p>
              <img
              src="@/assets/stock_image_person_9.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
            <div class="rounded-box p-4 bg-accent">
              <p>The superlative noun of nouns!</p>
              <img
              src="@/assets/stock_image_person_10.png"
              class="rounded-box" />
            </div>
          </div>
          <div class="carousel-item">
          <div class="rounded-box p-4 bg-accent">
            <p>The!</p>
            <img
            src="@/assets/stock_image_person_11.png"
            class="rounded-box" />
          </div>
        </div>
      
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AboutPage',
  props: {
    msg: String
  },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  font-family: 'Courier New', Courier, monospace;
  font-size: 1.8em;
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
p {
  margin: 20px;
}
div.text {
   word-wrap: break-word;
}
</style>
