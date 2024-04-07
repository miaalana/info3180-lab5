<template>
    <form @submit.prevent = "saveMovie" id="movieForm" class = "movie-form">

        <div v-if="sMessage" class="alert success">{{ sMessage }}</div>

        <div v-if="eMessage.length > 0" class="alert error">
        <ul>
        <li v-for="error in eMessage" :key="error">{{ error }}</li>
        </ul>
        </div>

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

const sMessage = ref('');
const eMessage = ref([]);

function clearMessages(){
    sMessage.value='';
    eMessage.value=[];
}

onMounted(() => {
    getCsrfToken();
});

function saveMovie() {
    eMessage.value = [];

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
        if (response.ok) {
            sMessage.value = 'File Uploaded Successfully';
            mData.value = { title:'', description:'', poster:null };
            movieForm.reset(); 
        }
        else{
            if(!mData.value.title){
                eMessage.value.push("Error in Title field - This field is required.");
            }

            if(!mData.value.description){
                eMessage.value.push("Error in the Description field - This field is required.");
            }

            if(!mData.value.poster){
                eMessage.value.push("Error in the Photo field - This field is required.");
            }
        }
    })
    .then(function (data) { 
        console.log(data);       
    })
    .catch(function (error){
        console.error(error);
        eMessage.value = ['Error Occurred'];
    });
};

function onFileChange(event){
    const file = event.target.files[0];
    if (file){
        mData.value.poster = file;
    }
}

</script>

<style scoped>
.movie-form{
    width: 1100px;
    margin: 50px;
}

.alert{
    margin-top:10px;
    padding:10px;
}

.success{
    background-color: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
}

.error{
    background-color: #f8d7da;
    border-color: #f5c6cb;
    color: #721c24;
}
</style>