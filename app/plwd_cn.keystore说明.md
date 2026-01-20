# plwd_cn.keystore 使用说明

本文件为 Android 应用正式版（Release）签名文件，适用于 Jetpack Compose 项目及常规 Android 项目。

## 签名文件信息
- **签名文件名**：plwd_cn.keystore
- **签名别名（Alias）**：plwd
- **签名密码（Key Password）**：plwd@2022@plwd
- **密钥库密码（Keystore Password）**：plwd@2022@plwd
- **国家（C）**：cn
- **组织（O）/组织单位（OU）/省份（S）/城市（L）**：plwd

## 配置方法

1. 将 `plwd_cn.keystore` 文件放置在项目根目录或安全位置。
2. 在 `app/build.gradle.kts` 的 `android` 节点下添加如下配置（已为你配置好）：

```kotlin
droid {
    signingConfigs {
        create("release") {
            storeFile = file("../plwd_cn.keystore")
            storePassword = "plwd@2022@plwd"
            keyAlias = "plwd"
            keyPassword = "plwd@2022@plwd"
        }
    }
    buildTypes {
        getByName("release") {
            signingConfig = signingConfigs.getByName("release")
        }
    }
}
```

3. 通过如下命令生成正式版 APK：

```sh
./gradlew assembleRelease
```

生成的 APK 路径：`app/build/outputs/apk/release/app-release.apk`

## 注意事项
- 请妥善保管此 keystore 文件及相关密码，遗失后将无法更新已发布的应用。
- 不要将 keystore 文件和密码上传到公开仓库。
- 若需更换签名，需在应用市场备案并谨慎操作。 