# Prompt: Apply Schema-Compliant Frontmatter

## Objective
Generate and prepend YAML frontmatter to a markdown note using `notes/schema.yaml`.

## Inputs
- `schema_path`: `notes/schema.yaml`
- `markdown_path`: `notes/<slug>/index.md`
- `slug`: `<slug>`

## Output (STRICT)
Return a single JSON object (no surrounding prose):

```json
{
  "frontmatter": "---\n...\n---\n",
  "validated": true,
  "errors": []
}
```

## Rules
- Read and comply with every required field in `notes/schema.yaml`.
- Add **no extra fields**.
- Ensure the frontmatter `slug` exactly matches the provided `slug`.
- Ensure frontmatter precedes all markdown content.
- `title` must match the note title (from H1 if present).
- Set `status` according to schema expectations (use the appropriate published/released value if enumerated).
- If any requirement cannot be met, set `validated=false` and populate `errors`.
- Do not add any prose outside the JSON output.
