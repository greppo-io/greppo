<template>
    <div id="app">
        <base-container />
    </div>
</template>

<script>
import { mapActions } from "vuex";
import BaseContainer from "./components/BaseContainer.vue";
import "./assets/tailwind.css";

export default {
    name: "App",
    components: {
        BaseContainer,
    },
    methods: {        
        ...mapActions(["getAPI"]),
    },
    created() {
        this.getAPI();        
    },
};
</script>

<style></style>
