<template>
    <div class="navbar bg-base-100">
        <div class="flex-1">
            <RouterLink class="btn btn-ghost text-xl" to="/">Home</RouterLink>
            <RouterLink class="btn btn-ghost text-xl" to="/cars">Cars</RouterLink>
            <RouterLink class="btn btn-ghost text-xl" to="/about">About</RouterLink>
        </div>
        <div class="flex-none gap-0.5">
              <div class="w-40 rounded-full">
                <img
                  alt="An amazing camaro that really fits the theme of the website."
                  src="@/assets/chev_camaro.png" />
              </div>
        </div>
      </div>
</template>

<script>
export default {
  name: 'NavBar'
}
</script>
