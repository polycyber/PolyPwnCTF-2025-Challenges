<template>
  <div class="hello">
    <h1>The Fast and Furryous Car catalogue</h1>
    <p>
      <i>
        Note: Car registration is closed right now, as the Torettos are busy with their next heist.
      </i>
    </p>
    <div style="display: flex; justify-content: center;" class="m-12">
      <div>
        <!-- Nice list with a little table of cars and their statistics, and a placeholder image of a car in the table. -->
        <table v-if="data">
          <thead>
          <tr>
            <th>Car</th>
            <th>Cylinders</th>
            <th>Nitro</th>
            <th>Image</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="car in data" :key="car.id">
            <td>{{ car.name }}</td>
            <td>{{ car.cylinders }}</td>
            <td>{{ car.nitro_quantity }} L</td>
            <td><img :src="imageUrl(car.image)" alt="Car image" width="200"></td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>

  </div>
</template>


<script>
import photo1 from '@/assets/images/Fast-and-Furious-Dom-Dodge-Charger-RT.avif'
import photo2 from '@/assets/images/2-Fast-2-Furious-Brian-OConner-Nissan-Skyliner-1.avif'
import photo3 from '@/assets/images/Fast-and-Furious-Dom-Chevrolet-Chevelle-SS.avif'
import photo4 from '@/assets/images/Fast-Five-Gurkha-LAPV.avif'
import photo5 from '@/assets/images/The-Fast-and-the-Furious-Acura-Integra.avif'

const car_images = {
  "car1" : photo1,
  "car2" : photo2,
  "car3" : photo3,
  "car4" : photo4,
  "car5" : photo5,
}

export default {
  name: 'MainPage',
  props: {
    msg: String
  },
  methods: {
    async fetchData() {
      const response = await fetch("http://ctf.polycyber.io:20304/cars");
      this.data = await response.json();
    },
    imageUrl(name) {
      return car_images[name]
    }
  },
  data() {
    return {
      data: null,
    };
  },
  beforeMount() {
   this.fetchData()
},
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
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
img {
  margin: 5px;
}
table {
  border-collapse: separate;
  border-spacing: 50px 0;
}

td {
  padding: 3px 0;
}
</style>
