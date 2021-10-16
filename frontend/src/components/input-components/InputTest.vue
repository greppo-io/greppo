<template>
    <div class="grid grid-cols-1 gap-6 text-gray-900 antialiased">
        <label class="block">
            <span class="text-gray-700">Text input</span>
            <input
                type="text"
                class="form-input mt-1 block w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
                placeholder=""
            />
        </label>
        <label class="block">
            <span class="text-gray-700">Date input</span>
            <input
                type="date"
                class="form-input mt-1 block w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
            />
        </label>
        <label class="block">
            <span class="text-gray-700">Dropdown select</span>
            <select
                class="form-select block w-full mt-1 rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
            >
                <option>Corporate event</option>
                <option>Wedding</option>
                <option>Birthday</option>
                <option>Other</option>
            </select>
        </label>
        <label class="block">
            <span class="text-gray-700">Text area input</span>
            <textarea
                class="form-textarea mt-1 block w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
                rows="3"
            ></textarea>
        </label>
        <div class="block">
            <span class="text-gray-700">Check box input</span>
            <label class="inline-flex items-center">
                <input
                    type="checkbox"
                    class="form-checkbox rounded bg-gray-200 border-transparent focus:border-transparent focus:bg-gray-200 text-gray-700 focus:ring-1 focus:ring-offset-2 focus:ring-gray-500"
                />
                <span class="ml-2">Email me news and special offers</span>
            </label>
        </div>
        <!-- <label class="block">
            <span class="text-gray-700">Email address</span>
            <input
                type="email"
                class="mt-1 block w-full rounded-md bg-gray-100 border-transparent focus:border-gray-500 focus:bg-white focus:ring-0"
                placeholder="john@example.com"
            />
        </label> -->
    </div>
</template>

<script>
export default {
    name: "AllInput",
};
</script>

<style></style>
