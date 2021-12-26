<template>
    <article class="prose-sm block my-5">
        <VueShowdown :markdown="value" />
    </article>
</template>

<script>
export default {
    name: "MarkdownDisplay",
    props: {
        id: String,
        name: String,
        value: String,
    },
    methods: {},
    computed: {},
};
</script>

<style scoped></style>
