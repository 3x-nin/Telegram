/*
 * Unofficial client (myclient) layer. Not part of upstream Telegram for Android.
 * Licensed under GNU GPL v. 2 or later, like the rest of this project.
 */

package org.telegram.myclient;

import org.telegram.messenger.AndroidUtilities;
import org.telegram.messenger.ChatObject;
import org.telegram.messenger.LocaleController;
import org.telegram.messenger.R;
import org.telegram.tgnet.TLRPC;
import org.telegram.ui.ActionBar.BaseFragment;
import org.telegram.ui.Components.BulletinFactory;

/**
 * Formats and copies the numeric id shown in the "Chat ID" row of the profile screen.
 *
 * <p>The value uses the Telegram Bot API form:
 * <ul>
 *     <li>users and bots: the user id (a secret chat shows the id of the other user);</li>
 *     <li>basic groups: {@code -chat_id};</li>
 *     <li>supergroups and channels: {@code -1000000000000 - channel_id}, the "-100" form.</li>
 * </ul>
 */
public final class ChatIdHelper {

    private static final long BOT_API_CHANNEL_OFFSET = 1_000_000_000_000L;

    private ChatIdHelper() {
    }

    /**
     * @param userId user id for a user, bot or secret chat profile, otherwise 0
     * @param chatId chat or channel id for a group or channel profile, otherwise 0
     * @param chat   the loaded chat for {@code chatId}; tells a basic group from a channel
     */
    public static long toBotApiId(long userId, long chatId, TLRPC.Chat chat) {
        if (chatId != 0) {
            if (ChatObject.isChannel(chat)) {
                return -BOT_API_CHANNEL_OFFSET - chatId;
            }
            return -chatId;
        }
        return userId;
    }

    public static String format(long userId, long chatId, TLRPC.Chat chat) {
        return Long.toString(toBotApiId(userId, chatId, chat));
    }

    public static void copy(BaseFragment fragment, String id) {
        AndroidUtilities.addToClipboard(id);
        if (fragment != null) {
            BulletinFactory.of(fragment).createCopyBulletin(LocaleController.getString(R.string.MyClientChatIdCopied)).show();
        }
    }
}
