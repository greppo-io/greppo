module.exports = {
    purge: { content: ["./public/**/*.html", "./src/**/*.vue"] },
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            transitionProperty: {
                height: "height",
            },
            typography: {
                sm: {
                    css: {
                        code: {
                            fontSize: "1em",
                        },
                        pre: {
                            "overflow-x": "auto",
                        },
                        h2: {
                            marginTop: "1.4em",
                        },
                    },
                },
            },
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
        require("@tailwindcss/forms")({
            strategy: "class",
        }),
        require("@tailwindcss/typography"),
    ],
};
