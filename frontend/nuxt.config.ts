// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  runtimeConfig: {
      public: {

        BACKEND_URL: process.env.BACKEND_URL,
        DAEMON_URL: process.env.DAEMON_URL
      }
  },
  devtools: { enabled: true },
  modules: ["@nuxt/ui", "@nuxt/fonts", "@pinia/nuxt"],
  compatibilityDate: "2024-09-12",
  colorMode: {
    preference: 'dark'
  },
  fonts: {
    families: [
      {
        name: 'IBM Plex Mono', provider:'google'
      }
    ]
  },
  ssr: false
})