<template>
    <multipane class="w-full h-screen" layout="vertical">
        <div
            class="p-5 border-r-2 w-96"
            :style="{ minWidth: '300px', maxWidth: '500px'}"
        >
            <div>
                <h6 class="title is-6">Pane 1</h6>
                <p class="subtitle is-6">Fixed width.</p>                
            </div>
        </div>
        <multipane-resizer></multipane-resizer>
        <div class="flex-grow p-5">
            <div>
                <h6 class="title is-6">Pane 3</h6>
                <p class="subtitle is-6">Takes remaining available space.</p>                
            </div>
        </div>
    </multipane>
</template>

<script>
import { Multipane, MultipaneResizer } from "vue-multipane";

export default {
    components: {
        Multipane,
        MultipaneResizer,
    },
};
</script>

<style>

</style>
