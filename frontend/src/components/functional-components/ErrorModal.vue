<template>
    <div
        class="modal-screen fixed top-0 left-0 w-screen h-screen bg-gray-900 bg-opacity-30"
    >
        <div
            class="bg-white flex rounded w-3/4 md:w-1/2 relative mx-auto mt-10"
            style="max-height: calc(90% - 2.5rem)"
        >
            <div class="flex flex-col items-start py-3 px-5">
                <div
                    class="py-3 px-1 flex justify-between items-center w-full text-gray-900 font-medium text-2xl"
                >
                    <p>{{ getErrorInfo.title }}</p>
                </div>

                <div class="py-3 pl-3 pr-4 p overflow-x-hidden overflow-y-auto">
                    <VueShowdown
                        :markdown="getErrorInfo.message"
                        class="prose"
                    />
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
    name: "ErrorModal",
    computed: {
        ...mapGetters(["getErrorInfo"]),
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
