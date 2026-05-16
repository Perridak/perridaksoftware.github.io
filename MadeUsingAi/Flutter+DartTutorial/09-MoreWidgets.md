# More Widgets

This chapter has two parts. First, we'll learn how to create your own widgets—the foundation for building reusable, maintainable UI components. Second, we'll provide a reference guide to widgets from Flutter's toolkit that we missed or skimmed in the earlier Flutter Widgets chapter.

## Part 1: Creating Your Own Widgets

Every widget you use in Flutter is built from more basic widgets. At some point, you'll need to build something that doesn't exist in Flutter's toolkit, or you'll want to extract part of your UI into a reusable piece. Creating custom widgets teaches you how Flutter works and gives you the power to build exactly what your app needs.

### Understanding When to Create a Custom Widget

Before diving into how, understand when. You should create a custom widget when:

- You repeat the same widget pattern across multiple screens
- A widget in your UI is complex enough to warrant its own file
- You want to encapsulate logic and styling together
- You're building a component library for your team

Example: In the Markdown Notes app, `NoteCard` (the reusable note preview widget) is a perfect candidate for a custom widget. It combines layout, styling, and interaction logic.

### Creating a Custom Stateless Widget

A `StatelessWidget` is the simplest custom widget. It's immutable—once built, its properties never change.

**Step 1: Understand the Structure**

Every widget needs to extend either `StatelessWidget` or `StatefulWidget` and override the `build()` method:

```dart
class MyCustomWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Return the UI
  }
}
```

**Step 2: Build Your First Custom Widget**

Let's create a simple widget that displays a note preview:

```dart
class NoteCard extends StatelessWidget {
  final Note note;
  final VoidCallback onTap;

  const NoteCard({
    required this.note,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Card(
        margin: EdgeInsets.symmetric(vertical: 8, horizontal: 16),
        child: Padding(
          padding: EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                note.title,
                style: Theme.of(context).textTheme.titleLarge,
              ),
              SizedBox(height: 8),
              Text(
                note.content,
                maxLines: 2,
                overflow: TextOverflow.ellipsis,
                style: TextStyle(color: Colors.grey[600]),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

Key observations:

- The constructor accepts required parameters (`note`, `onTap`)
- It uses `const` to mark the constructor, enabling optimizations
- The `build()` method returns a widget tree
- It uses composition: `Card` wraps `Padding` wraps `Column`

**Step 3: Use Your Custom Widget**

Once defined, use it like any Flutter widget:

```dart
ListView.builder(
  itemCount: notes.length,
  itemBuilder: (context, index) {
    return NoteCard(
      note: notes[index],
      onTap: () => openNoteDetail(notes[index]),
    );
  },
)
```

### Creating a Custom Stateful Widget

A `StatefulWidget` can change over time. It's appropriate when your widget needs to maintain state or respond to user interaction internally.

**Example: A Collapsible Note Card**

```dart
class CollapsibleNoteCard extends StatefulWidget {
  final Note note;

  const CollapsibleNoteCard({required this.note});

  @override
  State<CollapsibleNoteCard> createState() => _CollapsibleNoteCardState();
}

class _CollapsibleNoteCardState extends State<CollapsibleNoteCard> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Column(
        children: [
          ListTile(
            title: Text(widget.note.title),
            trailing: IconButton(
              icon: Icon(_isExpanded ? Icons.expand_less : Icons.expand_more),
              onPressed: () {
                setState(() => _isExpanded = !_isExpanded);
              },
            ),
          ),
          if (_isExpanded)
            Padding(
              padding: EdgeInsets.all(16),
              child: Text(widget.note.content),
            ),
        ],
      ),
    );
  }
}
```

Key differences from stateless:

- Extends `StatefulWidget` with a `createState()` method
- State is held in `_CollapsibleNoteCardState`
- Use `widget.` to access properties from the widget
- Call `setState()` to update the UI when state changes
- The underscore prefix (`_CollapsibleNoteCardState`) is Dart convention for private classes

**Understanding the Split**

The widget itself (`CollapsibleNoteCard`) is immutable. The state (`_CollapsibleNoteCardState`) is mutable. This split might seem odd, but it ensures clean separation: the widget describes what to display, the state manages how it changes.

### Creating a Custom Painter Widget (CustomPaint)

For custom graphics beyond what widgets provide, use `CustomPaint`. This is advanced but powerful.

**Example: A Simple Progress Ring**

```dart
class ProgressRing extends StatelessWidget {
  final double progress; // 0.0 to 1.0

  const ProgressRing({required this.progress});

  @override
  Widget build(BuildContext context) {
    return CustomPaint(
      painter: ProgressRingPainter(progress),
      size: Size(100, 100),
    );
  }
}

class ProgressRingPainter extends CustomPainter {
  final double progress;

  ProgressRingPainter(this.progress);

  @override
  void paint(Canvas canvas, Size size) {
    final center = Offset(size.width / 2, size.height / 2);
    final radius = size.width / 2;

    // Draw background ring
    canvas.drawCircle(
      center,
      radius,
      Paint()
        ..color = Colors.grey[300]!
        ..strokeWidth = 4
        ..style = PaintingStyle.stroke,
    );

    // Draw progress ring
    final sweep = 2 * 3.14159 * progress; // 2π * progress
    canvas.drawArc(
      Rect.fromCircle(center: center, radius: radius),
      -3.14159 / 2, // Start at top
      sweep,
      false,
      Paint()
        ..color = Colors.blue
        ..strokeWidth = 4
        ..style = PaintingStyle.stroke,
    );
  }

  @override
  bool shouldRepaint(ProgressRingPainter oldDelegate) {
    return oldDelegate.progress != progress;
  }
}
```

`CustomPaint` requires two things:

1. **A painter** — extends `CustomPainter` and implements `paint()` to draw
2. **shouldRepaint()** — returns true if the widget needs to redraw (optimization)

This approach is for truly custom graphics. For most UI needs, composition (combining existing widgets) is simpler and preferred.

### Widget Composition Best Practices

When building custom widgets, prefer composition over building from scratch:

**Compose existing widgets:**
```dart
class NotePreview extends StatelessWidget {
  final Note note;
  
  const NotePreview({required this.note});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: EdgeInsets.all(16),
      decoration: BoxDecoration(
        border: Border.all(color: Colors.grey),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(note.title, style: TextStyle(fontWeight: FontWeight.bold)),
          SizedBox(height: 8),
          Text(note.content),
        ],
      ),
    );
  }
}
```

This is simpler than custom painting and handles responsiveness automatically.

### Extracting Widgets for Clarity

If your `build()` method exceeds 50 lines or contains nested columns/rows, extract sections into separate widgets:

**Before:**
```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: Text('Notes')),
    body: Column(
      children: [
        Container(/*header styling*/),
        ListView.builder(/*list*/),
        Container(/*footer styling*/),
      ],
    ),
  );
}
```

**After:**
```dart
@override
Widget build(BuildContext context) {
  return Scaffold(
    appBar: AppBar(title: Text('Notes')),
    body: Column(
      children: [
        _buildHeader(),
        _buildList(),
        _buildFooter(),
      ],
    ),
  );
}

Widget _buildHeader() => Container(/*header styling*/);
Widget _buildList() => ListView.builder(/*list*/);
Widget _buildFooter() => Container(/*footer styling*/);
```

Or extract into separate widget classes for maximum reusability.

---

## Part 2: Widget Reference Guide

Flutter's widget catalog is extensive. This section covers widgets we haven't fully explored yet, organized by category. Each widget includes its purpose, when to use it, key properties, and a simple example.

### Scrolling Widgets

**SingleChildScrollView**

Scrolls a single child widget. Use when you have one widget that might overflow the screen.

Key properties: `scrollDirection`, `reverse`, `padding`

```dart
SingleChildScrollView(
  child: Column(
    children: [/*many widgets*/],
  ),
)
```

**ListView and ListView.builder**

Scrolls multiple children. Use `.builder` for long lists (lazy loading). Both covered in earlier chapter; included for completeness.

**GridView and GridView.builder**

Lays out children in a grid. Use `GridView.count` for fixed columns, `GridView.builder` for lazy-loaded grids.

Key properties: `crossAxisCount`, `mainAxisSpacing`, `crossAxisSpacing`

```dart
GridView.count(
  crossAxisCount: 2,
  children: [/*widgets*/],
)
```

**PageView**

Displays pages that users swipe between (carousel). Useful for onboarding flows or image galleries.

Key properties: `children`, `onPageChanged`

```dart
PageView(
  onPageChanged: (index) => setState(() => currentPage = index),
  children: [Page1(), Page2(), Page3()],
)
```

**CustomScrollView and Slivers**

Advanced scrolling with complex behaviors (e.g., collapsing app bars, pinned headers). Uses `Sliver` widgets instead of regular children.

```dart
CustomScrollView(
  slivers: [
    SliverAppBar(title: Text('App'), floating: true),
    SliverList(delegate: SliverChildListDelegate([/*items*/])),
  ],
)
```

### Interaction and Input Widgets

**GestureDetector**

Detects gestures (taps, drags, long presses). Covered in earlier chapter; mentioned here as a foundational interaction widget.

**InkWell**

Like `GestureDetector` but adds Material ripple effects. Preferred for Material design.

Key properties: `onTap`, `onLongPress`, `splashColor`, `highlightColor`

```dart
InkWell(
  onTap: () => print('Tapped'),
  child: Padding(
    padding: EdgeInsets.all(16),
    child: Text('Tap me'),
  ),
)
```

**Dismissible**

Allows users to swipe/drag to dismiss. Commonly used for swipe-to-delete.

Key properties: `key`, `onDismissed`, `background`, `secondaryBackground`

```dart
Dismissible(
  key: Key(item.id),
  onDismissed: (_) => deleteItem(item.id),
  background: Container(color: Colors.red),
  child: ListTile(title: Text(item.title)),
)
```

**Draggable and DragTarget**

Enables drag-and-drop. `Draggable` is the source, `DragTarget` is the destination.

```dart
Draggable<String>(
  data: 'item',
  child: Container(child: Text('Drag me')),
  feedback: Container(child: Text('Dragging...')),
)

DragTarget<String>(
  onAccept: (data) => print('Dropped: $data'),
  builder: (context, candidateData, rejectedData) =>
    Container(child: Text('Drop here')),
)
```

### Animation Widgets

**AnimatedBuilder**

Builds a widget in response to an animation. Use when you have complex animations tied to a single AnimationController.

Key properties: `animation`, `builder`

```dart
AnimatedBuilder(
  animation: controller,
  builder: (context, child) => Transform.rotate(
    angle: controller.value * 2 * 3.14159,
    child: Icon(Icons.refresh),
  ),
)
```

**AnimatedContainer, AnimatedOpacity, AnimatedPositioned**

Implicit animations that animate between property changes. Use when you want simple property animations without explicit controller.

```dart
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  width: _isExpanded ? 200 : 100,
  height: _isExpanded ? 200 : 100,
  color: _isExpanded ? Colors.blue : Colors.red,
  child: Text('Animate me'),
)
```

**TweenAnimationBuilder**

Animates a value over time. Use for specific numeric animations.

```dart
TweenAnimationBuilder<double>(
  tween: Tween(begin: 0, end: 1),
  duration: Duration(seconds: 2),
  builder: (context, value, child) => Opacity(
    opacity: value,
    child: child,
  ),
  child: Text('Fade in'),
)
```

### Styling and Theming Widgets

**DecoratedBox**

Applies decoration (border, shadow, color) to a child. More flexible than just using `Container`.

```dart
DecoratedBox(
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8),
    boxShadow: [BoxShadow(blurRadius: 4)],
  ),
  child: Text('Decorated'),
)
```

**ClipRRect, ClipOval, ClipPath**

Clips children to shapes. Use for rounded corners, circles, or custom shapes.

```dart
ClipRRect(
  borderRadius: BorderRadius.circular(8),
  child: Image.asset('image.png'),
)
```

**Opacity**

Makes a widget partially transparent. Covered earlier; included for reference.

**Transform**

Applies transformations (rotation, scaling, translation) to a child.

```dart
Transform.rotate(
  angle: 0.5, // radians
  child: Icon(Icons.star),
)

Transform.scale(
  scale: 1.5,
  child: Text('Bigger'),
)
```

### Layout Helpers

**AspectRatio**

Constrains a child to a specific aspect ratio.

```dart
AspectRatio(
  aspectRatio: 16 / 9,
  child: Image.asset('landscape.png'),
)
```

**FractionallySizedBox**

Sizes a child as a fraction of the parent.

```dart
FractionallySizedBox(
  widthFactor: 0.5, // 50% of parent width
  heightFactor: 0.8,
  child: Container(color: Colors.blue),
)
```

**LimitedBox**

Constrains a child's size when it's in an unbounded context (e.g., inside a ListView).

```dart
LimitedBox(
  maxHeight: 100,
  child: Container(),
)
```

**Spacer**

Fills available space. Useful in Rows and Columns.

```dart
Row(
  children: [
    Text('Left'),
    Spacer(), // Pushes next widget to the right
    Text('Right'),
  ],
)
```

### Async and Loading Widgets

**FutureBuilder**

Builds a widget based on the state of a Future. Covered in State Management chapter; included for reference.

**StreamBuilder**

Like `FutureBuilder` but for Streams. Rebuilds whenever the stream emits a new value.

```dart
StreamBuilder<int>(
  stream: countStream,
  builder: (context, snapshot) {
    if (snapshot.hasData) {
      return Text('Count: ${snapshot.data}');
    }
    return CircularProgressIndicator();
  },
)
```

### Other Essential Widgets

**Tooltip**

Shows a label when the user hovers or long-presses.

```dart
Tooltip(
  message: 'This is a button',
  child: IconButton(icon: Icon(Icons.help), onPressed: () {}),
)
```

**PopupMenuButton**

Displays a dropdown menu.

```dart
PopupMenuButton(
  itemBuilder: (context) => [
    PopupMenuItem(value: 1, child: Text('Option 1')),
    PopupMenuItem(value: 2, child: Text('Option 2')),
  ],
  onSelected: (value) => print('Selected: $value'),
)
```

**ExpansionTile**

A tile that expands to reveal more content.

```dart
ExpansionTile(
  title: Text('Expand me'),
  children: [Text('Hidden content')],
)
```

**AlertDialog**

Shows a modal dialog for important messages.

```dart
showDialog(
  context: context,
  builder: (context) => AlertDialog(
    title: Text('Confirm'),
    content: Text('Are you sure?'),
    actions: [
      TextButton(onPressed: () => Navigator.pop(context), child: Text('Cancel')),
      TextButton(onPressed: () => confirm(), child: Text('Yes')),
    ],
  ),
)
```

**BottomSheet**

Shows a sheet that slides up from the bottom.

```dart
showModalBottomSheet(
  context: context,
  builder: (context) => Container(
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [Text('Bottom sheet content')],
    ),
  ),
)
```

---

## Choosing the Right Widget

With hundreds of widgets available, how do you choose? Start with these principles:

1. **Prefer composition over custom painting.** Build from simpler widgets when possible.
2. **Use the most specific widget for your need.** `InkWell` instead of `GestureDetector` for Material, `Dismissible` for swipe-to-delete.
3. **Read widget documentation.** Flutter's API docs explain exactly what each widget does.
4. **Experiment.** The best way to understand widgets is to build with them.

As you build more apps, you'll develop intuition for which widget solves which problem. The widgets you use most often will become familiar friends.
