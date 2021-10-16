<template>
    <div>
        <select
            class="form-select block w-full mt-1 rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
            v-model="selectedBaseLayer"
            
        >
            <option
                v-for="base in getBaseLayerInfo"
                :key="base.id"
                :value="base.id"
                >{{ base.name }}</option
            >
        </select>
    </div>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
    name: "BaseLayerControl",    
    methods: {
        ...mapActions(["setBaseLayerVisibility"]),
    },
    computed: {
        ...mapGetters(["getBaseLayerInfo"]),
        selectedBaseLayer: {
            get() {
                return this.getBaseLayerInfo.find(
                    (element) => element.visible == true
                ).id;
            },
            set(newValue) {
                this.setBaseLayerVisibility(newValue);
            },
        },
    },    
};
</script>

<style></style>
