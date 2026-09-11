# Security Specification

## General rule

Assume all client input is untrusted.

## Secrets

Never place:
- private API keys
- service-account credentials
- database passwords
- signing secrets

in frontend source or committed files.

Use environment variables and deployment secret storage.

## Uploads

Validate:
- file type
- size
- extension/content where practical
- processing limits

Never blindly trust filename extensions.

## API

Validate request bodies.

Do not expose stack traces in production responses.

Use predictable error messages.

## Authorization

If authentication is implemented:
- verify project ownership/permissions server-side
- do not rely on hidden frontend controls
- verify edit/verify/export permissions
- do not trust user IDs supplied by the client

## Geometry security

Apply processing limits:
- maximum image dimensions/file size
- maximum feature counts where necessary
- timeouts or job limits for expensive operations

Avoid algorithms that can be trivially abused with pathological geometry/data.

## File/path safety

Never concatenate an arbitrary uploaded filename into a filesystem path.

Generate safe internal identifiers.

## CORS

Allow only the intended frontend origins in deployed environments.

## Logging

Do not log secrets.

Log:
- request IDs
- processing failures
- job IDs
- useful error context

## Prototype/demo rule

Demo credentials and sample data must never be real sensitive information.
