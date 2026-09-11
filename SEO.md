# SEO Specification

## Scope

The hackathon problem explicitly mentions SEO, so SEO is a first-class delivery requirement.

## Pages

At minimum provide meaningful metadata for:
- landing page
- product/workspace entry page if indexable
- any public informational page

Authenticated/private project workspaces do not need to be made indexable.

## Metadata

Every public page should have:
- unique title
- unique meta description
- canonical URL where appropriate
- Open Graph title/description/image
- appropriate robots directives

## Structure

Use:
- semantic `header`
- `nav`
- `main`
- `section`
- `footer`
- meaningful heading hierarchy

Use one primary H1 per public page unless a strong structural reason exists.

## Images

Provide descriptive alt text for meaningful imagery.

Decorative images should not create noisy alternative text.

## Crawlability

Provide:
- `robots.txt`
- `sitemap.xml`

Do not accidentally block the public landing page.

## Structured data

Use structured data only when it genuinely describes visible page content.

Do not add fake organization/product/review markup.

## Performance

SEO and performance are linked.

Check:
- image sizes
- layout shift
- script weight
- lazy loading where appropriate
- unnecessary dependencies

## Verification

Run Lighthouse or equivalent checks before submission.

SEO must be verified on the production deployment, not just localhost.
