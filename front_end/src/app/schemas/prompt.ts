import { z } from 'zod';

export const PromptSchema = z.object({
  id: z.number(),
  title: z.string().min(1),
  content: z.string().min(1),
  theme: z.enum(['marketing', 'finance', 'customer support', 'sales']),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime()
});

export type Prompt = z.infer<typeof PromptSchema>;
export type PromptArray = Prompt[];
export const PromptArraySchema = PromptSchema.array();

export const CreatePromptSchema = PromptSchema.omit({
  id: true,
  created_at: true,
  updated_at: true
});
