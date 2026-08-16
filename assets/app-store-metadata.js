(() => {
  const script = document.currentScript;
  if (!script) {
    return;
  }

  const metadataUrl = new URL("app-store-metadata.json", script.src);
  const dateFormatter = new Intl.DateTimeFormat("en-US", {
    month: "long",
    day: "numeric",
    year: "numeric",
    timeZone: "UTC"
  });

  function formatDate(value) {
    if (!value) {
      return "";
    }

    const date = new Date(value);
    if (Number.isNaN(date.getTime())) {
      return "";
    }

    return dateFormatter.format(date);
  }

  function fieldValue(app, field) {
    switch (field) {
      case "currentVersionReleaseDateFormatted":
        return formatDate(app.currentVersionReleaseDate);
      case "minimumOsVersion":
        return app.minimumOsVersion ? `iOS ${app.minimumOsVersion} or later` : "";
      default:
        return app[field] ?? "";
    }
  }

  function hydrate(metadata) {
    const app = metadata?.app;
    if (!app) {
      return;
    }

    document.querySelectorAll("[data-app-store-field]").forEach((node) => {
      const value = fieldValue(app, node.dataset.appStoreField);
      if (value) {
        node.textContent = value;
      }
    });

    document.querySelectorAll("[data-app-store-release-notes]").forEach((node) => {
      if (app.releaseNotes) {
        node.textContent = app.releaseNotes;
      }
    });

    document.querySelectorAll("[data-app-store-link]").forEach((node) => {
      if (app.trackViewUrl) {
        node.href = app.trackViewUrl;
      }
    });
  }

  fetch(metadataUrl, { cache: "no-store" })
    .then((response) => {
      if (!response.ok) {
        throw new Error(`Metadata request failed: ${response.status}`);
      }
      return response.json();
    })
    .then(hydrate)
    .catch(() => {
      document.documentElement.classList.add("app-store-metadata-fallback");
    });
})();
