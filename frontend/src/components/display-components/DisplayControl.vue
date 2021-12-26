<template>
    <div>
        <markdown-display
            v-if="
                data.type == 'Display' &&
                    data.name != 'title' &&
                    data.name != 'description'
            "
            :id="data.id"
            :name="data.name"
            :value="data.value"
        />
    </div>
</template>

<script>
import MarkdownDisplay from "../display-components/MarkdownDisplay.vue";

export default {
    name: "DisplayControl",
    props: {
        data: Object,
    },
    components: { MarkdownDisplay },
};
</script>

<style></style>
