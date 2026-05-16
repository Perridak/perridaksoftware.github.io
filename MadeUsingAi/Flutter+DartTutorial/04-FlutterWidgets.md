# Flutter Widgets

In Flutter, everything is a widget. A widget is an immutable description of part of your user interface. Unlike other UI frameworks that separate structure from styling, Flutter widgets combine both—they are self-contained, reusable components that describe what a piece of your UI should look like.

This chapter covers Flutter's essential widgets in the order you'd naturally use them when building a real app. We'll start with app structure and navigation, then build layouts, add interactivity, apply styling, and handle async operations. By the end, you'll be able to construct a complete, functional mobile UI without relying on drag-and-drop tools.

## Material vs. Cupertino: Design Systems

Flutter ships with two complete design systems:

**Material Design** implements Google's Material Design 3 specification. It's the default and recommended choice for most apps. Material provides a consistent, modern look across Android, iOS, web, and desktop. Components include `AppBar`, `FloatingActionButton`, `ElevatedButton`, `Card`, `SnackBar`, and hundreds more. If you're new to Flutter, start with Material.

**Cupertino** implements Apple's Human Interface Guidelines for iOS and macOS. Use Cupertino when building exclusively for Apple platforms or when you want the exact iOS/macOS native look. Cupertino components include `CupertinoNavigationBar`, `CupertinoButton`, `CupertinoSwitch`, and `CupertinoAlertDialog`. They look and behave like native iOS controls.

You can use both in the same app by checking the platform at runtime:

```dart
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:flutter/cupertino.dart';

Widget getPlatformButton() {
  if (Platform.isIOS) {
    return CupertinoButton(
      onPressed: () {},
      child: Text('iOS Button'),
    );
  } else {
    return ElevatedButton(
      onPressed: () {},
      child: Text('Android Button'),
    );
  }
}
```

For this chapter, we focus on Material Design, as it's the most common choice for cross-platform apps.

## Core Widget Concepts

### Stateless vs. Stateful Widgets

A `StatelessWidget` is immutable and cannot change. Once created, it displays the same UI every time, based only on its constructor parameters. Use `StatelessWidget` for UI that doesn't respond to user interaction or change over time.

```dart
class Greeting extends StatelessWidget {
  final String name;

  const Greeting({required this.name});

  @override
  Widget build(BuildContext context) {
    return Text('Hello, $name!');
  }
}
```

A `StatefulWidget` manages mutable state and rebuilds when that state changes. Use `StatefulWidget` when your UI needs to respond to user input, timers, animations, or data changes. The widget itself is immutable, but its associated `State` object holds mutable data.

```dart
class Counter extends StatefulWidget {
  @override
  State<Counter> createState() => _CounterState();
}

class _CounterState extends State<Counter> {
  int count = 0;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text('Count: $count'),
        ElevatedButton(
          onPressed: () {
            setState(() => count++);
          },
          child: Text('Increment'),
        ),
      ],
    );
  }
}
```

**Best practice:** Start with `StatelessWidget`. Only use `StatefulWidget` when you genuinely need mutable state. As your app grows, consider moving state management to dedicated patterns covered in the State Management chapter.

### The `const` Keyword and Performance

Use `const` constructors whenever possible. When a widget is declared as `const`, Flutter reuses the same instance across rebuilds, avoiding unnecessary reconstruction work. This is especially important for widgets that don't change.

```dart
// Good: const avoids rebuilds
const Text('Static label')

// Less efficient: rebuilds even though content is the same
Text('Static label')

// Also good: const for unchanging child widgets
const SizedBox(
  width: 100,
  height: 100,
  child: Icon(Icons.star),
)
```

Many built-in widgets have `const` constructors. Use them when the widget's properties won't change.

### BuildContext

`BuildContext` is a handle to the location of a widget in the widget tree. It's passed to the `build()` method and allows you to access inherited data, theme information, and the navigator. Think of it as a reference that says "you are here in the widget tree."

```dart
@override
Widget build(BuildContext context) {
  // Access the current theme
  var theme = Theme.of(context);
  
  // Check device size
  var screenWidth = MediaQuery.of(context).size.width;
  
  // Navigate to a new screen
  Navigator.push(context, MaterialPageRoute(builder: (_) => NextPage()));
  
  return Container();
}
```

## Building Your App Structure: MaterialApp and Scaffold

### MaterialApp

Every Flutter app starts with `MaterialApp`. It's your root widget and configures your entire app's theme, title, home screen, and routing.

```dart
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'My App',
      theme: ThemeData(
        useMaterial3: true,
        primarySwatch: Colors.blue,
      ),
      home: HomeScreen(),
    );
  }
}
```

### Scaffold

`Scaffold` provides the basic Material Design visual structure for a screen. It holds your `AppBar`, `Drawer`, `BottomNavigationBar`, `FloatingActionButton`, and main content area. Most screens in your app will use `Scaffold`.

```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: Text('Home')),
    drawer: Drawer(child: MyDrawerContent()),
    body: Center(child: Text('Main content')),
    floatingActionButton: FloatingActionButton(
      onPressed: () {},
      child: Icon(Icons.add),
    ),
  );
}
```

`Scaffold` automatically handles:
- Padding under the system status bar
- AppBar positioned at the top
- Body content below the AppBar
- Drawer slides in from the side
- FloatingActionButton positioned in the corner
- SnackBars displayed at the bottom

Without `Scaffold`, you'd manually position all these elements. Use it.

### AppBar

The `AppBar` sits at the top of your screen and typically displays your app title, navigation controls, and actions. It's one of the most important components in mobile apps because users expect navigation options at the top.

```dart
AppBar(
  title: Text('My App'),
  centerTitle: true,              // Center the title
  elevation: 4,                   // Shadow depth
  backgroundColor: Colors.blue,
  foregroundColor: Colors.white,  // Text and icon color
  leading: Icon(Icons.menu),      // Left-side icon (usually hamburger)
  actions: [
    IconButton(
      icon: Icon(Icons.search),
      onPressed: () => print('Search tapped'),
    ),
    IconButton(
      icon: Icon(Icons.settings),
      onPressed: () => print('Settings tapped'),
    ),
  ],
)
```

**When to use AppBar:**
- Display your app name or current page title
- Show navigation controls (back button, menu icon)
- Display action buttons (search, settings, share)
- Provide quick access to common functions

The `leading` widget is usually `null` (auto-generates a back button if there's a previous screen) or an icon for opening the drawer. The `actions` list holds buttons on the right side.

### Drawer

A `Drawer` slides in from the left side (or right, if you use `endDrawer`) and provides navigation to different sections of your app. It's the "hamburger menu" users expect on mobile.

```dart
Scaffold(
  appBar: AppBar(title: Text('Home')),
  drawer: Drawer(
    child: ListView(
      padding: EdgeInsets.zero,
      children: [
        DrawerHeader(
          decoration: BoxDecoration(color: Colors.blue),
          child: Text('Navigation', style: TextStyle(color: Colors.white)),
        ),
        ListTile(
          leading: Icon(Icons.home),
          title: Text('Home'),
          onTap: () => Navigator.pop(context), // Close drawer
        ),
        ListTile(
          leading: Icon(Icons.settings),
          title: Text('Settings'),
          onTap: () {
            Navigator.pop(context);
            Navigator.push(context, MaterialPageRoute(builder: (_) => SettingsScreen()));
          },
        ),
        ListTile(
          leading: Icon(Icons.info),
          title: Text('About'),
          onTap: () => Navigator.pop(context),
        ),
      ],
    ),
  ),
  body: Center(child: Text('Main content')),
)
```

**When to use Drawer:**
- Provide navigation to multiple sections of your app
- Hide menu options to keep the main content area clean
- Organize app features hierarchically

The drawer automatically gets a hamburger icon in the AppBar's leading position. When users tap it, the drawer slides open. Tap an item to navigate, then call `Navigator.pop(context)` to close the drawer.

## Basic Building Blocks

### Text and TextStyle

`Text` displays readable text on screen. Most UIs consist primarily of text.

```dart
// Simple text
Text('Hello, World!')

// Styled text
Text(
  'Large bold text',
  style: TextStyle(
    fontSize: 24,
    fontWeight: FontWeight.bold,
    color: Colors.blue,
  ),
)

// Multiple styles in one widget
RichText(
  text: TextSpan(
    children: [
      TextSpan(text: 'Bold ', style: TextStyle(fontWeight: FontWeight.bold)),
      TextSpan(text: 'normal ', style: TextStyle(fontWeight: FontWeight.normal)),
      TextSpan(text: 'italic', style: TextStyle(fontStyle: FontStyle.italic)),
    ],
  ),
)
```

`Text` is a `StatelessWidget`—it doesn't respond to taps. To make text tappable, wrap it in `GestureDetector` or `InkWell`.

### Icon

`Icon` displays vector graphics from Material's icon set. Icons are lightweight, scalable, and look great at any size.

```dart
Icon(Icons.home)                              // Default size (24)
Icon(Icons.favorite, color: Colors.red)      // Red heart
Icon(Icons.settings, size: 32)                // Larger icon
Icon(Icons.shopping_cart, color: Colors.blue, size: 28)
```

Flutter includes hundreds of Material icons. Browse them at the [Material Icons documentation](https://fonts.google.com/icons).

### Container

`Container` is a catch-all widget for styling and positioning. It combines padding, margin, background color, border, and child alignment into one widget. Use it when you need to style a piece of your UI.

```dart
Container(
  width: 200,
  height: 100,
  padding: EdgeInsets.all(16),              // Space inside
  margin: EdgeInsets.symmetric(vertical: 8), // Space outside
  decoration: BoxDecoration(
    color: Colors.blue,
    border: Border.all(color: Colors.black, width: 2),
    borderRadius: BorderRadius.circular(8),
  ),
  child: Text('Styled container'),
)
```

**When to use Container:**
- Add background color to a widget
- Add padding or margin
- Add a border or rounded corners
- Combine multiple styling properties

**Watch out for:** `Container` has no `const` constructor (it's mutable). For simple fixed-size boxes or spacing, use `SizedBox` instead. It's more efficient and has a `const` constructor.

### SizedBox

`SizedBox` creates a box with a specific size, or adds fixed spacing between widgets. It's simpler and more efficient than `Container` when you only need to control size.

```dart
// Create a 200x100 box
SizedBox(width: 200, height: 100, child: myWidget)

// Add vertical spacing between widgets
Column(
  children: [
    Text('Item 1'),
    SizedBox(height: 16),  // 16 pixels of space
    Text('Item 2'),
  ],
)

// Add horizontal spacing
Row(
  children: [
    Icon(Icons.email),
    SizedBox(width: 8),    // 8 pixels of space
    Text('user@example.com'),
  ],
)
```

Prefer `SizedBox` over `Container` for spacing and sizing. It's more performant because it has a `const` constructor.

### Padding

`Padding` adds space inside a widget. Use it when you want to create space between a widget and its edges (or between a widget and its content).

```dart
Padding(
  padding: EdgeInsets.all(16),  // 16 pixels on all sides
  child: Text('Padded text'),
)

Padding(
  padding: EdgeInsets.symmetric(horizontal: 16, vertical: 8),
  child: Text('Custom padding'),
)

Padding(
  padding: EdgeInsets.only(left: 16, top: 8),
  child: Text('Padding on specific sides'),
)
```

`Padding` is cleaner than wrapping everything in `Container` when you only need padding.

## Layout Widgets: Building Multi-Widget UIs

Layout widgets arrange multiple children. This is where you spend most of your Flutter time.

### Row: Arrange Widgets Horizontally

`Row` arranges widgets in a single horizontal line (left to right). Use it when you want to display widgets side-by-side, like an icon next to text, or buttons in a row.

```dart
Row(
  children: [
    Icon(Icons.email),
    SizedBox(width: 8),
    Text('user@example.com'),
  ],
)
```

By default, `Row` sizes itself to fit its children and doesn't expand. Control its behaviour with `mainAxisAlignment` (horizontal) and `crossAxisAlignment` (vertical):

```dart
Row(
  mainAxisAlignment: MainAxisAlignment.spaceBetween,  // Space items evenly
  crossAxisAlignment: CrossAxisAlignment.center,       // Vertically centre
  children: [
    Text('Left'),
    Text('Right'),
  ],
)
```

**Common alignments:**
- `MainAxisAlignment.start` — Pack items to the left
- `MainAxisAlignment.end` — Pack items to the right
- `MainAxisAlignment.center` — Pack items in the centre
- `MainAxisAlignment.spaceEvenly` — Equal space between and around items
- `MainAxisAlignment.spaceBetween` — Equal space between items (none around edges)
- `CrossAxisAlignment.stretch` — Expand items to fill available vertical space

**When to use Row:**
- Display an icon with text next to it
- Place buttons horizontally
- Show a horizontal list of items
- Create two-column layouts (with Expanded)

### Column: Arrange Widgets Vertically

`Column` arranges widgets in a single vertical line (top to bottom). Use it for most page layouts—headers, content, buttons.

```dart
Column(
  children: [
    Text('Title', style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold)),
    SizedBox(height: 8),
    Text('Subtitle'),
    SizedBox(height: 16),
    ElevatedButton(onPressed: () {}, child: Text('Action')),
  ],
)
```

`Column` controls spacing and alignment the same way as `Row`, but with vertical (`mainAxisAlignment`) and horizontal (`crossAxisAlignment`) directions swapped:

```dart
Column(
  mainAxisAlignment: MainAxisAlignment.start,       // Top alignment
  crossAxisAlignment: CrossAxisAlignment.stretch,   // Full width
  children: [
    Text('Item 1'),
    Text('Item 2'),
  ],
)
```

**When to use Column:**
- Build most page layouts
- Stack text, buttons, and other widgets vertically
- Create forms with fields stacked vertically

### Flex and Expanded: Divide Available Space

`Flex` is the base for both `Row` and `Column`. Use `Expanded` to make a child take up a proportional share of available space.

```dart
Row(
  children: [
    Expanded(
      flex: 1,
      child: Container(color: Colors.red, height: 100),
    ),
    Expanded(
      flex: 2,
      child: Container(color: Colors.blue, height: 100),
    ),
    // Red takes 1 part, blue takes 2 parts
    // Together they fill the row
  ],
)
```

**When to use Expanded:**
- Make widgets fill available space in a Row or Column
- Create responsive layouts that adapt to screen size
- Distribute space proportionally among multiple widgets

### Stack: Layer Widgets

`Stack` lets you layer widgets on top of each other. The first child in the list appears at the bottom, the last at the top.

```dart
Stack(
  children: [
    Container(width: 200, height: 200, color: Colors.blue),
    Positioned(
      top: 10,
      right: 10,
      child: Container(width: 50, height: 50, color: Colors.red),
    ),
    Positioned(
      bottom: 0,
      left: 0,
      right: 0,
      child: Container(height: 50, color: Colors.green),
    ),
  ],
)
```

Use `Positioned` to place children at exact positions. Omit `Positioned` to place a widget at the default position (top-left). You can position from top/bottom and left/right:

```dart
Positioned(
  top: 20,
  left: 20,
  child: Text('Top-left'),
)

Positioned(
  bottom: 20,
  right: 20,
  child: Text('Bottom-right'),
)
```

**When to use Stack:**
- Create floating buttons or badges
- Layer a gradient over an image
- Overlay text on images
- Build complex custom layouts

### Wrap: Layout That Wraps to Next Line

`Wrap` is like `Row` or `Column`, but wraps to the next line when it runs out of space. Use it for flexible layouts like tag clouds or button groups that should reflow on small screens.

```dart
Wrap(
  spacing: 8,      // Space between items horizontally
  runSpacing: 8,   // Space between rows
  children: [
    Chip(label: Text('Tag 1')),
    Chip(label: Text('Tag 2')),
    Chip(label: Text('Tag 3')),
    Chip(label: Text('Tag 4')),
    // Wraps to next line if needed
  ],
)
```

**When to use Wrap:**
- Display tags or chips that reflow
- Show button groups that wrap
- Create flexible grids without defining columns

### ListView: Scrollable List

`ListView` displays a scrollable list of widgets. Use it when you have more content than fits on screen.

```dart
ListView(
  children: [
    ListTile(title: Text('Item 1')),
    ListTile(title: Text('Item 2')),
    ListTile(title: Text('Item 3')),
  ],
)
```

For large lists (hundreds or thousands of items), use `ListView.builder` to build items lazily—only creating widgets for items visible on screen:

```dart
ListView.builder(
  itemCount: 1000,
  itemBuilder: (context, index) {
    return ListTile(title: Text('Item $index'));
  },
)
```

**When to use ListView:**
- Display more content than fits on one screen
- Show a list of items (messages, search results, notifications)
- Create scrollable forms or settings screens

**Watch out for:** Don't nest `ListView` inside a `Column` or `SingleChildScrollView`. They compete for space. Use `ListView` directly or use `SingleChildScrollView` with a `Column` if you have a small amount of content.

### GridView: Scrollable Grid

`GridView` displays items in a grid (rows and columns). Use it for image galleries, app launchers, or any grid-based layout.

```dart
GridView.count(
  crossAxisCount: 2,  // 2 columns
  children: List.generate(20, (index) {
    return Card(
      child: Center(child: Text('Item $index')),
    );
  }),
)
```

For dynamic layouts or large grids, use `GridView.builder`:

```dart
GridView.builder(
  gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 3,  // 3 columns
  ),
  itemCount: 100,
  itemBuilder: (context, index) {
    return Container(
      color: Colors.blue[((index + 1) * 100)],
      child: Center(child: Text('$index')),
    );
  },
)
```

**When to use GridView:**
- Display image galleries
- Show app icons or launcher screens
- Create grid-based product listings

### SingleChildScrollView

Make a single child scrollable when it's larger than the available space:

```dart
SingleChildScrollView(
  child: Column(
    children: [
      // Many widgets that might overflow screen height
      Text('Item 1'),
      SizedBox(height: 16),
      Text('Item 2'),
      SizedBox(height: 16),
      // ... more content
    ],
  ),
)
```

**When to use SingleChildScrollView:**
- Wrap a `Column` or `Row` when content might overflow
- Make a form scrollable
- Handle variable-height content

**Watch out for:** Don't use `SingleChildScrollView` with `ListView` or `GridView`—they handle scrolling internally and will cause errors if wrapped in another scrollable widget.

### Center and Align: Position Widgets

`Center` places a child in the middle of available space:

```dart
Center(child: Text('Centred text'))
```

`Align` positions a child within available space with more control:

```dart
Align(
  alignment: Alignment.bottomRight,
  child: Text('Bottom right'),
)

Align(
  alignment: Alignment.topCenter,
  child: Text('Top centre'),
)
```

**When to use Center/Align:**
- Centre content on a screen
- Position widgets at specific alignments
- Create balanced layouts

## Interactive Widgets

### Button Widgets

**ElevatedButton** for primary actions. It has a shadow and stands out:

```dart
ElevatedButton(
  onPressed: () => print('Pressed'),
  child: Text('Save'),
)
```

**TextButton** for low-emphasis actions. No background, just text:

```dart
TextButton(
  onPressed: () {},
  child: Text('Cancel'),
)
```

**OutlinedButton** for secondary actions. Has a border but no fill:

```dart
OutlinedButton(
  onPressed: () {},
  child: Text('Edit'),
)
```

**IconButton** for icon-only buttons. Perfect for AppBar actions:

```dart
IconButton(
  icon: Icon(Icons.favorite),
  onPressed: () => print('Liked'),
)
```

**FloatingActionButton** for the primary action on a screen. Sits in a corner:

```dart
FloatingActionButton(
  onPressed: () {},
  child: Icon(Icons.add),
)
```

**When to use each:**
- **ElevatedButton:** Primary action (Submit, Save, Confirm)
- **TextButton:** Secondary or low-emphasis action (Cancel, Learn More)
- **OutlinedButton:** Important secondary action (Delete, Edit)
- **IconButton:** Quick actions (Search, Settings, Close)
- **FloatingActionButton:** Single primary action on a screen (Create, Add, Share)

### TextField and TextFormField

`TextField` captures user input:

```dart
TextField(
  decoration: InputDecoration(
    hintText: 'Enter your name',
    labelText: 'Name',
    border: OutlineInputBorder(),
    prefixIcon: Icon(Icons.person),
  ),
  onChanged: (value) => print('Value: $value'),
)
```

`TextFormField` is used in forms. It supports validation and integrates with `Form`:

```dart
TextFormField(
  decoration: InputDecoration(labelText: 'Email'),
  validator: (value) {
    if (value == null || value.isEmpty) {
      return 'Email is required';
    }
    if (!value.contains('@')) {
      return 'Enter a valid email';
    }
    return null;
  },
)
```

**When to use TextField:**
- Search fields
- Single-line inputs
- Settings where validation isn't required

**When to use TextFormField:**
- Login forms
- Sign-up forms
- Any form with validation

### Checkbox and Switch

`Checkbox` lets users select multiple options:

```dart
bool isChecked = false;

Checkbox(
  value: isChecked,
  onChanged: (value) {
    setState(() => isChecked = value ?? false);
  },
)
```

`Switch` is for on/off toggles:

```dart
bool isEnabled = false;

Switch(
  value: isEnabled,
  onChanged: (value) {
    setState(() => isEnabled = value);
  },
)
```

**When to use Checkbox:**
- Allow users to select multiple items
- Agree to terms
- Filter options

**When to use Switch:**
- Toggle features on/off
- Enable/disable notifications
- Dark mode toggle

### Dropdown and DropdownButton

Let users select from a predefined list:

```dart
String selectedValue = 'Option 1';

DropdownButton<String>(
  value: selectedValue,
  items: ['Option 1', 'Option 2', 'Option 3']
    .map((e) => DropdownMenuItem(value: e, child: Text(e)))
    .toList(),
  onChanged: (value) {
    setState(() => selectedValue = value ?? 'Option 1');
  },
)
```

**When to use DropdownButton:**
- Select from a list of predefined options
- Filter by category
- Choose a sorting method

### GestureDetector and InkWell

`GestureDetector` detects taps and gestures on any widget:

```dart
GestureDetector(
  onTap: () => print('Tapped'),
  onLongPress: () => print('Long pressed'),
  onDoubleTap: () => print('Double tapped'),
  child: Container(width: 100, height: 100, color: Colors.blue),
)
```

`InkWell` is similar but provides Material Design ripple feedback:

```dart
InkWell(
  onTap: () => print('Tapped with ripple'),
  child: Text('Tap me'),
)
```

**When to use GestureDetector:**
- Detect custom gestures
- Respond to drags or swipes
- Make any widget tappable without ripple feedback

**When to use InkWell:**
- Make widgets tappable with visual feedback
- Show Material Design ripple animation
- Button-like widgets that aren't actual buttons

### Form and TextFormField

For complex forms with validation, use `Form` with `TextFormField`:

```dart
class LoginForm extends StatefulWidget {
  @override
  State<LoginForm> createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            decoration: InputDecoration(labelText: 'Email'),
            validator: (value) {
              if (value == null || value.isEmpty) return 'Email required';
              if (!value.contains('@')) return 'Invalid email';
              return null;
            },
          ),
          TextFormField(
            decoration: InputDecoration(labelText: 'Password'),
            obscureText: true,
            validator: (value) {
              if (value == null || value.length < 6) return 'Password too short';
              return null;
            },
          ),
          ElevatedButton(
            onPressed: () {
              if (_formKey.currentState!.validate()) {
                print('Form is valid');
              }
            },
            child: Text('Login'),
          ),
        ],
      ),
    );
  }
}
```

**When to use Form:**
- Validate multiple fields together
- Submit all form data at once
- Reset all fields simultaneously

## Styling and Theming

### Theme and ThemeData

Define a consistent colour scheme and text styles for your entire app:

```dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    primaryColor: Colors.blue,
    primarySwatch: Colors.blue,
    appBarTheme: AppBarTheme(
      backgroundColor: Colors.blue,
      foregroundColor: Colors.white,
    ),
    inputDecorationTheme: InputDecorationTheme(
      border: OutlineInputBorder(),
      filled: true,
      fillColor: Colors.grey[100],
    ),
  ),
  home: HomeScreen(),
)
```

Access theme data in your widgets:

```dart
@override
Widget build(BuildContext context) {
  var theme = Theme.of(context);
  return Text(
    'Themed text',
    style: TextStyle(color: theme.primaryColor),
  );
}
```

**When to use Theme:**
- Ensure consistent branding across your app
- Support light/dark modes
- Make the app easy to rebrand

### Card

A Material Design card with elevation and padding. Use it to group related content:

```dart
Card(
  elevation: 4,
  child: Padding(
    padding: EdgeInsets.all(16),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text('Card Title', style: TextStyle(fontWeight: FontWeight.bold)),
        SizedBox(height: 8),
        Text('Card content goes here'),
      ],
    ),
  ),
)
```

**When to use Card:**
- Group related content
- Create list items
- Display product information
- Make content visually distinct

### Opacity and Visibility

`Opacity` makes a widget partially transparent:

```dart
Opacity(
  opacity: 0.5,  // 50% transparent
  child: Text('Semi-transparent text'),
)
```

`Visibility` shows or hides a widget:

```dart
Visibility(
  visible: isVisible,
  child: Text('Visible or hidden'),
  replacement: SizedBox.shrink(),  // Show this instead
)
```

**When to use Opacity:**
- Fade out disabled content
- Highlight or dim elements
- Create visual hierarchy

**When to use Visibility:**
- Conditionally show/hide entire widgets
- Replace widgets based on state

## Displaying Images and Assets

### Image

Display images from various sources:

```dart
// From app assets
Image.asset('assets/my_image.png', width: 200, height: 200)

// From internet
Image.network('https://example.com/image.png')

// With error handling
Image.network(
  'https://example.com/image.png',
  errorBuilder: (context, error, stackTrace) {
    return Text('Failed to load image');
  },
  loadingBuilder: (context, child, loadingProgress) {
    if (loadingProgress == null) return child;
    return CircularProgressIndicator();
  },
)
```

**When to use Image:**
- Display user avatars
- Show product images
- Create image galleries

### Icon

Display Material icons:

```dart
Icon(Icons.home)
Icon(Icons.favorite, color: Colors.red, size: 32)
Icon(Icons.shopping_cart, color: Colors.blue)
```

**When to use Icon:**
- Navigation indicators
- Button icons
- Status indicators
- App branding

### ClipRRect and ClipOval

Clip widgets to rounded corners or ovals:

```dart
ClipRRect(
  borderRadius: BorderRadius.circular(8),
  child: Image.asset('image.png', width: 200, height: 200),
)

ClipOval(
  child: Image.asset('image.png', width: 100, height: 100),
)
```

**When to use Clipping:**
- Create circular avatars
- Round corners on images
- Create custom shapes

## Handling Async Operations

### FutureBuilder

Display different UI based on a Future's state (loading, completed, error):

```dart
FutureBuilder<String>(
  future: fetchData(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return CircularProgressIndicator();
    }
    if (snapshot.hasError) {
      return Text('Error: ${snapshot.error}');
    }
    return Text('Data: ${snapshot.data}');
  },
)

Future<String> fetchData() async {
  await Future.delayed(Duration(seconds: 2));
  return 'Loaded data';
}
```

**When to use FutureBuilder:**
- Load data from an API
- Wait for file operations
- Display loading states

### StreamBuilder

Handle streams of data that arrive over time:

```dart
StreamBuilder<int>(
  stream: countStream(),
  builder: (context, snapshot) {
    if (snapshot.hasData) {
      return Text('Count: ${snapshot.data}');
    }
    return CircularProgressIndicator();
  },
)

Stream<int> countStream() async* {
  for (int i = 1; i <= 100; i++) {
    await Future.delayed(Duration(milliseconds: 500));
    yield i;
  }
}
```

**When to use StreamBuilder:**
- Real-time data updates
- WebSocket connections
- Sensor data streams
- Animations that continuously update

## Understanding Constraints and Layout Rules

Flutter's layout system works with constraints. Understanding this is crucial for building responsive UIs.

**How it works:**
1. Parent passes size constraints to child (minimum and maximum width/height)
2. Child chooses its size within those constraints
3. Parent positions the child based on alignment

**Key insight:** A widget cannot be larger than its parent's constraints allow. A widget cannot decide to be 500 pixels wide if its parent only allows 300 pixels.

```dart
// Container expands to fill parent's constraints
Container(color: Colors.blue)  // Takes all available space

// SizedBox respects its size parameter (within constraints)
SizedBox(width: 100, height: 100)  // Always 100x100 (or less if parent constrains it)

// Expanded fills remaining space in Row/Column
Expanded(child: myWidget)  // Fills all available space
```

**Common gotcha:** `Center` doesn't constrain its child to any size—it just centres whatever size the child chooses. To centre a widget with a specific size, wrap it in `SizedBox` first:

```dart
// Correct
Center(
  child: SizedBox(width: 200, height: 200, child: myWidget),
)

// Wrong - myWidget can be any size
Center(child: myWidget)
```

**Important for responsive design:**
- Use `MediaQuery` to check screen size
- Use `Expanded` to fill available space proportionally
- Use constraints to force specific dimensions
- Test on different screen sizes

## Best Practices

1. **Use `const` constructors** wherever possible to avoid unnecessary rebuilds.
2. **Break large widgets into smaller ones.** If your `build()` method exceeds 50 lines, extract parts into separate widget classes.
3. **Avoid deep nesting.** Extract nested widgets into separate classes for readability and performance.
4. **Use `ListView.builder` and `GridView.builder`** for long lists to avoid building off-screen widgets.
5. **Prefer `StatelessWidget`** over `StatefulWidget`. Move state to dedicated patterns as your app grows.
6. **Understand constraints and layout rules.** Most layout bugs stem from misunderstanding how size flows through the widget tree.
7. **Use `Scaffold` for screen structure.** Don't manually position AppBar, Drawer, and body.
8. **Apply `Material` or `Cupertino` consistently.** Don't mix design systems randomly.
9. **Theme your app globally.** Define colours and styles in `ThemeData`, not in individual widgets.

## Additional Widgets

The Flutter ecosystem includes many more widgets beyond those covered in this chapter. The following are important but explored in greater detail in later chapters or the Widget Reference Appendix:

**State and Navigation (covered in later chapters):**
- `Navigator` — Handle screen navigation
- `StatefulWidget` lifecycle — Covered in State Management chapter
- `Provider` and state management widgets — Covered in State Management chapter
- `BottomNavigationBar` — Multi-screen navigation with tabs
- `Drawer` and navigation patterns — Covered in Routing & Navigation chapter

**Animation and Effects (Widget Reference Appendix):**
- `AnimatedContainer` — Animate property changes
- `AnimatedOpacity` — Animate opacity
- `Hero` — Animated transitions between screens
- `Transform` — Rotate, scale, skew widgets
- `CustomPaint` — Draw custom shapes
- `Shader` — Advanced visual effects

**Advanced Layout (Widget Reference Appendix):**
- Slivers (`SliverAppBar`, `SliverList`, `SliverGrid`) — Advanced scrolling
- `CustomMultiChildLayout` — Full control over child positioning
- `Flow` — Custom flow-based layout

**Accessibility (Widget Reference Appendix):**
- `Semantics` — Improve accessibility
- `MergeSemantics` — Manage semantic tree

**Platform-Specific Widgets (Widget Reference Appendix):**
- Cupertino-specific variants (navigation, buttons, etc.)
- Platform-adaptive widgets that look native on each OS

Refer to the [Flutter Widget Index](https://docs.flutter.dev/reference/widgets) for a complete reference of all available widgets.

---

## Hands-On Project

Ready to apply what you've learned? Work through the [Markdown Notes Project Part B](markdown-notes-project-part-b.html) to build a functional note-viewing interface in Flutter. You'll practise using Scaffold, AppBar, ListView, TextFields, buttons, and state management as you create a real, interactive app that users can navigate and use.
