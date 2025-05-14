import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: true, // This is equivalent to --host in the CLI
    allowedHosts: ["5173-i7yf4le1i5j7ww9yxbfa0-3198e65d.manus.computer"],
  },
});

