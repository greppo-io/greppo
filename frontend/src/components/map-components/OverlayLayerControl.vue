<template>
    <div
        class="bg-gray-100 text-black px-4 py-2 border-l-4 my-1"
        :class="visible ? 'border-active' : 'border-gray-400'"
        :style="cssVars"
    >
        <div class="flex">
            <div class="flex-grow">
                <p class="text-lg">{{ layerData.title }}</p>
            </div>
            <div class="flex-none mt-2 pl-4">
                <layer-switch
                    :initialValue="layerData.visible"
                    :layerID="layerData.id"
                    :layerColor="layerData.color"
                    @toggleValue="toggleValue"
                />
            </div>
        </div>
        <p class="text-sm my-2">{{ layerData.description }}</p>
    </div>
</template>

<script>
import LayerSwitch from "./LayerSwitch";
import { mapActions } from "vuex";

export default {
    name: "OverlayLayerControl",
    props: {
        layerData: Object,
    },
    components: {
        LayerSwitch,
    },
    data() {
        return {
            visible: false,
        };
    },
    methods: {
        ...mapActions(["setOverlayLayerVisibility"]),        
        toggleValue() {
            this.visible = !this.visible;
            this.setOverlayLayerVisibility({id:this.layerData.id, visible:this.visible})            
        },
    },
    created() {
        this.visible = this.layerData.visible;
    },
    computed: {
        cssVars() {
            return {
                "--border-color": this.layerData.color,
            };
        },
    },
};
</script>

<style scoped>
.border-active {
    border-color: var(--border-color);
}
</style>
