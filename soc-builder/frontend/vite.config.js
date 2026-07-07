import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/nigeldumont.github.io/soc-builder/app/",
  build: {
    outDir: "../app",
    emptyOutDir: true,
  },
  server: {
    port: 5174,
  },
});
