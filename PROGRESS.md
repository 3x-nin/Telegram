# PROGRESS: istylegraph (unofficial Telegram client with an iOS-style UI)

Branch: `myclient/ios-reskin`. Base: upstream DrKLO/Telegram `master` (12.10.5).
App name: **istylegraph**. Package: `com.istylegraph.app` (debug: `.beta`).
The app uses the real Telegram servers and protocol. tgnet, MTProto and encryption are not changed.

## Status

| Step | State |
|---|---|
| 0. Setup and branding | Done. |
| 1. iOS analysis | Done: `DESIGN_SPEC.md`. |
| 2. iOS-style reskin | Partly done: palettes, bubble radii, tab order, push/pop motion, nav title size, send arrow. See "Not matched". |
| 3. Chat ID | Done. Needs a device check. |
| 4. Build, ToS pass, this file | CI builds pass (see below). ToS pass below. |

## Build verification (CI, `assembleAfatDebug`, arm64-v8a, no real credentials)

Each build checks out the branch head, so a build also covers the commits before it.

| Run | Covers | Result |
|---|---|---|
| [36228232057](https://github.com/3x-nin/Telegram/actions/runs/36228232057) | Step 0 build and fork switches, Chat ID | Pass |
| [36240175849](https://github.com/3x-nin/Telegram/actions/runs/36240175849) | Branding (package, icons, wordmark, disclosure) | Pass |
| [36240337579](https://github.com/3x-nin/Telegram/actions/runs/36240337579) | Bubble corner radii | Pass |
| [36241956456](https://github.com/3x-nin/Telegram/actions/runs/36241956456) | iOS palettes, tab order | Pass |
| [36242521149](https://github.com/3x-nin/Telegram/actions/runs/36242521149) | Push/pop motion, nav titles, logo assets | Pass |
| [36249100386](https://github.com/3x-nin/Telegram/actions/runs/36249100386) | Calls-tab options, send arrow | See the run |
| [36249576169](https://github.com/3x-nin/Telegram/actions/runs/36249576169) | Package id `com.istylegraph.app` | See the run |

The APK is attached to each run as the artifact `myclient-debug-arm64`. It has no api_id, so it cannot log in. Build your own with your credentials (below).

## How to build

1. Get your own api_id and api_hash at https://my.telegram.org (API development tools). Do not use the credentials of other apps.
2. Copy `local.properties.example` to `local.properties` and set `MYCLIENT_API_ID` and `MYCLIENT_API_HASH`. The file is in `.gitignore`. Environment variables with the same names also work.
3. Run `./gradlew :TMessagesProj_App:assembleAfatDebug -PmyclientAbi=arm64-v8a`. Leave out `-PmyclientAbi` to build all ABIs.
4. For a release build, use your own keystore.
5. Push notifications need your own Firebase project. `TMessagesProj_App/google-services.json` is a placeholder.

## Changed files

Fork code is marked "Unofficial client (myclient)". New Java code is in `org.telegram.myclient`. New resources are in `TMessagesProj_App/src/main/res` when possible, so upstream files stay unchanged.

| Commit | Files | Purpose |
|---|---|---|
| a4263de, 109fd59, 48808a7 | `.github/workflows/myclient-apply-edits.yml`, `.github/workflows/myclient-build.yml`, `myclient/tools/apply_edits.py`, `myclient/edits/README.md`, `myclient/README.md` | CI: applies queued anchored edits, one commit per edit, then builds. |
| 0eb1b57 | `DESIGN_SPEC.md` | iOS design tokens with iOS source references, Android mapping, gaps. |
| ad8436f | `TMessagesProj/build.gradle` | Optional single-ABI build (`-PmyclientAbi`). |
| 3f075d5 | `TMessagesProj/build.gradle`, `TMessagesProj/src/main/java/org/telegram/messenger/BuildVars.java`, `local.properties.example` | api_id and api_hash from `local.properties` or environment. Upstream credentials removed. |
| c24f723 | `BuildVars.java` | Fork safety: no official update checks, no SafetyNet key, own releases URL, passkeys off. |
| bdf9f61 | `TMessagesProj/src/main/java/org/telegram/myclient/ChatIdHelper.java` (new), `TMessagesProj/src/main/java/org/telegram/ui/ProfileActivity.java`, `TMessagesProj/src/main/res/values/strings.xml` | Chat ID row in profiles, tap to copy. |
| fc4ca8d | `gradle.properties`, `TMessagesProj_App/google-services.json`, `TMessagesProj_App/src/main/res/values/strings.xml` (new), `TMessagesProj/build.gradle`, `TMessagesProj/src/main/res/xml/auth.xml`, `TMessagesProj/src/main/res/xml/sync_contacts.xml`, `TMessagesProj/src/main/java/org/telegram/messenger/ContactsController.java`, `BuildVars.java` | First package id (`com.itelegram.unofficial`, replaced in d10b8ee), app name, account type follows the package. |
| d348545 | `TMessagesProj_App/src/main/res/`: `values/myclient_colors.xml`, `drawable/myclient_icon_foreground.xml`, `mipmap-anydpi-v26/` and `mipmap-anydpi/` (`ic_launcher`, `ic_launcher_round`, `icon_2..6_launcher`, `icon_2..6_launcher_round`, `icon_foreground`, `icon_*_foreground_sa`), `drawable-anydpi/notification.xml`, `drawable-anydpi/ic_launcher_dr.xml`, `drawable/tg_splash_320.xml`, `drawable-anydpi/intro_tg_plane.xml` | Original launcher, notification, splash and intro icons. |
| d3a72a3 | `TMessagesProj_App/src/main/res/drawable/telegram_logo.xml`, `drawable/telegram_logo_2.xml` | "istylegraph" wordmark (placeholder art). |
| b30efeb | `TMessagesProj/src/main/res/values/strings.xml`, `ui/SettingsActivity.java`, `ui/IntroActivity.java`, `myclient/MyClientStrings.java` (new), `messenger/LocaleController.java` | Unofficial disclosure in Settings, intro text, app name kept over cloud language packs. |
| 3bb8eab | `messenger/SharedConfig.java`, `ui/ActionBar/MessageDrawable.java`, `ui/ThemeActivity.java` | iOS bubble radii: 16 main, 8 grouped side. |
| 752b1db | `TMessagesProj/src/main/assets/ios_day.attheme` (new), `TMessagesProj/src/main/assets/ios_night.attheme` (new), `ui/ActionBar/Theme.java` | iOS Day and iOS Night themes, defaults on first launch. |
| 8a99b7c | `ui/MainTabsActivity.java`, `ui/SettingsActivity.java` | Tabs: Contacts, Chats, Settings. "Recent Calls" row in Settings. |
| a30332d | `ui/Components/CubicBezierInterpolator.java`, `ui/ActionBar/ActionBarLayout.java`, `ui/ActionBar/ActionBar.java` | Full-width push/pop slide with the iOS curve, 17sp nav titles. |
| 245687a | `TMessagesProj_App/src/main/res/raw/plane_logo_plain.json`, `raw/qr_code_logo.json`, `raw/qr_logo.svg`, `drawable-anydpi/logo_middle.xml` | Original art for the QR logos, round-video watermark and Terms of Service dialog. |
| c9abe32 | `ui/MainTabsActivity.java`, `ui/CallLogActivity.java` | The call list no longer offers to show or hide the Calls tab. |
| 186d00b | `TMessagesProj_App/src/main/res/drawable/send_plane_24.xml` | iOS-style up arrow on all send buttons. |
| d10b8ee | `gradle.properties`, `TMessagesProj_App/google-services.json` | Package id `com.istylegraph.app` (no Telegram name). |

Java paths without a prefix are in `TMessagesProj/src/main/java/org/telegram/`.

## Decisions

- Themes: two new built-in themes ("iOS Day", "iOS Night") instead of changes to the upstream themes. They are copies of the upstream Blue and Night palettes with the iOS values appended, so keys that iOS does not define keep working values. They have no accent options. Saved theme choices are kept.
- Tabs: iOS order Contacts, Chats, Settings, with Chats selected at start. The Calls and Profile tabs are hidden, not deleted, so upstream code around them keeps working. `MYCLIENT_IOS_TABS` in `MainTabsActivity` restores the upstream layout.
- Motion: only the standard push/pop changed. Swipe-back already moves the full screen. Preview (long-press) animations are unchanged.
- Send button: only the glyph changed. The new-design send button already draws a filled accent circle with a white icon, as on iOS.
- Package id: `com.istylegraph.app`. The contacts account type, provider authorities and the generated `MyClientAccountType` string follow `APP_PACKAGE`.
- Large titles: not used, because iOS Telegram turns them off (`NavigationController.swift:1505`).

## Telegram API ToS pass (core.telegram.org/api/terms)

| Rule | State |
|---|---|
| Own api_id and api_hash | Read from `local.properties` or environment. None are committed. Upstream values removed. |
| No "Telegram" in the app title | Title is "istylegraph". The package id `com.istylegraph.app` has no Telegram name either. |
| No official logo | Launcher icons, notification icon, splash, intro texture, wordmarks, QR logos, round-video watermark, the Terms of Service logo and the send glyph are replaced with original art. |
| Tell users the app is unofficial | Text under the version in Settings. Intro page 1 also says it. |
| Security | No change to tgnet, MTProto or encryption. |

No open ToS points are known. Check the store listing text and screenshots yourself before you publish.

## Not matched to iOS (flagged, not guessed)

1. Chat background: the iOS pattern wallpaper is not reproduced. Day uses a #A2D7F5 to #ABC8E0 gradient (the gradient end comes from the upstream Blue theme). Night uses solid black.
2. iOS Night uses white as the accent. Android draws white text on accent buttons in many places, so iOS Night keeps the Android Night accent for buttons and links.
3. In iOS Night, chat list rows are black and settings cells are #1C1C1D. Android uses one color key for both, so both are #1C1C1D.
4. Tabs: iOS can show an optional Calls tab. Here, Calls is not a tab. Recent calls open from Settings and from the Contacts tab menu.
5. Tabs: the Profile tab and its long-press account switcher are gone. Accounts are listed in Settings.
6. Push/pop duration is 350 ms, the UIKit default. The value was not found in the iOS code (DESIGN_SPEC gap). The iOS parallax shift and dimming of the screen below are not added.
7. Nav titles are 17sp but stay left-aligned. iOS centers them. `ActionBar.centerTitle()` only changes the text gravity and the layout code has no centered mode, so it is not turned on.
8. Sheet corner radius (iOS 10, glass 38) is not changed. Most sheets use the 9-patch `sheet_shadow_round`.
9. DESIGN_SPEC gaps, not changed: bubble tail shape, reply bar, timestamp weight, input field metrics, row heights, nav bar height, tab icon sizes, list corner radius.
10. `ChatActivity.java`, `Cells/ChatMessageCell.java` and `PhotoViewer.java` could not be read with the tools used, so there are no chat-screen or media-viewer layout changes.
11. SF Pro is not bundled (Apple license). The app uses Roboto.
12. Other app modules (Standalone, Huawei, HockeyApp) are not updated for the new package. Only `TMessagesProj_App` (afat) is supported.

## Check on a device

The CI build compiles the code but does not run it. Check these on a device:

- Install: the app installs as `com.istylegraph.app` next to the official app. A test build with the old id `com.itelegram.unofficial` is a separate app; uninstall it.
- Chat ID: correct values for a user, a basic group (`-id`), a supergroup and a channel (`-100...`). Tap copies the value.
- Launcher icons (default and alternate), notification icon, splash, intro animation, wordmark in the chat list header.
- Themes: first launch uses iOS Day, and night mode uses iOS Night. Check action bar icons, folder tabs, the search field and the chat input on both.
- Tabs: Contacts, Chats, Settings. Swipe between pages. Back returns to Chats. "Recent Calls" in Settings opens the call list, and the call list shows no calls-tab options.
- Push/pop: full-width slide. Look for screens with a transparent background.
- Send buttons: the arrow is centered in the circle (the old plane glyph may have had an optical offset).
- Contacts sync: the system account appears as istylegraph in Android account settings.
- QR screens, QR bottom sheets, round-video watermark, Terms of Service dialog, update-required screen.
