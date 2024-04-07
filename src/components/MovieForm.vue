<template>
    <form @submit.prevent = "saveMovie" id="movieForm" class = "movie-form">
        <div class="form-group mb-3">
            <label for="title" class="form-label">Movie Title</label>
            <input v-model="mData.title" type="text" id="title" name="title" class="form-control"/>
        </div>

        <div class="form-group mb-3">
            <label for="description" class="form-label">Description</label>
            <input v-model="mData.description" id="description" name="description" class="form-control"/>
        </div>

        <div class="form-group mb-3">
            <label for="poster" class="form-label">Movie Poster</label>
            <input type="file" @change="onFileChange" id="poster" name="poster" class="form-control" accept="image/*"/>
        </div>

        <button type="submit" class="btn btn-primary">Save Movie</button>
    </form>
</template>

<script setup>
import { ref, onMounted } from "vue";

let csrf_token = ref("");

function getCsrfToken(){
    fetch("/api/v1/csrf-token")
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        csrf_token.value = data.csrf_token;
    });
}

const mData = ref({
    title:'',
    description:'',
    poster:null,
});

onMounted(() => {
    getCsrfToken();
});

function saveMovie() {
    let movieForm = document.getElementById('movieForm');
    let form_data = new FormData(movieForm);

    fetch("/api/v1/movies", {
        method: 'POST',
        body: form_data,
        headers: {
            'X-CSRFToken': csrf_token.value
        }
    })
    .then(function (response){
        return response.json();
    })
    .then(function (data) {
        console.log(data);
    })
    .catch(function (error){
        console.log(error)
        });
};
</script>

<style scoped>
.movie-form{
    width: 1100px;
    margin: 50px;
}
</style>