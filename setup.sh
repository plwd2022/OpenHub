#!/bin/bash
set -euxo pipefail

# 1. 安装基础依赖
sudo apt-get update
sudo apt-get install -y wget unzip git curl openjdk-17-jdk

# 2. 配置环境变量并持久化
# 追加到~/.bashrc，便于后续shell会话自动生效
grep -qF 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' ~/.bashrc || echo 'export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64' >> ~/.bashrc
grep -qF 'export GRADLE_USER_HOME=$HOME/.gradle' ~/.bashrc || echo 'export GRADLE_USER_HOME=$HOME/.gradle' >> ~/.bashrc
grep -qF 'export ANDROID_SDK_ROOT=$HOME/android-sdk' ~/.bashrc || echo 'export ANDROID_SDK_ROOT=$HOME/android-sdk' >> ~/.bashrc
grep -qF 'export ANDROID_HOME=$ANDROID_SDK_ROOT' ~/.bashrc || echo 'export ANDROID_HOME=$ANDROID_SDK_ROOT' >> ~/.bashrc
grep -qF 'export PATH=$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH' ~/.bashrc || echo 'export PATH=$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH' >> ~/.bashrc

# 直接在当前脚本会话中导出环境变量，确保即时生效
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export GRADLE_USER_HOME=$HOME/.gradle
export ANDROID_SDK_ROOT=$HOME/android-sdk
export ANDROID_HOME=$ANDROID_SDK_ROOT
export PATH=$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$PATH

# 3. 安装 Android SDK (如果不存在)
if [ ! -d "$ANDROID_SDK_ROOT/cmdline-tools" ]; then
  mkdir -p "$ANDROID_SDK_ROOT/cmdline-tools"
  cd "$ANDROID_SDK_ROOT/cmdline-tools"
  wget -q https://dl.google.com/android/repository/commandlinetools-linux-11076708_latest.zip -O tools.zip
  unzip -q tools.zip
  mv cmdline-tools latest

  # 4. 安装 Android SDK 组件，并自动接受所有许可证
  yes | "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$ANDROID_SDK_ROOT" --licenses || true
  
  # 安装项目所需的SDK版本和构建工具
  "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$ANDROID_SDK_ROOT" \
    "platform-tools" \
    "platforms;android-36" \
    "build-tools;36.0.0" \
    "build-tools;35.0.0" \
    "build-tools;34.0.0"

  cd - # 回到原始目录
else
  echo "✅ Android SDK 已存在，跳过安装。"
  
  # 检查是否需要安装额外的SDK版本
  if [ ! -d "$ANDROID_SDK_ROOT/platforms/android-36" ]; then
    echo "📦 安装 Android 36 SDK..."
    yes | "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$ANDROID_SDK_ROOT" --licenses || true
    "$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" --sdk_root="$ANDROID_SDK_ROOT" "platforms;android-36" "build-tools;36.0.0"
  fi
fi

# 5. 授权 gradlew
chmod +x gradlew

# 重新加载.bashrc，确保环境变量在当前会话中生效
source ~/.bashrc

echo "✅ Android Jetpack Compose 环境准备完成！"
echo "📋 已安装的组件："
echo "   - Java 17 OpenJDK"
echo "   - Android SDK Platform 36"
echo "   - Android Build Tools 36.0.0, 35.0.0, 34.0.0"
echo "   - Android Platform Tools"
echo "   - Gradle Wrapper (8.13)"
echo ""
echo "🚀 后续编译/测试/打包请由平台AI自动执行。"