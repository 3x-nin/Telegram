# DESIGN_SPEC: iOS-style reskin of the unofficial Android client

Status: draft for review. Written before any UI code changes.

## Conventions

- **Source of truth:** the iOS client in `3x-nin/Telegram-iOS`. Every value cites `file:line`. Paths are under `submodules/` unless they start with another folder.
- **Units:** 1 iOS pt = 1 Android dp. Telegram for Android sets text sizes in dp, so font sizes also map 1:1.
- **Fonts:** iOS uses the system font (SF Pro). SF Pro is licensed by Apple and is not shipped. Android keeps the system sans-serif. Weight map: regular 400, medium 500, semibold 600 (medium 500 where 600 is not available), bold 700.
- **Icons:** no SF Symbols and no other Apple assets. Android keeps Telegram for Android's own icon set; only size and weight change.
- **Default iOS themes:** day is **Classic** (`dayClassic`), used on first launch. Dark is **Night**. Sources: `TelegramUIPreferences/Sources/PresentationThemeSettings.swift:655`, `TelegramPresentationData/Sources/PresentationData.swift:386-409`.
- **Derived** = computed from a formula in the code. **Gap** = not found in the code. Gaps are not guessed.
- Colors with alpha are written `#RRGGBBAA`.

Short names used in the tables:

- `Day` = `TelegramPresentationData/Sources/DefaultDayPresentationTheme.swift`
- `Dark` = `TelegramPresentationData/Sources/DefaultDarkPresentationTheme.swift`
- `ItemCommon` = `TelegramUI/Components/Chat/ChatMessageItemCommon/Sources/ChatMessageItemCommon.swift`
- `ChatListItem` = `ChatListUI/Sources/Node/ChatListItem.swift`

## 1. Colors

### 1.1 Lists and screens

| Token | Day (Classic) | Night | Source |
|---|---|---|---|
| Plain background | `#FFFFFF` | `#000000` | Day:472-478, Dark:412-418 |
| Grouped background | `#EFEFF4` | `#000000` | same |
| Cell background | `#FFFFFF` | `#1C1C1D` | same |
| Separator | `#C8C7CC` | `#5454588C` | Day:489-490, Dark:430-431 |
| Section header text | `#6D6D72` | `#8D8E93` | Day:495, Dark:437 |
| Primary text | `#000000` | `#FFFFFF` | Day:476, Dark:416 |
| Secondary text | `#8E8E93` | `#98989E` | same |
| Accent and links | `#0088FF` | `#FFFFFF` | Day:55,480, Dark:416-417 |
| Destructive | `#FF3B30` | `#EB5545` | Day:482, Dark:421 |
| Disclosure arrow | `#BAB9BE` | `#FFFFFF47` | Day:494, Dark:429 |
| Switch on | `#35C759` | `#67CE67` | Day:463, Dark:405 |
| Check and badge fill / glyph | `#0088FF` / `#FFFFFF` | `#FFFFFF` / `#000000` | Day:506-510, Dark:443-447 |

### 1.2 Navigation bar

| Token | Day (Classic) | Night | Source |
|---|---|---|---|
| Background (blurred) | `#F2F2F2E6` | `#1D1D1DE6` | Day:412-430, Dark:345-363 |
| Buttons | `#0088FF` | `#FFFFFF` | same |
| Title | `#000000` | `#FFFFFF` | same |
| Subtitle | `#787878` | `#FFFFFF80` | same |
| Separator | `#C8C7CC` | `#5454588C` | same |
| Badge fill / text | `#FF3B30` / `#FFFFFF` | `#FFFFFF` / `#000000` | same |

### 1.3 Tab bar

| Token | Day (Classic) | Night | Source |
|---|---|---|---|
| Background (blurred) | `#F2F2F2E6` | `#1D1D1DE6` | Day:433-444, Dark:365-376 |
| Separator | `#B2B2B2` | `#5454588C` | same |
| Icon, not selected | `#959595` | `#FFFFFF` (same as selected in this file; the glass tab bar may dim it, verify) | same |
| Label, not selected | `#000000CC` | `#FFFFFF` | same |
| Icon and label, selected | `#0088FF` | `#FFFFFF` | same |
| Badge fill / text | `#FF3B30` / `#FFFFFF` | `#FFFFFF` / `#000000` | same |

### 1.4 Chat list

| Token | Day (Classic) | Night | Source |
|---|---|---|---|
| Row background | `#FFFFFF` | `#000000` | Day:539-570, Dark:489-522 |
| Title | `#000000` | `#FFFFFF` | same |
| Message preview | `#8E8E93` | `#8D8E93` | same |
| Date | `#8E8E93` | `#8D8E93` | same |
| Unread badge fill / text | `#0088FF` / `#FFFFFF` | `#FFFFFF` / `#000000` | same |
| Muted unread badge fill / text | `#B6B6BB` / `#FFFFFF` | `#666666` / `#000000` | same |
| Pinned row background | `#F7F7F7` | `#1C1C1D` | same |
| Read checkmarks | `#0088FF` | `#FFFFFF` | same |
| Online dot | `#4CC91F` | `#4CC91F` | same |

### 1.5 Chat

| Token | Day (Classic) | Night | Source |
|---|---|---|---|
| Wallpaper | Built-in pattern. Gradient inputs `#72D5FD`, `#2A9EF1`, `#8EABF0`, `#A2D7F5`, `#B7E2F5`, `#C6E8F5`. Rendered result: Gap | Built-in pattern. `#598BF6`, `#7A5EEF`, `#D67CFF`, `#F38B58`, intensity -34 | Day:1007,1109+, Dark:344-351,730 |
| Incoming bubble | `#FFFFFF`. Stroke derived from the service color at alpha 0.2 | `#1D1D1DE6`, no stroke | Day:574-620, Dark:523-565 |
| Incoming text / secondary / link | `#000000` / `#52525299` / `#004BAD` | `#FFFFFF` / `#FFFFFF80` / `#FFFFFF` | Day:645-650, Dark:565-567 |
| Outgoing bubble | `#E1FFC7`, same derived stroke | Gradient `#61BCF9` to `#0088FF`, no stroke | Day:666-711, Dark:574-619 |
| Outgoing text / secondary / link / checks | `#000000` / `#008C09CC` / `#004BAD` / `#19C700` | `#FFFFFF` / `#FFFFFF80` / `#FFFFFF` / `#FFFFFF` | Day:700-711,939, Dark:605-619,640 |
| Service message (date) fill / text | `#FFFFFFCC` / `#8D8E93` | `#1F1F1F` / `#FFFFFF`; date pill fill `#00000033` | Day:965-975, Dark:654-662 |
| Input panel background | `#F2F2F2E6` (blurred) | `#1D1D1DE6` | Day:945-964, Dark:686-705 |
| Input field fill / placeholder / stroke | `#FFFFFFCC` / `#00000066` / `#0000001A` | Derived (white over black, alpha 0.95) / `#FFFFFF7A` / `#FFFFFF1A` | same |
| Send button fill / glyph | `#0088FF` / `#FFFFFF` | `#FFFFFF` / `#000000` | same |

## 2. Typography

| Use | Weight and size | Source |
|---|---|---|
| Base size (`PresentationFontSize.regular`) | 17 | `ComponentsThemes.swift:19-36` |
| Navigation title | semibold 17 | `ItemListUI/Sources/ItemListController.swift:736` |
| Large titles | Not used. UIKit large titles are turned off | `Display/Source/Navigation/NavigationController.swift:1505` |
| List item title | regular 17 | `ItemListUI/Sources/ItemListItem.swift:214-223` |
| Section header | regular 13, not uppercased. Derived: floor(17 x 13/17) | `ItemListItem.swift:214-223`, `ItemListUI/Sources/Items/ItemListSectionHeaderItem.swift:182-190` |
| Footer text | regular 13 to 15, depends on the item | `ItemListUI/Sources/Items/ItemListInfoItem.swift:235-240` |
| Chat list title | semibold 16. Derived: floor(17 x 16/17) | ChatListItem:2294-2299 |
| Chat list preview | regular 15 | same |
| Chat list date | regular 14 | same |
| Chat list unread badge | semibold 12, monospaced digits | ChatListItem:2298-2299 |
| Message text | regular 17 | `TelegramPresentationData/Sources/PresentationData.swift:886-900` |
| Message timestamp | 11, derived: floor(17 x 11/17). Weight: Gap | `TelegramUI/Components/Chat/ChatMessageDateAndStatusNode/Sources/ChatMessageDateAndStatusNode.swift:551` |
| Reply preview title and text | Gap (size set at runtime) | `TelegramUI/Components/Chat/ChatMessageReplyInfoNode/Sources/ChatMessageReplyInfoNode.swift:196-197` |
| Reaction count | medium 11 | `Components/ReactionButtonListComponent/Sources/ReactionButtonListComponent.swift:630,651` |
| Profile action button | semibold 16 | `TelegramUI/Components/PeerInfo/PeerInfoScreen/Sources/PeerInfoHeaderActionButtonNode.swift:77-84` |
| Tab label (legacy tab bar) | medium 10 | `TabBarUI/Sources/TabBarNode.swift:16-18` |

Font helper: `Display/Source/Font.swift:1-364`. `Font.regular`, `medium`, `semibold` and `bold` map to the matching system font weights.

## 3. Chat bubbles and message layout

| Metric | Value | Source |
|---|---|---|
| Corner radius, main | 16 | `TelegramUIPreferences/Sources/PresentationThemeSettings.swift:561` |
| Corner radius, grouped side | 8 | same |
| Group consecutive bubbles | on | same |
| Tail | Drawn on the last bubble of a group through `.Tail` corner images. Size: Gap | `TelegramUI/Components/Chat/ChatMessageBubbleContentNode/Sources/ChatMessageBubbleContentCalclulateImageCorners.swift:97-152` |
| Text padding (phone) | top 6, left and right 11, bottom 6 (plus or minus 1 px) | ItemCommon:139 |
| Minimum bubble size | 40 x 35 | ItemCommon:138 |
| Maximum width (screen width 500 or less) | screen width - 36 | ItemCommon:138 |
| Bubble edge inset | 3 | ItemCommon:138 |
| Spacing inside a group | 0 | ItemCommon:138 |
| Spacing between groups | 2 + 1 px | ItemCommon:138 |
| Media bubble padding | 2 | ItemCommon:140 |
| Media corner radius | 16; 8 on grouped sides | ItemCommon:152 |
| Avatar column in groups | 34 + 4 = 38 | ItemCommon:146 |
| Date header height | 34 | ItemCommon:146 |
| Timestamp placement | Inside the bubble at the trailing edge, with status checks. Varies by content type | `ChatMessageDateAndStatusNode.swift:1419-1428` |
| Reply preview | Text padding 3 top and bottom. Thumbnail side = 2 x first line height. Accent bar width: Gap | `ChatMessageReplyInfoNode.swift:639,685,688-701` |
| Reactions | Height 30, side padding 11, icon 20, gap 2 | `ReactionButtonListComponent.swift:828-831` |

## 4. Chat input bar

| Metric | Value | Source |
|---|---|---|
| Base panel height | 40 | `TelegramUI/Components/Chat/ChatInputPanelNode/Sources/ChatInputPanelNode.swift:42-47` |
| Text field corner radius and insets | Gap (in the concrete text input panel) | |
| Attach, send and mic button sizes | Gap | |

## 5. Chat list

| Metric | Value | Source |
|---|---|---|
| Avatar | 60. Derived: min(60, floor(17 x 60/17)) | ChatListItem:2025-2029 |
| Avatar placement | Centered vertically | ChatListItem:4202 |
| Separator | 1 px, right inset 16 | ChatListItem:923, 5366-5383 |
| Row height | Depends on content. Fixed value: Gap | ChatListItem:4036-4055 |
| Unread badge size | Depends on text. Gap | |

## 6. Navigation bar

| Metric | Value | Source |
|---|---|---|
| Back arrow | Custom path in a 13 x 22 box | `Display/Source/NavigationBar.swift:8-19` |
| Back label | Title of the previous screen, or custom text | `NavigationBar.swift:162-177` |
| Title font | semibold 17 | `ItemListController.swift:736` |
| Large titles | Off | `NavigationController.swift:1505` |
| Search field | Height 44, side inset 16, regular 17 | `SearchBarNode/Sources/SearchBarNode.swift:833-846,1218` |
| Search field corner radius | Gap | `SearchBarNode.swift:1045` |
| Bar height, title alignment | Gap | |

## 7. Tab bar

| Metric | Value | Source |
|---|---|---|
| Order | Contacts, Calls (optional), Chats, Settings | `TelegramUI/Sources/TelegramRootController.swift:201-224` |
| Selected at start | Chats | `TelegramRootController.swift:242` |
| Height | 49 + bottom safe area (compact: 34) | `TabBarUI/Sources/TabBarController.swift:184-195` |
| Active implementation | Component-based glass `TabBarComponent` | `TabBarUI/Sources/TabBarContollerNode.swift:143,230-290` |
| Tab switch | Spring, 0.4 s | `TabBarContollerNode.swift:222-226` |
| Icon size, badge geometry | Gap | |

## 8. Settings and grouped lists

| Metric | Value | Source |
|---|---|---|
| Layout | Rounded inset blocks when the width is 320 or more (all phones) | `ItemListUI/Sources/ItemListItem.swift:179-181` |
| Block corner radius | Gap (set per item) | |
| Text left inset | 16; 59 with an icon (16 + 43); 62 with an avatar | `ItemListUI/Sources/Items/ItemListDisclosureItem.swift:418-425` |
| Right inset | 16; 34 with a disclosure arrow | `ItemListDisclosureItem.swift:343-351` |
| Row vertical inset | 11 (legacy); 13 to 15 (glass) | `ItemListDisclosureItem.swift:519-547` |
| Section spacing | Top 24 or 35, between sections 16, bottom 35 | `ItemListItem.swift:144-177` |
| Section header | Text height + 13. Top inset 24 (first section) or 28 | `ItemListSectionHeaderItem.swift:225-237` |
| Row badge | 20 (24 when semi-transparent) | `ItemListDisclosureItem.swift:365-375` |
| Icon size and icon corner radius | Gap | |

## 9. Profile and info

| Metric | Value | Source |
|---|---|---|
| Avatar | 100; 200 in the modal overlay | `TelegramUI/Components/PeerInfo/PeerInfoScreen/Sources/PeerInfoHeaderNode.swift:534-535` |
| Avatar top | Status bar + 22 | `PeerInfoHeaderNode.swift:644` |
| Header | Expanded and collapsed title states, blended on scroll | `PeerInfoHeaderNode.swift:83-94,818-861` |
| Action buttons | Corner radius 11, semibold 16. Size set by the caller | `PeerInfoHeaderActionButtonNode.swift:27,77-84` |
| Info row height | Gap | |

## 10. Media viewer

| Metric | Value | Source |
|---|---|---|
| Background | Black | `GalleryUI/Sources/GalleryControllerNode.swift:65-67` |
| Dismiss gesture | Vertical swipe. Dismisses when speed > 1 or distance > height / 12 | `GalleryControllerNode.swift:514-583,565-568` |
| Controls | Fade in 0.15 s linear; fade out 0.1 to 0.25 s | `GalleryControllerNode.swift:423-458,480-507` |
| Header scrim | Black, alpha 0.65 | `GalleryControllerNode.swift:308-310` |
| Content settle | Spring, 0.4 s | `GalleryControllerNode.swift:423-458` |

## 11. Motion

| Metric | Value | Source |
|---|---|---|
| Curves in use | Linear, ease-in-out, ease-in, system spring, custom spring (mass 5, stiffness 900), custom Bezier | `Display/Source/ContainedViewLayoutTransition.swift:10-18` |
| Slide curve | Cubic Bezier (0.33, 0.52, 0.25, 0.99) | `ContainedViewLayoutTransition.swift:20-22` |
| Modal sheet corner radius | 10 (standard); 38 (glass) | `Display/Source/Navigation/NavigationModalContainer.swift:390-398` |
| Modal top inset | Status bar + 10 | `NavigationModalContainer.swift:414-425` |
| Swipe-back | Interactive pop | `Display/Source/Navigation/NavigationContainer.swift:253-254` |
| Tab switch | Spring, 0.4 s | `TabBarContollerNode.swift:222-226` |
| Push and pop duration and curve | Gap | |
| Action sheet timing | Gap | |

## 12. Android file map

Paths are under `TMessagesProj/src/main/java/org/telegram/`. Sizes are line counts. "Not indexed" means the file is too large for code search, so I cannot read it.

| iOS surface | Android classes | Size | Planned approach |
|---|---|---|---|
| Colors and themes | `ui/ActionBar/ThemeColors.java` (defaults), `ui/ActionBar/Theme.java` (built-in themes from `bluebubbles`, `day`, `night`, `darkblue`, `arctic` `.attheme` assets) | 1,795; 10,499 | Add the Classic and Night palettes as a separate theme layer (new theme assets and a small registration hook). Keep upstream defaults unchanged. |
| Chat bubbles | `ui/ActionBar/MessageDrawable.java`; `messenger/SharedConfig.java` (`bubbleRadius = 17`) | 898; 1,915 | Default radius 16, grouped side 8. |
| Chat screen | `ui/ChatActivity.java`, `ui/Cells/ChatMessageCell.java` | Not indexed | Tail shape, bubble padding, timestamp, reply and reaction layout are out of reach for now. |
| Input bar | `ui/Components/ChatActivityEnterView.java` | 16,280 | Colors through theme keys. Field radius and padding only through small anchored edits. |
| Chat list | `ui/DialogsActivity.java`, `ui/Cells/DialogCell.java` (avatar radius 26, so 52dp), `ui/Adapters/DialogsAdapter.java` (rows 70 or 76dp) | 14,974; 6,750; 1,895 | Text sizes 16, 15, 14 and colors first. A 60dp avatar and new row heights are larger layout edits: later. |
| Tab bar | `ui/MainTabsActivity.java` (tabs: Chats, Contacts, Settings or Calls, Profile), `ui/Components/glass/GlassTabView.java` | 1,273; 694 | Reorder to Contacts, Calls (optional), Chats, Settings. Profile tab: decision needed (see 13). |
| Navigation bar | `ui/ActionBar/ActionBar.java`, `ui/ActionBar/ActionBarLayout.java` (swipe-back already exists) | 2,550; 3,716 | Title weight and size, back arrow, and the slide curve for push and pop. Keep swipe-back. |
| Sheets | `ui/ActionBar/BottomSheet.java`, `ui/ActionBar/AlertDialog.java`, `ui/Components/ItemOptions.java` | 2,604; 2,115; 2,341 | Sheet corner radius 10. Use sheets where iOS does, one case at a time. |
| Settings | `ui/SettingsActivity.java`, `ui/Components/UniversalAdapter.java`, `ui/Components/RecyclerListView.java` (rounded sections, radius 16, padding 12) | 2,169; 1,301; 4,024 | Already inset-grouped. Apply the list colors. The radius stays until the iOS value is confirmed. |
| Profile | `ui/ProfileActivity.java` | 17,631 | Chat ID row (Step 3). Header layout unchanged for now. |
| Media viewer | `ui/PhotoViewer.java` | Not indexed | Out of reach for now. |
| Motion | `ui/Components/CubicBezierInterpolator.java` | 88 | Add the iOS slide curve as a named constant. |

## 13. Decisions and deviations

- **Large titles:** not added, because iOS Telegram turns them off.
- **Fonts:** system sans-serif, not SF Pro (license).
- **Icons:** Telegram for Android's own icons, resized where needed. No Apple assets.
- **Profile tab:** iOS has no Profile tab. Proposal: Contacts, Calls (optional), Chats, Settings, with the own profile opened from the Settings header as on iOS. Needs approval.
- **Night accent:** iOS Night uses white as the accent. Android keeps its accent picker; the iOS values become the defaults of the new theme layer.

## 14. Open gaps

These are not guessed. Each one needs a closer read of the iOS code or a screenshot comparison:

- Bubble tail geometry, reply accent bar width, reply fonts, timestamp weight.
- Input field corner radius and insets; attach, send and mic button sizes.
- Chat list row height and unread badge size.
- Navigation bar height, title alignment, search field corner radius.
- Tab icon size and badge geometry.
- Grouped list block corner radius and icon size.
- Profile info row height.
- Push and pop duration and curve; action sheet timing.
- Rendered default wallpaper.
