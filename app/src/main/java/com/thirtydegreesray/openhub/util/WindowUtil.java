

package com.thirtydegreesray.openhub.util;

import android.app.Activity;
import android.content.Context;
import android.graphics.Rect;
import androidx.annotation.NonNull;

/**
 * 手机窗口工具�?
 */
public class WindowUtil {

    /**
     * 屏幕宽度
     */
    public static int screenWidth = 0;

    /**
     * 屏幕高度
     */
    public static int screenHeight = 0;

    /** 
     * 根据手机的分辨率�?dp 的单�?转成�?px(像素) 
     */  
    public static int dipToPx(@NonNull Context context, float dpValue) {
        final float scale = context.getResources().getDisplayMetrics().density;  
        return (int) (dpValue * scale + 0.5f);  
    }  
  
    /** 
     * 根据手机的分辨率�?px(像素) 的单�?转成�?dp 
     */  
    public static int pxToDip(@NonNull Context context, float pxValue) {
        final float scale = context.getResources().getDisplayMetrics().density;  
        return (int) (pxValue / scale + 0.5f);  
    }

    /**
     *
     * @param activity
     * @return
     */
    public static int getStatusHeight(@NonNull Activity activity){
        int statusHeight = 0;
        Rect localRect = new Rect();
        activity.getWindow().getDecorView().getWindowVisibleDisplayFrame(localRect);
        statusHeight = localRect.top;
        if (0 == statusHeight){
            Class<?> localClass;
            try {
                localClass = Class.forName("com.android.internal.R$dimen");
                Object localObject = localClass.newInstance();
                int i5 = Integer.parseInt(localClass.getField("status_bar_height").get(localObject).toString());
                statusHeight = activity.getResources().getDimensionPixelSize(i5);
            } catch (ClassNotFoundException e) {
                e.printStackTrace();
            } catch (IllegalAccessException e) {
                e.printStackTrace();
            } catch (InstantiationException e) {
                e.printStackTrace();
            } catch (NumberFormatException e) {
                e.printStackTrace();
            } catch (IllegalArgumentException e) {
                e.printStackTrace();
            } catch (SecurityException e) {
                e.printStackTrace();
            } catch (NoSuchFieldException e) {
                e.printStackTrace();
            }
        }
        return statusHeight;
    }
}
 
