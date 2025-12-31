

package com.thirtydegreesray.openhub.util;

import android.content.Context;
import android.net.ConnectivityManager;
import android.net.NetworkInfo;
import androidx.annotation.NonNull;
import android.util.Log;

/**
 * 检测实时网络状�? <p>
 * @author Administrator
 *
 */
public enum  NetHelper {
	INSTANCE;

	public static final int TYPE_DISCONNECT = 0;
	public static final int TYPE_WIFI = 1;
	public static final int TYPE_MOBILE = 2;


	private int mCurNetStatus;
	private Context mContext;

	public void init(Context context){
		mContext = context;
		checkNet();
	}

	/**
	 * 检测当前网络状�?
	 */
	public void checkNet(){
		try {
			ConnectivityManager connectivity = (ConnectivityManager) mContext
					.getSystemService(Context.CONNECTIVITY_SERVICE);
			if (connectivity != null) {
				// 获取网络连接管理的对�?
				NetworkInfo info = connectivity.getActiveNetworkInfo();
				if (info != null&& info.isAvailable()) {
					// 判断当前网络是否已经连接
					if (info.getState() == NetworkInfo.State.CONNECTED) {
						if(info.getType() == ConnectivityManager.TYPE_WIFI)
							mCurNetStatus =  TYPE_WIFI;
						if(info.getType() == ConnectivityManager.TYPE_MOBILE)
							mCurNetStatus =  TYPE_MOBILE;
					}
				} else{
					mCurNetStatus = TYPE_DISCONNECT;
				}
			}
		} catch (Exception e) {
			Log.v("error",e.toString());
			e.printStackTrace();
			mCurNetStatus = TYPE_DISCONNECT;
		}
	}

	/**
	 * 网络是否可用
	 * @return
     */
	@NonNull
    public Boolean getNetEnabled(){
		return mCurNetStatus == TYPE_MOBILE || mCurNetStatus == TYPE_WIFI;
	}

	/**
	 * 是否处于移动网络状�?
	 * @return
     */
	@NonNull
    public Boolean isMobileStatus(){
		return mCurNetStatus == TYPE_MOBILE;
	}

	/**
	 * 获取当前网络状�?
	 * @return
     */
	public int getNetStatus() {
		return mCurNetStatus;
	}
}
