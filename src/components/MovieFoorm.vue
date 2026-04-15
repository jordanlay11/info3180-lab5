<template>
  <div class="form-group mb-3">
    <div v-if="successMessage" class="alert alert-success mt-3">
      {{ successMessage }}
    </div>
    <div v-if="errorMessages.length" class="alert alert-danger mt-3">
      <ul class="mb-0">
        <li v-for="error in errorMessages" :key="error">{{ error }}</li>
      </ul>
    </div>
    <form id="movieForm" @submit.prevent="saveMovie">
      <div>
        <label for="title" class="form-label">Title:</label>
        <input
          type="text"
          id="title"
          name="title"
          v-model="title"
          required
          class="form-control"
        />
      </div>
      <div>
        <label for="description" class="form-label">Description:</label>
        <input
          type="text"
          id="description"
          name="description"
          v-model="description"
          required
          class="form-control"
        />
      </div>
      <div>
        <label for="poster" class="form-label">Poster:</label>
        <input
          type="file"
          id="poster"
          name="poster"
          @change="handlePoster"
          required
          class="form-control"
        />
      </div>
      <button type="submit">Add Movie</button>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");
const title = ref("");
const description = ref("");
const poster = ref(null);
const successMessage = ref("");
const errorMessages = ref([]);

onMounted(() => {
  getCsrfToken();
});

function getCsrfToken() {
  fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    });
}

const handlePoster = (event) => {
  poster.value = event.target.files[0];
};

const saveMovie = () => {
  successMessage.value = "";
  errorMessages.value = [];

  let movieForm = document.getElementById("movieForm");
  let form_data = new FormData(movieForm);

  fetch("/api/v1/movies", {
    method: "POST",
    body: form_data,
    headers: { "X-CSRFToken": csrf_token.value },
  })
    .then(function (response) {
      return response.json().then(function (data) {
        if (response.ok) {
          successMessage.value = "Movie added successfully!";
          title.value = "";
          description.value = "";
          poster.value = null;
          movieForm.reset();
        } else {
          errorMessages.value = data.form_errors || ["An error occurred."];
        }
      });
    })
    .catch(function (error) {
      errorMessages.value = ["Network error: " + error.message];
    });
};
</script>
