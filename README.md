# Kings Support

Public support and privacy pages for the Kings iOS app by SCIM Ventures.

Published with GitHub Pages at:

- Support: https://cosagent76-hub.github.io/kings-support/support/
- Privacy: https://cosagent76-hub.github.io/kings-support/privacy/
- How to Play: https://cosagent76-hub.github.io/kings-support/play/
- Gallery: https://cosagent76-hub.github.io/kings-support/gallery/
- Family Scorebook: https://cosagent76-hub.github.io/kings-support/family-scorebook/
- What's New: https://cosagent76-hub.github.io/kings-support/whats-new/
- App or Paper: https://cosagent76-hub.github.io/kings-support/paper/
- Age Suitability: https://cosagent76-hub.github.io/kings-support/age/
- Printable Rules: https://cosagent76-hub.github.io/kings-support/printable/
- Changelog: https://cosagent76-hub.github.io/kings-support/changelog/
- App Store: https://apps.apple.com/us/app/kings-card-game-scoring/id6791298125

This repository intentionally contains only public website content. It does not contain the Kings app source code, signing assets, App Store package, or private App Review contact information.

## App Store Metadata

The support site keeps a small public App Store metadata snapshot at `assets/app-store-metadata.json`. Refresh it from Apple's public lookup endpoint with:

```sh
node scripts/update-app-store-metadata.mjs
```

The visible pages include readable fallback text, then hydrate version, release date, price, seller, compatibility, App Store URL, and release notes from the local JSON when it loads.

## Staged App Previews

The 2026-08-15 app preview MP4 exports are staged under `assets/app-previews/staged-2026-08-15/` with version-safe notes. They are intentionally not linked from visible pages until marketing decides whether to publish them and the App Store release state is verified.
