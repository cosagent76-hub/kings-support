# Kings required updates

`app-compatibility.json` is the public, read-only minimum-version policy consumed by Kings builds that include the update requirement. It contains no player, contact, account, or game data. The initial policy is permissive and does not retire any published Kings version.

Do not raise the minimum until that exact version/build is available for users to download from the App Store. App Review approval alone is not proof of availability. Publish the required update without a phased rollout, verify its availability, then raise the policy as part of the approved release.

Each policy change must increase `revision`, including a rollback. `minimumBuild` applies only when the installed marketing version equals `minimumVersion`; a newer marketing version is supported even if its build numbering starts lower. Keep `schemaVersion` at 1. All four fields are required.

Kings checks on launch, foregrounding, and every five minutes while active. Incompatible builds show Update Required and cannot use the normal screens or CloudKit operations. A remembered update requirement survives an offline restart. A previously verified compatible build can still play offline; a first launch without a valid prior check requires connectivity. The policy uses HTTPS, does not follow redirects, and is cached locally so a failed check cannot clear a known requirement. A stale revision cannot overwrite a newer local policy.

Installed builds without the update-check code cannot enforce this policy. The first adoption of the feature requires updating those devices normally. This is client enforcement, not a server-side block on historical clients or a promise to detect a new requirement while offline.

Before raising the floor, verify the public JSON returns HTTP 200 with the intended revision and run the release candidate's update-required, cached-offline, and compatible-version checks. For an accidental floor change, publish the corrected floor with a higher revision; users can choose Check Again or reopen Kings online.
