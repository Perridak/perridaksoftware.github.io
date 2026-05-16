# Routing and Navigation

Routing is how your app moves between screens. Navigation is the art of doing it well—making transitions smooth, preserving state, and enabling users to move through your app intuitively.

This chapter teaches routing patterns and navigation architecture. We'll start with the fundamentals: how Flutter's Navigator works, how to pass data between screens, and how to structure navigation cleanly. Then we'll integrate what you learned about CRUD operations in the previous chapter, showing how routing patterns enable multi-screen CRUD workflows.

## The Problem: Managing Screen Transitions

In Part B and Part C of the Markdown Notes project, you likely navigated between screens using simple `Navigator.push()`:

```dart
Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => NoteDetailScreen(note: note)),
);
```

This works for small apps, but creates problems as complexity grows:

- **Hard-coded routes:** Each screen knows exactly what other screens exist and how to construct them. If you add a new parameter to a screen, you update every place that navigates to it.
- **No deep linking:** You can't open a specific screen via a URL (important for web and testing).
- **Unclear navigation flow:** Reading the code, it's hard to see what screens exist and how they relate.
- **State loss:** When you pop a screen, you lose information about what data should refresh.
- **Tight coupling:** Screens are tightly coupled to the screens they navigate to.

Good routing architecture solves these problems. It centralizes navigation logic and makes the app's structure clear.

## Understanding the Navigator

Before learning advanced patterns, you need to understand how Flutter's Navigator works fundamentally.

### The Navigation Stack

The Navigator manages a stack of routes (screens). Think of it like a stack of index cards:

```
Top of stack (visible):    Screen C (NoteDetailScreen)
                           Screen B (NoteListScreen)
Bottom of stack:           Screen A (HomeScreen)
```

When you call `Navigator.push()`, you add a card to the top. The new screen appears. When you call `Navigator.pop()`, you remove the top card, revealing what's underneath.

### Routes: Named vs. Anonymous

There are two ways to navigate:

**Anonymous routes** (what you've likely been doing):
```dart
Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => NoteDetailScreen(note: note)),
);
```

You directly construct the screen widget. The Navigator doesn't know the screen's name—it just knows how to build it.

**Named routes** (the better approach for larger apps):
```dart
Navigator.pushNamed(context, '/note-detail', arguments: note);
```

You reference a route by name. The Navigator looks up how to build that route in a centralized route table. The screen doesn't know who called it—it just knows it was called with certain arguments.

Named routes have advantages:
- Navigation is declarative (you name where you're going, not how to build it)
- Routes are defined in one place
- Deep linking is possible
- The app's structure is visible in the route table

### How Named Routes Work

In your `MaterialApp`, define a route table:

```dart
MaterialApp(
  routes: {
    '/': (context) => HomeScreen(),
    '/notes-list': (context) => NoteListScreen(),
    '/note-detail': (context) {
      final note = ModalRoute.of(context)!.settings.arguments as Note;
      return NoteDetailScreen(note: note);
    },
    '/create-note': (context) => CreateNoteScreen(),
  },
  home: HomeScreen(),
);
```

Now navigate by name:

```dart
Navigator.pushNamed(
  context,
  '/note-detail',
  arguments: note,
);
```

The Navigator looks up '/note-detail' in the route table, builds the screen, and passes the note as arguments.

### The Difference: Push vs. Replace vs. Pop

**Navigator.push()** adds a new screen to the stack. The previous screen is still there (underneath).
```dart
Navigator.push(context, MaterialPageRoute(builder: (_) => DetailsScreen()));
// Stack: [Home, Details] - Home is underneath
```

**Navigator.pop()** removes the top screen, revealing the one underneath.
```dart
Navigator.pop(context);
// Stack: [Home] - Details is removed
```

**Navigator.pushReplacementNamed()** replaces the top screen instead of adding a new one.
```dart
Navigator.pushReplacementNamed(context, '/new-screen');
// Stack: [Home, NewScreen] - OldScreen is replaced
```

Use `pushReplacement` when the previous screen shouldn't exist anymore. For example, after login succeeds, replace the login screen with the home screen—you don't want users to pop back to the login screen.

## Passing Data Between Screens

Routing becomes complex when you need to pass data. There are several approaches, each appropriate for different situations.

### Method 1: Constructor Parameters (Simple Cases)

For simple data and shallow navigation, pass parameters directly:

```dart
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (_) => NoteDetailScreen(note: selectedNote),
  ),
);
```

The detail screen receives the note in its constructor and can use it.

**Advantages:** Simple, direct, no ceremony.
**Disadvantages:** Hard-codes the navigation; doesn't scale to deep navigation trees.

### Method 2: Route Arguments (Named Routes)

For named routes, pass data via arguments:

```dart
// In the route table
'/note-detail': (context) {
  final note = ModalRoute.of(context)!.settings.arguments as Note;
  return NoteDetailScreen(note: note);
},

// When navigating
Navigator.pushNamed(
  context,
  '/note-detail',
  arguments: note,
);
```

The screen retrieves its arguments from `ModalRoute.of(context)?.settings.arguments`.

**Advantages:** Named routes are cleaner; decouples navigation from screen construction.
**Disadvantages:** Requires casting arguments; doesn't prevent navigation errors if arguments are wrong type.

### Method 3: State Management (Complex Cases)

For complex data that multiple screens need, use your state manager (Provider) instead of passing through routes:

```dart
// Don't pass the note—screens read it from Provider
Navigator.pushNamed(context, '/note-detail');

// In NoteDetailScreen, read from Provider
class NoteDetailScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final note = context.watch<NotesProvider>().findNoteByTitle(
      ModalRoute.of(context)!.settings.arguments as String, // Just pass title
    );
    // ... rest of screen
  }
}
```

This approach separates navigation concerns from data concerns. Routes pass minimal information (IDs, keys); screens fetch full data from state management.

**Advantages:** Scales to complex apps; state is centralized; screens are decoupled.
**Disadvantages:** Requires understanding state management.

### Returning Data from a Screen

When you pop a screen, you can return data:

```dart
// In the detail screen, when the user is done editing
Navigator.pop(context, updatedNote);

// In the calling screen, capture the result
final result = await Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => EditScreen()),
);

if (result != null) {
  // User returned data
  print('Edited note: $result');
}
```

**Important:** With state management, you usually don't need this. The detail screen updates the note via the provider, and the list screen watches the provider for changes. Data flows through the provider, not through Navigator return values.

## Navigation Architecture: GoRouter

For larger apps, managing routes with a simple route table becomes unwieldy. `GoRouter` is a package that provides a more powerful routing system:

```dart
final router = GoRouter(
  routes: [
    GoRoute(
      path: '/',
      builder: (context, state) => const HomeScreen(),
      routes: [
        GoRoute(
          path: 'notes/:id',
          builder: (context, state) {
            final id = state.pathParameters['id']!;
            return NoteDetailScreen(noteId: id);
          },
        ),
      ],
    ),
  ],
);

// Use GoRouter in your app
MaterialApp.router(
  routerConfig: router,
);

// Navigate with GoRouter
context.go('/notes/$noteId');
```

GoRouter advantages:
- URL-based routing (works on web, enables deep linking)
- Hierarchical route structure
- Route guards (check permissions before navigating)
- Cleaner than manual Navigator management

However, for learning purposes and smaller apps, the built-in Navigator and named routes are sufficient.

## Understanding Navigation Context

Navigation happens within a `BuildContext`. This is important: not every context can navigate. The context must be from a widget that's a descendant of the `Navigator` (which is created by `MaterialApp`).

A common error:

```dart
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: HomeScreen(),
    );
  }
}

class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        Navigator.push(context, ...); // Works - context is under MaterialApp
      },
      child: Text('Go to next'),
    );
  }
}
```

This works because `HomeScreen` is a descendant of `MaterialApp`, which contains the Navigator.

If you try to navigate from `MyApp` itself, it fails:

```dart
class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: ElevatedButton(
        onPressed: () {
          Navigator.push(context, ...); // Fails - context is MyApp, not under Navigator
        },
        child: Text('Go to next'),
      ),
    );
  }
}
```

The context is from `MyApp`, which is the parent of the Navigator, not a descendant. The Navigator doesn't exist yet.

## CRUD Operations Across Screens

Now we integrate what you learned in the State Management chapter. Routing and CRUD work together—routes move users between screens, and CRUD operations happen within those screens.

### READ: Navigating to a Detail Screen

When a user taps a note in the list, you navigate to a detail screen to read its full content:

```dart
// In NoteListScreen
Consumer<NotesProvider>(
  builder: (context, notesProvider, child) {
    return ListView.builder(
      itemCount: notesProvider.notes.length,
      itemBuilder: (context, index) {
        final note = notesProvider.notes[index];
        return ListTile(
          title: Text(note.title),
          onTap: () {
            // Navigate to detail screen, passing the note title
            Navigator.pushNamed(
              context,
              '/note-detail',
              arguments: note.title, // Pass minimal data
            );
          },
        );
      },
    );
  },
)

// In route table
'/note-detail': (context) {
  final title = ModalRoute.of(context)!.settings.arguments as String;
  return NoteDetailScreen(noteTitle: title);
},

// In NoteDetailScreen
class NoteDetailScreen extends StatelessWidget {
  final String noteTitle;

  const NoteDetailScreen({required this.noteTitle});

  @override
  Widget build(BuildContext context) {
    // READ: fetch the full note from provider using the title
    final note = context.watch<NotesProvider>().findNoteByTitle(noteTitle);
    
    if (note == null) {
      return Scaffold(body: Center(child: Text('Note not found')));
    }

    return Scaffold(
      appBar: AppBar(title: Text(note.title)),
      body: Center(child: Text(note.content)),
    );
  }
}
```

Key insight: The route passes minimal data (just the title). The detail screen fetches the full note from the provider. This decouples navigation from data fetching.

### CREATE: Navigating to and Returning from Create Screen

When creating a note, you navigate to a create screen, and after the note is created, you return to the list:

```dart
// In NoteListScreen
FloatingActionButton(
  onPressed: () {
    Navigator.pushNamed(context, '/create-note');
    // No need to await - the provider already updated the list
  },
  child: Icon(Icons.add),
)

// In route table
'/create-note': (context) => CreateNoteScreen(),

// In CreateNoteScreen
class CreateNoteScreen extends StatefulWidget {
  @override
  State<CreateNoteScreen> createState() => _CreateNoteScreenState();
}

class _CreateNoteScreenState extends State<CreateNoteScreen> {
  late TextEditingController _titleController;
  late TextEditingController _contentController;

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController();
    _contentController = TextEditingController();
  }

  @override
  void dispose() {
    _titleController.dispose();
    _contentController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Create Note'),
        actions: [
          IconButton(
            icon: Icon(Icons.check),
            onPressed: _saveNote,
          ),
        ],
      ),
      body: Padding(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(controller: _titleController),
            SizedBox(height: 16),
            TextField(controller: _contentController),
          ],
        ),
      ),
    );
  }

  void _saveNote() {
    // CREATE: add note via provider
    final note = Note(
      title: _titleController.text,
      content: _contentController.text,
      folder: 'General',
      tags: [],
    );

    context.read<NotesProvider>().createNote(note);

    // Return to list - the provider already notified listeners
    Navigator.pop(context);
    
    // Show success
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Note created')),
    );
  }
}
```

Key insight: After CREATE, you simply pop the screen. The provider notified listeners, so the list screen automatically shows the new note. No need to return data through the Navigator.

### UPDATE: Navigating to Edit and Reflecting Changes

When editing a note, navigate to a detail screen in edit mode, make changes, and return. The list automatically reflects changes because the provider notified listeners:

```dart
// In NoteListScreen, navigate to detail for editing
ListTile(
  title: Text(note.title),
  onTap: () {
    Navigator.pushNamed(
      context,
      '/note-detail',
      arguments: note.title,
    );
  },
)

// In NoteDetailScreen, implement edit mode
class NoteDetailScreen extends StatefulWidget {
  final String noteTitle;

  const NoteDetailScreen({required this.noteTitle});

  @override
  State<NoteDetailScreen> createState() => _NoteDetailScreenState();
}

class _NoteDetailScreenState extends State<NoteDetailScreen> {
  late TextEditingController _contentController;
  bool _isEditing = false;

  @override
  void initState() {
    super.initState();
    final note = context.read<NotesProvider>().findNoteByTitle(widget.noteTitle);
    _contentController = TextEditingController(text: note?.content ?? '');
  }

  @override
  void dispose() {
    _contentController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final note = context.watch<NotesProvider>().findNoteByTitle(widget.noteTitle);

    if (note == null) {
      return Scaffold(body: Center(child: Text('Note not found')));
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(note.title),
        actions: [
          if (_isEditing)
            IconButton(
              icon: Icon(Icons.check),
              onPressed: _saveChanges,
            )
          else
            IconButton(
              icon: Icon(Icons.edit),
              onPressed: () => setState(() => _isEditing = true),
            ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: _isEditing
            ? TextField(controller: _contentController)
            : Text(note.content),
      ),
    );
  }

  void _saveChanges() {
    final note = context.read<NotesProvider>().findNoteByTitle(widget.noteTitle)!;
    
    // UPDATE: modify via provider
    context.read<NotesProvider>().updateNote(
      widget.noteTitle,
      Note(
        title: note.title,
        content: _contentController.text,
        folder: note.folder,
        tags: note.tags,
      ),
    );

    setState(() => _isEditing = false);
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Note updated')),
    );
  }
}
```

Key insight: When you UPDATE via the provider, listeners (the list screen) automatically see the changes. You don't need to pass data back through the Navigator.

### DELETE: Safe Deletion and Navigation

When deleting, you might want to return to the list screen:

```dart
class NoteDetailScreen extends StatefulWidget {
  final String noteTitle;

  const NoteDetailScreen({required this.noteTitle});

  @override
  State<NoteDetailScreen> createState() => _NoteDetailScreenState();
}

class _NoteDetailScreenState extends State<NoteDetailScreen> {
  @override
  Widget build(BuildContext context) {
    final note = context.watch<NotesProvider>().findNoteByTitle(widget.noteTitle);

    if (note == null) {
      // Note was deleted - navigate back
      Navigator.pop(context);
      return Container();
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(note.title),
        actions: [
          IconButton(
            icon: Icon(Icons.delete),
            onPressed: () => _confirmDelete(context),
          ),
        ],
      ),
      body: Text(note.content),
    );
  }

  void _confirmDelete(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('Delete note?'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              // DELETE: remove via provider
              context.read<NotesProvider>().deleteNote(widget.noteTitle);

              // Close dialog
              Navigator.pop(context);

              // Return to list
              Navigator.pop(context);

              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Note deleted')),
              );
            },
            child: Text('Delete', style: TextStyle(color: Colors.red)),
          ),
        ],
      ),
    );
  }
}
```

Key insight: The detail screen watches the provider for the note. If the note is deleted (perhaps on another screen), the watcher detects it's gone and automatically pops the detail screen.

## Multi-Screen Navigation Patterns

As your app grows, managing navigation across many screens requires structure.

### Tab Navigation

Some apps have multiple screens that are peers (home, search, profile). Use `BottomNavigationBar` or `NavigationRail`:

```dart
class MainApp extends StatefulWidget {
  @override
  State<MainApp> createState() => _MainAppState();
}

class _MainAppState extends State<MainApp> {
  int _selectedIndex = 0;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: IndexedStack(
        index: _selectedIndex,
        children: [
          NoteListScreen(),
          SearchScreen(),
          SettingsScreen(),
        ],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        items: [
          BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
          BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
          BottomNavigationBarItem(icon: Icon(Icons.settings), label: 'Settings'),
        ],
        onTap: (index) {
          setState(() => _selectedIndex = index);
        },
      ),
    );
  }
}
```

`IndexedStack` keeps all screens alive (preserves state), switching between them by index.

### Hierarchical Navigation

Some apps have a clear hierarchy: main screens with detail screens beneath them. Use named routes with a clear structure:

```dart
routes: {
  '/': (context) => MainApp(),
  '/notes-list': (context) => NoteListScreen(),
  '/note-detail': (context) {
    final title = ModalRoute.of(context)!.settings.arguments as String;
    return NoteDetailScreen(noteTitle: title);
  },
  '/settings': (context) => SettingsScreen(),
  '/about': (context) => AboutScreen(),
}
```

Routes follow a logical structure, making the app's organization clear.

## Best Practices for Navigation

1. **Centralize routes:** Define all routes in one place (MaterialApp or a separate file). Don't scatter navigation throughout your code.

2. **Use meaningful route names:** `/note-detail` is clearer than `/detail`. Route names are part of your app's API.

3. **Minimize route arguments:** Pass IDs or keys, not entire objects. Screens fetch full data from state management.

4. **Respect the back stack:** Users expect the back button to work intuitively. Use `push` for forward navigation, `pop` for back.

5. **Show loading states:** When navigating, especially with async operations, show progress.

6. **Handle missing data gracefully:** If a screen expects data that's missing, show an error or navigate back.

7. **Use `pushReplacement` sparingly:** Only when the previous screen shouldn't exist anymore (like after login).

---

## Hands-On Project

Ready to apply routing with CRUD operations? Work through [Markdown Notes Project Part D](markdown-notes-project-part-d.html) to refactor the notes app to use named routes and GoRouter, demonstrating how routing and state management work together for clean multi-screen CRUD workflows.
