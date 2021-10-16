<template>
    <label class="block my-5">
        <span class="text-gray-700">{{ name }}</span>
        <select
            class="form-select block w-full mt-1 rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
            v-model="modelValue"
        >
            <option
                v-for="(option, index) in options"
                :key="index"
                :value="option"
                >{{ option }}</option
            >
        </select>
    </label>
</template>

<script>
import { mapGetters, mapActions } from "vuex";

export default {
    name: "SelectInput",
    props: {
        id: String,
        name: String,
        options: Array,
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

<style></style>
