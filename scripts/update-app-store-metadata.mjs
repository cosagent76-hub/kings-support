#!/usr/bin/env node

import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const appId = "6791298125";
const country = "us";
const lookupUrl = `https://itunes.apple.com/lookup?id=${appId}&country=${country}`;

const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(scriptDir, "..");
const outputPath = path.join(repoRoot, "assets", "app-store-metadata.json");

function requiredString(value, fallback = "") {
  return typeof value === "string" && value.trim() ? value.trim() : fallback;
}

async function main() {
  const response = await fetch(lookupUrl, {
    headers: {
      Accept: "application/json"
    }
  });

  if (!response.ok) {
    throw new Error(`Apple lookup failed: ${response.status} ${response.statusText}`);
  }

  const payload = await response.json();
  const app = payload?.results?.[0];

  if (payload?.resultCount !== 1 || !app) {
    throw new Error(`Apple lookup returned ${payload?.resultCount ?? 0} results for app id ${appId}`);
  }

  const metadata = {
    source: lookupUrl,
    fetchedAt: new Date().toISOString(),
    app: {
      trackId: app.trackId,
      trackName: requiredString(app.trackName, "Kings Card Game Scoring"),
      version: requiredString(app.version),
      currentVersionReleaseDate: requiredString(app.currentVersionReleaseDate),
      releaseDate: requiredString(app.releaseDate),
      formattedPrice: requiredString(app.formattedPrice, "Free"),
      trackContentRating: requiredString(app.trackContentRating, app.contentAdvisoryRating),
      minimumOsVersion: requiredString(app.minimumOsVersion),
      artistName: requiredString(app.artistName),
      sellerName: requiredString(app.sellerName, app.artistName),
      bundleId: requiredString(app.bundleId),
      trackViewUrl: requiredString(app.trackViewUrl, "https://apps.apple.com/us/app/kings-card-game-scoring/id6791298125"),
      sellerUrl: requiredString(app.sellerUrl, "https://cosagent76-hub.github.io/kings-support/"),
      releaseNotes: requiredString(app.releaseNotes)
    }
  };

  await mkdir(path.dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${JSON.stringify(metadata, null, 2)}\n`);
  console.log(`Updated ${path.relative(repoRoot, outputPath)} from Apple public lookup.`);
  console.log(`Kings App Store version: ${metadata.app.version || "unknown"}`);
}

main().catch((error) => {
  console.error(error.message);
  process.exitCode = 1;
});
