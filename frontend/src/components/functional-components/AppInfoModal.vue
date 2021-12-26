<template>
    <div
        class="modal-screen fixed top-0 left-0 w-screen h-screen bg-gray-900 bg-opacity-30"
    >
        <div
            class="bg-white flex rounded w-3/4 md:w-1/2 relative mx-auto mt-10"
            style="max-height: calc(90% - 2.5rem);"
        >
            <div class="flex flex-col items-start py-3 px-5">
                <button
                    type="button"
                    class="absolute top-3 right-3 w-5 h-5 cursor-pointer"
                    @click="closeModal"
                >
                    <unicon name="multiply" fill="black" width="20px"></unicon>
                </button>

                <div
                    class="py-3 px-1 flex justify-between items-center w-full text-gray-900 font-medium text-2xl"
                >
                    <p v-if="getAppInfo.title">{{ getAppInfo.title }}</p>
                    <p v-else>A geospatial app</p>
                </div>

                <div class="py-3 pl-3 pr-4 p overflow-x-hidden overflow-y-auto">
                    <VueShowdown :markdown="getAppDescription" class="prose" />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
    name: "AppInfoModal",
    methods: {
        ...mapActions(["setAppInfo"]),
        closeModal() {
            this.setAppInfo({ modal: false });
        },
    },
    computed: {
        ...mapGetters(["getAppInfo"]),
        getAppDescription() {
            if (this.getAppInfo.description) {
                return this.getAppInfo.description;
            } else {
                return "## Geospatial app \n A geospatial application built using Greppo. \n For more information, check out: \n - Documentation at [docs.greppo.io](https://docs.greppo.io) \n - Website at [greppo.io](https://greppo.io) \n - GitHub repo at [github.com/greppo-io](https://github.com/greppo-io/greppo)";
            }
        },
    },
};
</script>

<style scoped>
.modal-screen {
    z-index: 9999;
    width: 100vw;
    height: 100vh;
}
p {
    margin: 0.5rem 0;
}
</style>
