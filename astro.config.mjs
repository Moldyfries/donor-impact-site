// Astro configuration for the Riverside Commons donor-impact page.
// Kept deliberately small: this is a single static page, so there is nothing to configure
// beyond telling Astro where the site will live once it is deployed.
import { defineConfig } from 'astro/config';

export default defineConfig({
  // Everything is prerendered to plain HTML at build time, which is what the free host serves.
  output: 'static',
});
