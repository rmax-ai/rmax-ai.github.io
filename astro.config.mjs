import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://rmax.ai',
  output: 'static',
  integrations: [sitemap()],
});
