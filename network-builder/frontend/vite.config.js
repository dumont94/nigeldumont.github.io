import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/nigeldumont.github.io/network-builder/app/",
  server: {
    port: 5173,
  },
});
