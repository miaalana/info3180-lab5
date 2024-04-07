<template>
<div>
<h1>Upload Form</h1>
<movie-form></movie-form>
</div>
</template>

<script setup>
import { defineComponent } from 'vue';
import MovieForm from '@/components/MovieForm.vue';

defineComponent({
components:{
    MovieForm,
},
});
</script>

<style scoped>
h1{
    margin: 50px;
}
</style>