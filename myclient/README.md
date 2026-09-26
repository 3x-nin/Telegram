# myclient: unofficial client layer

This branch builds an unofficial Android client based on the open-source
Telegram for Android app. It is not affiliated with or endorsed by Telegram.

Fork-specific code and tools live in clearly named places, to keep upstream
merges simple:

| Path | Purpose |
|---|---|
| `myclient/tools/apply_edits.py` | Applies queued anchored edits (see `myclient/edits/README.md`). |
| `myclient/edits/` | Queue of small edits to large upstream files. Empty when all edits are applied. |
| `.github/workflows/myclient-*.yml` | Edit applier and arm64 debug build. |
| `TMessagesProj/src/main/java/org/telegram/myclient/` | Fork-only Java code. |
| `DESIGN_SPEC.md` | iOS design values and the Android file map. |
| `PROGRESS.md` | Every changed file and why, plus open gaps. |

## Build locally

1. `git clone --recursive --shallow-submodules <repo-url>` and check out this branch.
2. Copy the keys from `local.properties.example` into `local.properties` and fill in
   your own api_id and api_hash from https://my.telegram.org/apps.
3. Open the project in Android Studio and build `TMessagesProj_App` (afat debug).
