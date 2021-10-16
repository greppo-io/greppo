<template>
    <div
        class="loading-screen absolute bg-gray-500 bg-opacity-50 flex items-center justify-center"
    >
        <div
            class="flex justify-center items-center space-x-1 text-sm text-black"
        >
            <svg
                fill="none"
                class="w-6 h-6 animate-spin"
                viewBox="0 0 32 32"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                    clip-rule="evenodd"
                    d="M15.165 8.53a.5.5 0 01-.404.58A7 7 0 1023 16a.5.5 0 011 0 8 8 0 11-9.416-7.874.5.5 0 01.58.404z"
                    fill="currentColor"
                    fill-rule="evenodd"
                />
            </svg>

            <div>Loading ...</div>
        </div>
    </div>
</template>

<script>
export default {
    name: "LoadingScreen",
};
</script>

<style>
.loading-screen {
    z-index: 9999;
    width: 100vw;
    height: 100vh;
}
</style>
