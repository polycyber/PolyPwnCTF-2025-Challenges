<template>
    <div class="bottom bg-base-100">
        <div class="flex-1">
          <p>
            Backend powered by FastAPI (under development). Frontend powered by Vue.js.
          </p>
        </div>
        <div class="flex-none gap-0.5">
              <!-- <div class="w-40 rounded-full">
                <img
                  alt="Tailwind CSS Navbar component"
                  src="@/assets/chev_camaro.png" />
              </div> -->
        </div>
      </div>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>

<style scoped>
div.bottom {
  /* Use a different font, and larger lettring */
  font-family: 'Courier New', Courier, monospace;
  /* font-size: 2em; */
  /* Add a border to the bottom of the heading */
  border-top: 1px solid #888;
  position: relative;
  padding: 15px;
  z-index: 100; 
  bottom: 0; 
  left: 0;
  width: 100%;
}
</style>