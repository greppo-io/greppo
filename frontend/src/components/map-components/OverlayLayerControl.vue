<template>
    <div
        class="bg-gray-100 text-black px-4 py-2 border-l-4 my-1"
        :class="layerData.visible ? 'border-active' : 'border-gray-400'"
        :style="cssVars"
    >
        <div class="flex">
            <div class="flex-grow">
                <p class="text-lg">{{ layerData.title }}</p>
            </div>
            <div class="flex-none mt-2 pl-4">                
                <toggle-button
                    v-model="modelValue"
                    :color="this.layerData.color"
                    :labels="{ checked: 'On', unchecked: 'Off' }"                    
                />
            </div>
        </div>
        <p class="text-sm my-2">{{ layerData.description }}</p>
    </div>
</template>

<script>
import { mapActions } from "vuex";

export default {
    name: "OverlayLayerControl",
    props: {
        layerData: Object,
    },    
    data() {
        return {
            visible: false,
        };
    },
    methods: {
        ...mapActions(["setOverlayLayerVisibility"]),      
    },    
    computed: {
        cssVars() {
            return {
                "--border-color": this.layerData.color,
            };
        },
        modelValue: {
            get() {
                return this.layerData.visible;
            },
            set(newValue) {
                this.setOverlayLayerVisibility({
                    id: this.layerData.id,
                    visible: newValue,
                });
            },
        },
    },
};
</script>

<style scoped>
.border-active {
    border-color: var(--border-color);
}
</style>
