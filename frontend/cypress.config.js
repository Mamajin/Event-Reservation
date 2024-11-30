import { defineConfig } from "cypress";

export default defineConfig({
  e2e: {
<<<<<<< HEAD
    baseUrl: "https://event-reservation-isp.vercel.app/",
=======
    // Production URL https://event-reservation-isp.vercel.app/
    // Local Host URL http://localhost:5173/
    baseUrl: "http://localhost:5173/",
>>>>>>> ebfa4ac01bfc5364ba13385dd7b3c3f937c03a18
    defaultCommandTimeout: 10000,
    viewportWidth: 1280,
    viewportHeight: 720,
    waitForInitialPage: true,
    retries: {
      runMode: 2,
      openMode: 1
    }
  },
  setupNodeEvents(on, config) {
    // implement node event listeners here
  },
});