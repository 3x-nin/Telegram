# PROGRESS

Branch: `myclient/ios-reskin`, from `master` (upstream Telegram for Android 12.10.5).
Last update: 2026-09-26.

## Status by step

| Step | Status |
|---|---|
| 0. Setup | Partly done. api_id/api_hash come from local.properties through BuildConfig. Services that only work for the official app are off. Pending: app name and applicationId, Firebase config for the new package, contacts account type, original launcher and notification icons, disclosure text, server-string guard for the app name. |
| 1. Analysis | Done: `DESIGN_SPEC.md` (draft for review). |
| 2. UI changes | Not started. |
| 3. Chat ID | Done in code. Build check running. |
| 4. Verify | arm64 debug build running in CI. Compliance pass pending. |

## Changed files

| Commit | File | Why |
|---|---|---|
| `a4263de` | `.github/workflows/myclient-apply-edits.yml` | Applies queued edits as separate commits, then runs the build. |
| `a4263de` | `.github/workflows/myclient-build.yml` | arm64-v8a debug build to check that the project compiles. No real credentials. |
| `a4263de` | `myclient/tools/apply_edits.py` | Anchored edit applier. Whole-file rewrites are not practical for the large upstream files. |
| `a4263de` | `myclient/edits/README.md`, `myclient/README.md` | Edit format; overview of the fork layer and local build steps. |
| `0eb1b57` | `DESIGN_SPEC.md` | iOS values with file:line sources, Android file map, gaps. |
| `ad8436f` | `TMessagesProj/build.gradle` | Opt-in `-PmyclientAbi=<abi>` to build native code for one ABI (CI speed). |
| `3f075d5` | `TMessagesProj/build.gradle` | BuildConfig fields `MYCLIENT_API_ID` / `MYCLIENT_API_HASH` from local.properties or environment; warning when missing. |
| `3f075d5` | `TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java` | `APP_ID` / `APP_HASH` read from BuildConfig. Upstream values removed. |
| `3f075d5` | `local.properties.example` | Keys to copy into the git-ignored local.properties. |
| `c24f723` | `BuildVars.java` | `CHECK_UPDATES=false`, `SUPPORTS_PASSKEYS=false`, `SAFETYNET_KEY=""`, `PLAYSTORE_APP_URL` points to this fork's releases. |
| `bdf9f61` | `TMessagesProj/src/main/java/org/telegram/myclient/ChatIdHelper.java` | Bot API id format and copy-to-clipboard. |
| `bdf9f61` | `TMessagesProj/src/main/res/values/strings.xml` | `MyClientChatId`, `MyClientChatIdCopied`. |
| `bdf9f61` | `TMessagesProj/src/main/java/org/telegram/ui/ProfileActivity.java` | Chat ID row: field, reset, row index (user, topic and chat branches), view type, bind, tap-to-copy, diff position. |

The `myclient/edits/*.edit` files from the queue commit `e60f244` are removed again by the commits that apply them.

## Not changed on purpose

- tgnet/MTProto, encryption and secret-chat code: untouched.
- `GOOGLE_AUTH_CLIENT_ID`, `getSmsHash()`, Huawei fields: left as upstream. Google sign-in and SMS auto-fill need your own values for a new package.

## Open items and risks

- **Credentials:** `2040` / `b18441...` are Telegram Desktop's official api_id and api_hash. Telegram's API terms (rule 2.1) require your own from https://my.telegram.org/apps. Put them in local.properties only.
- **App name:** "itelegram" contains "Telegram", which conflicts with API terms rule 2.3 and with the Step 4 check. Decision pending.
- **Push notifications:** `google-services.json` only lists Telegram's own Firebase apps. A new applicationId needs a matching config to build, and Telegram's servers most likely send FCM pushes only through Telegram's own Firebase project. Expect to rely on the background connection setting.
- **App name inside the app:** server language packs can still return "Telegram" for `AppName`. A small guard in `LocaleController` is planned.
- **Chat ID:** secret chats show the other user's id (the Bot API has no secret chats). The label is "Chat ID" for every peer type. Only English text exists; other languages should fall back to English (to verify). Tap copies; the long-press menu is unchanged.
- **Build coverage:** CI builds arm64-v8a only. Other ABIs are not checked.
- **Not readable:** `ChatActivity.java`, `ChatMessageCell.java` and `PhotoViewer.java` are too large for code search. Bubble tail and padding, timestamp and reply layout, and the media viewer cannot be matched to iOS for now.
- **Design gaps:** see `DESIGN_SPEC.md`, section 14.
