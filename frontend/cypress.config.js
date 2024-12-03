import { defineConfig } from "cypress";

export default defineConfig({
  projectId: "r6s82d",

  e2e: {
    // Production URL https://event-reservation-isp.vercel.app/
    // Local Host URL http://localhost:5173/
    baseUrl: "https://event-reservation-isp.vercel.app/",
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