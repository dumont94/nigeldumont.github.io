import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Proxy /api/* calls to the Flask backend during development.
// This avoids CORS preflight issues when React (port 5173) calls Flask (port 5000).
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});
