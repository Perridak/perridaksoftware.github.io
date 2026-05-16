# Getting Started

Welcome! This chapter will guide you through setting up Flutter on your system. We'll cover a minimal installation—just what you need to develop and run Flutter apps without unnecessary bloat.

Choose your platform below to see platform-specific instructions.

<div class="platform-selector">
  <button class="platform-btn" onclick="togglePlatform('windows')">🪟 Windows</button>
  <button class="platform-btn" onclick="togglePlatform('macos')">🍎 macOS</button>
</div>

---

## System Overview

Before we dive into platform-specific steps, here's what you'll be installing:

1. **Flutter SDK** – The framework and development tools
2. **Dart SDK** – Included with Flutter; the programming language
3. **Git** – Version control (required by Flutter)
4. **Platform-specific tools** – Android SDK, Xcode Command Line Tools, etc.
5. **An editor** – We'll assume Visual Studio Code, but you can use any editor

The good news: you don't need the full Android Studio or Visual Studio IDEs. We'll show you how to install just the essential components.

---

<div class="platform-windows">

## Windows Setup

### Requirements Check

Ensure your system meets these requirements:

- **OS:** Windows 10 or later (64-bit)
- **Disk Space:** ~2.5 GB total (400 MB for Flutter SDK, the rest for Android SDK and tools)
- **Internet:** A stable connection for downloading ~2 GB of files

### Step 1: Install Git

Flutter requires Git for version control.

1. Visit [https://git-scm.com/download/win](https://git-scm.com/download/win)
2. Download the latest 64-bit installer
3. Run the installer and use default settings (important: keep "Git Bash" selected)
4. After installation, open PowerShell and verify:

```
git --version
```

Expected output: `git version X.X.X...`

### Step 2: Download Flutter SDK

1. Visit [https://flutter.dev/docs/release/archive](https://flutter.dev/docs/release/archive) (or flutter.dev, then look for Download)
2. Download the latest stable Windows release (look for the `.zip` file, NOT the `.tar.gz`)
3. Extract the downloaded `flutter_windows_X.X.X-stable.zip` to a permanent location. We recommend:

```
C:\src\flutter
```

Do NOT extract to `Program Files` (it requires admin permissions for updates). Create the `C:\src` folder first if needed.

### Step 3: Add Flutter to Your PATH

This lets you run Flutter commands from any PowerShell window.

1. Press `Win + X` and select "System" (or right-click "This PC" → Properties)
2. Click "Advanced system settings" on the right
3. Click "Environment Variables" button at the bottom
4. Under "User variables", click "New"
5. Variable name: `PATH`
6. Variable value: `C:\src\flutter\bin` (adjust if you extracted elsewhere)
7. Click OK, then OK again to close all windows
8. **Restart PowerShell completely** (close and reopen)

Verify it worked:

```
flutter --version
```

Expected output: `Flutter X.X.X • channel stable • ...`

### Step 4: Install Android SDK

Flutter needs the Android SDK to build Android apps. You don't need Android Studio—we'll install just the SDK.

#### Option A: Minimal Setup (Recommended)

1. Download **Android Command Line Tools** from:
   [https://developer.android.com/studio#command-tools](https://developer.android.com/studio#command-tools)
   
   Look for "Command line tools only" section, download the Windows version.

2. Create a folder structure:

```
C:\Android\cmdline-tools
```

3. Extract the downloaded `cmdline-tools-windows-XXXXX.zip` into that folder. After extraction, you should have:

```
C:\Android\cmdline-tools\
  └── cmdline-tools\
      ├── bin\
      ├── lib\
      └── (other files)
```

4. In PowerShell, set environment variables:

```
[Environment]::SetEnvironmentVariable("ANDROID_HOME", "C:\Android", "User")
[Environment]::SetEnvironmentVariable("ANDROID_SDK_ROOT", "C:\Android", "User")
```

5. Close and reopen PowerShell, then run:

```
sdkmanager --sdk_root=C:\Android --list
```

This should display available SDK packages.

6. Install required components:

```
sdkmanager --sdk_root=C:\Android "build-tools;latest"
sdkmanager --sdk_root=C:\Android "platforms;android-34"
sdkmanager --sdk_root=C:\Android "platform-tools"
```

#### Option B: If You Prefer Android Studio UI

If you find command-line tools confusing, download and install Android Studio from [https://developer.android.com/studio](https://developer.android.com/studio). During setup, it will guide you to install the SDK. Then proceed with Step 5 below.

### Step 5: Accept Android Licenses

Run this command to accept the required licenses:

```
flutter doctor --android-licenses
```

When prompted, type `y` and press Enter for each license.

### Step 6: Verify Your Setup

Run the diagnostic tool:

```
flutter doctor
```

Expected output (checkmarks indicate success):

```
Doctor summary (to see all details, run flutter doctor -v):

[✓] Flutter (Channel stable, X.X.X)
[✓] Windows Version (Windows 10)
[✓] Android toolchain - develop for Android devices (Android SDK X.X)
[✓] Android Studio (version X.X) [optional - you don't need this]
[✓] VS Code (version X.X.X)
[✓] Connected device (optional - only if a device is plugged in)
```

**Red X marks indicate missing components.** See the troubleshooting section if you encounter errors.

### Step 7: Create Your First App

Create a test project to verify everything works:

```
flutter create my_first_app
cd my_first_app
flutter run
```

The first run takes time (2-3 minutes) as it builds the Android app. You should see output ending with "Built and skipped checking for root certificate" or similar, indicating success.

If no Android device is connected, you'll see an error about available devices. That's okay for now—we'll cover device setup in the next section.

---

### Optional: Target Windows or Web Apps

Windows developers can also build Windows desktop apps. After completing the Android setup above:

**For Windows desktop apps:**

```
flutter config --enable-windows-desktop
flutter doctor
```

Run `flutter doctor` again and look for a green checkmark next to "Windows Version".

**For web apps:**

```
flutter config --enable-web
flutter doctor
```

Then `flutter create --platforms=web my_web_app` will create a web project.

</div>

<div class="platform-macos">

## macOS Setup

### Requirements Check

Ensure your system meets these requirements:

- **OS:** macOS 11 (Big Sur) or later
- **Chip:** Intel or Apple Silicon (M1/M2/M3)
- **Disk Space:** ~3 GB total (400 MB for Flutter SDK, rest for Xcode Command Line Tools, Android SDK, and optional Xcode)
- **Internet:** A stable connection for downloading ~3 GB of files

### Step 1: Install Xcode Command Line Tools

macOS requires these tools for development. Install them:

```
xcode-select --install
```

A dialog will appear. Click "Install" and wait (5-15 minutes depending on connection speed).

Verify installation:

```
xcode-select --print-path
```

Expected output: `/Applications/Xcode.app/Contents/Developer` or similar.

### Step 2: Download Flutter SDK

1. Visit [https://flutter.dev/docs/release/archive](https://flutter.dev/docs/release/archive)
2. Download the latest stable macOS release (look for `.tar.xz` file, NOT the Windows `.zip`)
3. Extract to your development directory. We recommend:

```
mkdir -p ~/development
cd ~/development
tar xf ~/Downloads/flutter_macos_X.X.X-stable.tar.xz
```

This creates `~/development/flutter`.

### Step 3: Add Flutter to Your PATH

Open Terminal and edit your shell configuration file. Modern macOS uses `zsh` by default:

```
nano ~/.zshrc
```

Add this line at the end:

```
export PATH="$PATH:$HOME/development/flutter/bin"
```

Press `Ctrl + O`, then Enter to save, then `Ctrl + X` to exit.

Reload your profile:

```
source ~/.zshrc
```

Verify it worked:

```
flutter --version
```

Expected output: `Flutter X.X.X • channel stable • ...`

### Step 3B: Install CocoaPods (Required for plugins)

Flutter plugins that use native macOS code require CocoaPods. Install it if you haven't already:

```
sudo gem install cocoapods
```

Verify installation:

```
pod --version
```

### Step 5: Install Android SDK (for Android development)

Flutter needs the Android SDK to build Android apps on macOS.

#### Option A: Minimal Setup (Recommended)

1. Create SDK directory:

```
mkdir -p ~/Library/Android/sdk
```

2. Download Android Command Line Tools from:
   [https://developer.android.com/studio#command-tools](https://developer.android.com/studio#command-tools)
   
   Download the macOS version.

3. Extract into the SDK folder:

```
cd ~/Downloads
unzip cmdline-tools-mac-XXXXX.zip
mkdir -p ~/Library/Android/sdk/cmdline-tools/latest
mv cmdline-tools/* ~/Library/Android/sdk/cmdline-tools/latest/
```

4. Set environment variables. Edit `~/.zshrc` again:

```
nano ~/.zshrc
```

Add these lines:

```
export ANDROID_SDK_ROOT=$HOME/Library/Android/sdk
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH="$PATH:$ANDROID_SDK_ROOT/cmdline-tools/latest/bin"
```

Reload:

```
source ~/.zshrc
```

5. Install required components:

```
sdkmanager "build-tools;latest"
sdkmanager "platforms;android-34"
sdkmanager "platform-tools"
```

#### Option B: If You Prefer GUI

Download Android Studio from [https://developer.android.com/studio](https://developer.android.com/studio). During setup, it will install the SDK automatically.

### Step 6: Accept Android Licenses

```
flutter doctor --android-licenses
```

Type `y` for each license prompt.

### Step 7: Verify Your Setup

```
flutter doctor
```

Expected output:

```
Doctor summary (to see all details, run flutter doctor -v):

[✓] Flutter (Channel stable, X.X.X)
[✓] Xcode - develop for iOS and macOS (Xcode X.X)
[✓] CocoaPods (version X.X.X)
[✓] Android toolchain - develop for Android devices (Android SDK X.X)
[✓] VS Code (version X.X.X)
```

**If you see red X marks, see the troubleshooting section below.**

### Step 8: Create Your First App

```
flutter create my_first_app
cd my_first_app
flutter run
```

On first run, Flutter builds a debug app, which takes 2-3 minutes. If successful, you'll see output indicating the build completed.

If no simulator or device is connected, you'll get a "no connected devices" error. That's fine—we'll cover device setup next.

---

### Optional: Target iOS, macOS, or Web

macOS developers have three additional platform options:

**For iOS apps (requires Xcode or Simulator):**

```
flutter config --enable-ios
flutter doctor
```

Then `flutter create --platforms=ios my_ios_app`.

Note: Building iOS apps requires Xcode (the full IDE), not just Command Line Tools. Download from the App Store if needed (~12 GB).

**For macOS desktop apps:**

```
flutter config --enable-macos
flutter doctor
```

Then `flutter create --platforms=macos my_desktop_app`.

**For web apps:**

```
flutter config --enable-web
flutter doctor
```

Then `flutter create --platforms=web my_web_app`.

</div>

---

## Next: Running on Devices or Simulators

Now that your environment is set up, you can:

- **Android:** Connect an Android phone via USB and run `flutter run`
- **iOS (macOS only):** Launch the iOS Simulator and run `flutter run`
- **Web:** Run `flutter run -d chrome` or any web browser
- **Windows/macOS desktop:** Run `flutter run` targeting your desktop

Each platform's device setup is covered in dedicated chapters.

---

## Troubleshooting

### "Command not found: flutter"

**Problem:** PowerShell/Terminal doesn't recognize the `flutter` command.

**Solution:**
- Verify Flutter is in your PATH: `echo $env:PATH` (Windows) or `echo $PATH` (macOS)
- Make sure you restarted PowerShell/Terminal after adding to PATH
- On macOS, run `source ~/.zshrc` to reload your shell profile

### "Android SDK not found"

**Problem:** `flutter doctor` shows red X for Android toolchain.

**Solution:**
- Verify `ANDROID_HOME` is set: `echo $env:ANDROID_HOME` (Windows) or `echo $ANDROID_HOME` (macOS)
- Ensure you ran the `sdkmanager` commands to install build-tools and platforms
- On Windows, try running from a fresh PowerShell window

### "Xcode Command Line Tools not installed" (macOS)

**Problem:** Flutter can't find development tools.

**Solution:**
```
xcode-select --install
```

Then wait for installation to complete and run `flutter doctor` again.

### "License not accepted" (Android)

**Problem:** `flutter doctor` shows "Android SDK licenses not accepted".

**Solution:**
```
flutter doctor --android-licenses
```

Type `y` for each prompt.

### App build fails with "No connected devices"

**Problem:** `flutter run` says no devices found.

**Solution:** This is normal if you haven't set up a device or emulator yet. 
- To use an Android Emulator, install Android Studio and create a virtual device, then run `flutter run`.
- Alternatively, connect a physical Android phone via USB (enable Developer Mode first).
- On macOS, launch the iOS Simulator: `open -a Simulator`, then `flutter run`.

### "Gradle build failed" or similar Android errors

**Problem:** App build crashes during the Android build process.

**Solution:**
1. Clean the project: `flutter clean`
2. Get dependencies: `flutter pub get`
3. Try building again: `flutter build apk` (Android) to see full error messages
4. Check that all `sdkmanager` packages are installed (build-tools, platforms)

### Unable to connect to simulator or emulator

**Problem:** Device/emulator not showing in `flutter devices`.

**Solution:**
- Make sure the device/emulator is running
- On Android: Emulator must be started before running `flutter run`
- On iOS: Simulator must be running (or start it with `open -a Simulator`)
- Try: `flutter clean` and `flutter pub get`, then `flutter run` again

---

**Still stuck?** Run `flutter doctor -v` for verbose output showing exactly what's missing, and refer to the official docs at [https://flutter.dev/docs/get-started/install](https://flutter.dev/docs/get-started/install).
