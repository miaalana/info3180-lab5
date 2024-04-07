<template>
<div>
    <h1>Movies</h1>
    <div class="container">
        <div v-for="movie in movies" :key="movie.id">
            <div class="mov">
            <img :src="movie.poster" alt="Movie Poster" class="mpost"/>
            <div class="details">
                <h2>{{ movie.title }}</h2>
                <br>
                <p>{{ movie.description }}</p>
            </div>
            </div>
        </div>
    </div>
</div>
</template>

<script setup>
import { ref, onMounted } from "vue";

let movies = ref([]);

function fetchMovies(){
    fetch("/api/v1/movies")
    .then(function (response){
        return response.json();
    })
    .then(function (data) { 
        movies.value = data.movies || [];
    })
    .catch(function (error){
        console.error("Error fetching movies:",error);
    });
}

onMounted(fetchMovies);
</script>

<style scoped>

h1{
    padding:50px;
}

.container{
    display:grid;
    column-gap: 20px;
    grid-template-columns: auto auto;
    gap: 40px;  
}

.mov{
    display: grid;
    grid-template-columns: auto 300px;
    column-gap: 20px;
    border: 1px solid #ccc;
    border-radius: 20px;
    width: auto;
    box-shadow: 0 0 5px rgba(0,0,0,0,1);
}

.mpost{
    width:200px;
    height: auto;
    border-radius: 5px;
}

.details{
    display: flex;
    flex-direction:column;
    margin-top:10px;
}
</style>