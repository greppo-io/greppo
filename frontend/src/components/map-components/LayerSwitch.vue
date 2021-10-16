<template>
    <div class="flex justify-center items-center" :style="cssVars">
        <div
            class="relative rounded-full w-10 h-5 transition duration-200 ease-linear"
            :class="toggleValue ? 'bg-active' : 'bg-gray-400'"
        >
            <label
                for="toggle"
                class="absolute left-0 bg-white border-2 w-5 h-5 rounded-full transition transform duration-100 ease-linear cursor-pointer"
                :class="
                    toggleValue
                        ? 'translate-x-full border-active'
                        : 'translate-x-0 border-gray-400'
                "
            ></label>
            <input
                type="checkbox"
                id="layerID"
                name="toggle"
                class="appearance-none w-full h-full active:outline-none focus:outline-none cursor-pointer"
                @click="handleToggle"
            />
        </div>
    </div>
</template>

<script>
export default {
    name: "LayerSwitch",
    props: {
        layerID: String,
        layerColor: {
            type: String,
            default: "#CCCCCC",
        },
        initialValue: {
            type: Boolean,
            default: false,
        },
    },
    data() {
        return {
            toggleValue: false,
        };
    },
    methods: {
        handleToggle() {
            if (this.toggleValue) {
                this.toggleValue = false;
            } else {
                this.toggleValue = true;
            }
            this.$emit("toggleValue", this.toggleValue);
        },
    },
    computed: {
        cssVars() {
            return {
                "--border-color": this.layerColor,
                "--bg-color": this.layerColor,
            }
        }
    },
    created() {
        this.toggleValue = this.initialValue;
    },
};
</script>

<style scoped>
.border-active {
    border-color: var(--border-color);
}
.bg-active {
    background-color: var(--bg-color);
}
</style>
