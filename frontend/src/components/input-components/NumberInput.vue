<template>
    <label class="block my-5">
        <span class="text-gray-700">{{ name }}</span>
        <input
            type="number"
            class="form-input mt-1 block w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
            v-model="modelValue"
        />
    </label>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
    name: "NumberInput",
    props: {
        id: String,
        name: String,
    },
    methods: {
        ...mapActions(["setInputComponentData"]),
    },
    computed: {
        ...mapGetters(["getInputComponentData"]),
        modelValue: {
            get() {
                return this.getInputComponentData(this.id).value;
            },
            set(newValue) {
                this.setInputComponentData({ id: this.id, value: newValue });
            },
        },        
    },
};
</script>

<style scoped>
input::-webkit-outer-spin-button,
input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

input[type="number"] {
    -moz-appearance: textfield;
}
</style>
