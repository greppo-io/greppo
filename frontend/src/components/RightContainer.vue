<template>
    <div class="flex relative" v-if="false">
        <!-- Right Side Bar Control -->
        <div
            @click="toggleRightContainer"
            class="sidebar-control h-10 w-10 bg-white absolute mt-2 -ml-10 flex items-center rounded-tl rounded-bl justify-center cursor-pointer"
        >
            <unicon name="analytics" fill="black"></unicon>
        </div>

        <div
            class="flex flex-col w-96 h-screen sidebar"
            v-show="rightContainerOpen"
        >
            <div class="p-3 pt-16 bg-white h-full overflow-auto">
                <!-- Right Side Bar Content  -->
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex";
import { eventHub } from "src/event-hub";

export default {
    name: "RightContainer",
    components: {},
    data() {
        return {
            rightContainerOpen: false,
        };
    },
    methods: {
        toggleRightContainer() {
            this.rightContainerOpen = !this.rightContainerOpen;
            if (this.getComponentStatus.mapComponent) {
                eventHub.$emit("resetMapContainerSize");
            }
        },
    },
    computed: mapGetters(["getComponentStatus"]),
};
</script>

<style scoped>
.sidebar,
.sidebar-control {
    z-index: 1100;
}
.sidebar-width {
    width: 33vw;
    min-width: 340px;
}
</style>

