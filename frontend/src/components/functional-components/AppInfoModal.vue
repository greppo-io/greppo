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
                    <div v-if="getAppInfo.description">
                        <VueShowdown
                            :markdown="getAppInfo.description"
                            class="block markdown-section"
                        />
                    </div>
                    <div v-else>
                        <p>A geospatial data app built using Greppo.</p>
                        <p>For information on using greppo, visit: greppo.io</p>
                    </div>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    <p>Lorem ipsum dolor sit, amet consectetur adipisicing elit. Asperiores cum dolore magni porro voluptates similique tenetur debitis, commodi quae, itaque nam dolorem quaerat soluta alias ab corrupti libero animi ex.</p>
                    
                </div>

                <!-- <div
                    class="pt-2 pb-1.5 pr-3 flex justify-end items-center w-full"
                >
                    <button
                        type="button"
                        @click="closeModal"
                        class="py-1.5 px-4 font-semibold border border-black rounded hover:bg-black hover:text-white"
                    >
                        Close
                    </button>
                </div> -->
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
