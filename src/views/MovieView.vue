<script setup>
import { ref, onMounted } from "vue";
let movies = ref([]);

function fetchMovies() {
  fetch("/api/v1/movies")
    .then((response) => response.json())
    .then((data) => {
      movies.value = data.movies;
    });
}

onMounted(() => {
  fetchMovies();
});
</script>

<template>
  <div>
    <h1>Movies</h1>
    <ul
      style="
        display: flex;
        flex-wrap: wrap;
        list-style-type: none;
        padding: 0;
        justify-content: space-around;
      "
    >
      <li
        v-for="movie in movies"
        :key="movie.id"
        style="flex-basis: 45%; margin: 10px"
      >
        <div
          style="
            display: flex;
            flex-direction: row;
            align-items: flex-start;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
          "
        >
          <img
            :src="movie.poster"
            :alt="movie.title"
            style="width: 100px; height: auto; margin-right: 10px;"
          />
          <div style="flex: 1;">
            <h3 style="font-weight: bold; margin: 0 0 5px 0;">
              {{ movie.title }}
            </h3>
            <p style="margin: 0;">{{ movie.description }}</p>
          </div>
        </div>
      </li>
    </ul>
    <MovieForm @movie-added="fetchMovies" />
  </div>
</template>
