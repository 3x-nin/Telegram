/*
 * Unofficial client (myclient) layer. Not part of upstream Telegram for Android.
 * Licensed under GNU GPL v. 2 or later, like the rest of this project.
 */

package org.telegram.myclient;

import android.content.Context;

import org.telegram.messenger.ApplicationLoader;
import org.telegram.messenger.R;

/**
 * Strings that belong to this unofficial build. LocaleController asks this class first, so
 * Telegram's server language packs and the bundled translations cannot bring back "Telegram"
 * as the app name.
 */
public final class MyClientStrings {

    private MyClientStrings() {
    }

    /**
     * @return this build's own value for the string, or null if the string is not owned by the fork
     */
    public static String forkOwned(String key, int stringRes) {
        final int res;
        if (stringRes == R.string.AppName || "AppName".equals(key)) {
            res = R.string.AppName;
        } else if (stringRes == R.string.AppNameBeta || "AppNameBeta".equals(key)) {
            res = R.string.AppNameBeta;
        } else {
            return null;
        }
        final Context context = ApplicationLoader.applicationContext;
        if (context == null) {
            return null;
        }
        try {
            return context.getResources().getString(res);
        } catch (Exception e) {
            return null;
        }
    }
}
