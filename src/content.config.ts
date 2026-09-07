import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const notes = defineCollection({
  loader: glob({ base: './notes', pattern: '*/index.md' }),
  schema: z.object({
    title: z.string(),
    slug: z.string(),
    description: z.string(),
    author: z.string().default('Max'),
    site: z.string().default('rmax.ai'),
    section: z.string().default('notes'),
    type: z.string().default('essay'),
    status: z.string().default('published'),
    date: z.coerce.date(),
    updated: z.coerce.date().optional(),
    tags: z.array(z.string()).default([]),
    reading_time: z.string().optional(),
    canonical_url: z.string().url().optional(),
    license: z.string().optional(),
  }),
});

export const collections = { notes };
