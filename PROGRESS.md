# PROGRESS

Branch: `myclient/ios-reskin`, from `master` (upstream Telegram for Android 12.10.5).
App name: **istylegraph**. applicationId: **com.itelegram.unofficial** (debug: `.beta`).
Last update: 2026-09-26.

## Status by step

| Step | Status |
|---|---|
| 0. Setup | Done, with open items below. Own api_id/api_hash via local.properties and BuildConfig; new name and applicationId; placeholder Firebase config; own contacts account type; original icons and wordmark; disclosure in Settings and in the intro; app-name guard against server strings. |
| 1. Analysis | Done: `DESIGN_SPEC.md` (draft for review). |
| 2. UI changes | Not started. |
| 3. Chat ID | Done. Builds in CI. Not yet tested on a device. |
| 4. Verify | arm64 debug build passes in CI up to the Chat ID commit. Branding commits: build running. Compliance pass: see below. |

## Changed files

| Commit | File | Why |
|---|---|---|
| `a4263de`, `109fd59` | `.github/workflows/myclient-apply-edits.yml`, `.github/workflows/myclient-build.yml`, `myclient/tools/apply_edits.py`, `myclient/edits/README.md`, `myclient/README.md` | CI tooling: applies queued anchored edits as separate commits, then builds an arm64 debug APK. |
| `0eb1b57` | `DESIGN_SPEC.md` | iOS values with file:line sources, Android file map, gaps. |
| `ad8436f` | `TMessagesProj/build.gradle` | Opt-in `-PmyclientAbi=<abi>` to build native code for one ABI (CI speed). |
| `3f075d5` | `TMessagesProj/build.gradle`, `BuildVars.java`, `local.properties.example` | `APP_ID` / `APP_HASH` come from `MYCLIENT_API_ID` / `MYCLIENT_API_HASH` in the git-ignored local.properties (or environment). Upstream values removed. |
| `c24f723` | `BuildVars.java` | `CHECK_UPDATES=false`, `SUPPORTS_PASSKEYS=false`, `SAFETYNET_KEY=""`, `PLAYSTORE_APP_URL` points to this fork's releases. |
| `bdf9f61` | `myclient/ChatIdHelper.java`, `values/strings.xml`, `ProfileActivity.java` | Chat ID row with tap-to-copy (Bot API format). |
| `fc4ca8d` | `gradle.properties` | `APP_PACKAGE=com.itelegram.unofficial`. |
| `fc4ca8d` | `TMessagesProj_App/google-services.json` | Placeholder Firebase config for the new package names (no real keys). |
| `fc4ca8d` | `TMessagesProj_App/src/main/res/values/strings.xml` | `AppName` = istylegraph, `AppNameBeta` = istylegraph Beta. |
| `fc4ca8d` | `TMessagesProj/build.gradle`, `res/xml/auth.xml`, `res/xml/sync_contacts.xml`, `ContactsController.java` | Contacts sync account type = applicationId base (`MYCLIENT_ACCOUNT_TYPE`, `@string/MyClientAccountType`). |
| `fc4ca8d` | `BuildVars.java` | `isBetaApp()` checks the `.beta` suffix. |
| `d348545` | `TMessagesProj_App/src/main/res/` (mipmap-anydpi-v26, mipmap-anydpi, drawable-anydpi, drawable, values) | Original icon (speech bubble, violet): launcher and alternative launcher icons, icon-picker previews, notification icon, account icon, Android 12 splash icon, intro texture. |
| `d3a72a3` | `TMessagesProj_App/src/main/res/drawable/telegram_logo.xml`, `telegram_logo_2.xml` | "istylegraph" wordmark replaces the Telegram wordmark in the intro, chat list header and stories header. |
| `b30efeb` | `values/strings.xml`, `SettingsActivity.java`, `IntroActivity.java`, `LocaleController.java`, `myclient/MyClientStrings.java` | Disclosure under the Settings version line; intro page 1 notice; app name always from this build's resources. |

Queue commits (`e60f244`, `105c91e`) only add `myclient/edits/*.edit` files. The applying commits remove them again.

## Compliance pass (Telegram API terms and your Step 4 list)

| Item | Status |
|---|---|
| Own api_id / api_hash, not committed | Wired through local.properties. No values in the repo. You must register your own at https://my.telegram.org/apps. Do not use `2040` (Telegram Desktop). |
| App title without "Telegram" (rule 2.3) | "istylegraph". |
| No official logo (rule 2.4) | Launcher, alternative icons, notification, account, splash, intro plane and wordmarks replaced. Still open: the `plane_logo_plain` Lottie (QR code screen, round-video overlay). |
| API use shown in the intro (rule 2.2) | Intro page 1 says the app uses the Telegram API and is not affiliated with Telegram. Add the same text to any store description. |
| Disclosure in Settings | Under the version line at the bottom of Settings (there is no separate About screen). |

## Not changed on purpose

- tgnet/MTProto, encryption and secret-chat code: untouched.
- `GOOGLE_AUTH_CLIENT_ID`, `getSmsHash()`, Huawei fields: left as upstream. Google sign-in and SMS auto-fill need your own values for the new package.
- `TMessagesProj_AppHockeyApp`, `TMessagesProj_AppStandalone`, `TMessagesProj_AppHuawei`: not updated. Their google-services.json files do not know the new package, so only `TMessagesProj_App` builds.

## Open items and risks

- **Push notifications:** the Firebase config is a placeholder, so FCM token requests fail. Telegram's servers most likely send FCM pushes only through Telegram's own Firebase project, so even your own Firebase project may not receive them. Use Settings > Notifications > keep-alive service / background connection.
- **Plane animation:** `res/raw/plane_logo_plain.json` (QR code screen, round-video overlay) still shows the Telegram plane. Needs an original Lottie file.
- **Wordmark:** the "istylegraph" wordmark is a hand-drawn placeholder. Replace it with a designed asset.
- **Intro animation:** page 1 draws the chat-bubble texture where the plane was. It may look stretched; check on a device.
- **Other in-app text:** strings such as "Telegram Premium" or "Telegram FAQ" name the Telegram service and are left as they are.
- **Chat ID:** secret chats show the other user's id (the Bot API has no secret chats). The label is "Chat ID" for every peer type. Only English text exists; other languages fall back to English (to verify). Tap copies; the long-press menu is unchanged.
- **Build coverage:** CI builds arm64-v8a debug only. Release, other ABIs and other app modules are not checked.
- **Not readable:** `ChatActivity.java`, `ChatMessageCell.java` and `PhotoViewer.java` are too large for code search. Bubble tail and padding, timestamp and reply layout, and the media viewer cannot be matched to iOS for now.
- **Design gaps:** see `DESIGN_SPEC.md`, section 14.
