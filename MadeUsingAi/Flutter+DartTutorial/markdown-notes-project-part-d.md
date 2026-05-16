# Markdown Notes Project Part D — Named Routes and Navigation Architecture

## Overview

In Parts A, B, and C, you built the note-taking app's core functionality: CLI logic, Flutter UI, and CRUD operations with state management. Now you'll refactor the navigation to use named routes and proper navigation architecture.

This project shows how routing and state management work together. Routes handle transitions between screens; the provider handles data. This separation of concerns makes your app maintainable as it grows.

This is a guided refactor. You'll restructure existing screens to work with a centralized route table, demonstrating clean navigation architecture.

## Architecture

You'll refactor your app to use named routes. The structure remains the same, but navigation becomes centralized:

```
lib/
├── main.dart                          // Updated: centralized route table
├── models/
│   └── note.dart
├── providers/
│   └── notes_provider.dart
├── screens/
│   ├── note_list_screen.dart          // Updated: use pushNamed
│   ├── note_detail_screen.dart        // Updated: receive noteTitle as argument
│   ├── create_note_screen.dart        // Updated: use named route
│   └── home_screen.dart               // NEW: main entry point
└── widgets/
    └── note_card.dart
```

## Step 1: Understand the Route Table

Before refactoring, understand how routes work.

**Your Task:** Review the route table structure in your mind.

A route table maps route names to screen builders:

```dart
{
  '/': (context) => HomeScreen(),
  '/notes-list': (context) => NoteListScreen(),
  '/note-detail': (context) {
    final title = ModalRoute.of(context)!.settings.arguments as String;
    return NoteDetailScreen(noteTitle: title);
  },
  '/create-note': (context) => CreateNoteScreen(),
}
```

**Questions to think about:**
- Why is the route name a string like '/notes-list' instead of just a class reference?
- In the '/note-detail' route, why do we only pass the title as an argument instead of the entire note?
- What does `ModalRoute.of(context)` do?

## Step 2: Create the Route Table

**Your Task:** In `main.dart`, create a centralized route table.

Create a new method or function that returns the route table:

```dart
Map<String, WidgetBuilder> getRoutes() {
  return {
    '/': (context) => HomeScreen(),
    '/notes-list': (context) => NoteListScreen(),
    '/note-detail': (context) {
      // TODO: Extract the note title from arguments
      // TODO: Return NoteDetailScreen with the title
    },
    '/create-note': (context) => CreateNoteScreen(),
  };
}
```

**Questions:**
- In the '/note-detail' route, what type should the arguments be?
- How do you safely extract arguments and handle the case where they're missing?

Then update `MaterialApp` to use the route table:

```dart
MaterialApp(
  routes: getRoutes(),
  // TODO: Set home to HomeScreen
)
```

## Step 3: Create HomeScreen

**Your Task:** Create `lib/screens/home_screen.dart`

This is your app's entry point—a simple screen that navigates to the main notes list.

```dart
class HomeScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // TODO: Navigate to /notes-list
          },
          child: Text('Go to Notes'),
        ),
      ),
    );
  }
}
```

**Alternative:** HomeScreen could directly be NoteListScreen. The extra screen is optional—use it if you want an entry point for future features like login or splash screens.

## Step 4: Refactor NoteListScreen to Use Named Routes

**Your Task:** Update `NoteListScreen` to use `Navigator.pushNamed()`.

Current code (probably):
```dart
onTap: () {
  Navigator.push(
    context,
    MaterialPageRoute(builder: (_) => NoteDetailScreen(note: note)),
  );
}
```

**Refactor to named routes:**
```dart
onTap: () {
  // TODO: Use Navigator.pushNamed to navigate to '/note-detail'
  // TODO: Pass note.title as arguments
}
```

Similarly, for the "Create Note" button:
```dart
FloatingActionButton(
  onPressed: () {
    // TODO: Use Navigator.pushNamed to navigate to '/create-note'
  },
  child: Icon(Icons.add),
)
```

**Questions:**
- What method do you call to navigate with a named route?
- How do you pass data (the note title) to the route?

## Step 5: Refactor NoteDetailScreen

**Your Task:** Update `NoteDetailScreen` to receive data via route arguments instead of constructor parameters.

Current code (probably):
```dart
class NoteDetailScreen extends StatefulWidget {
  final Note note;
  
  const NoteDetailScreen({required this.note});
  
  @override
  State<NoteDetailScreen> createState() => _NoteDetailScreenState();
}
```

**Refactor to:**
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
    // TODO: Watch the provider and find the note by title
    // final note = context.watch<NotesProvider>().findNoteByTitle(widget.noteTitle);
    
    // TODO: Display the note content
    // If note is null (was deleted), show error or navigate back
  }
}
```

**Why this change?** Routes pass minimal data (IDs, keys). Screens fetch full data from the provider. This decouples navigation from data.

In `initState()`, initialize controllers with data from the provider:

```dart
@override
void initState() {
  super.initState();
  final note = context.read<NotesProvider>().findNoteByTitle(widget.noteTitle);
  // TODO: Initialize _contentController with note?.content
}
```

## Step 6: Refactor CreateNoteScreen

**Your Task:** Update `CreateNoteScreen` to navigate using the route.

After saving, instead of `Navigator.pop()`, consider if you want to return to the list or stay on the create screen:

```dart
void _saveNote() {
  // TODO: Validate title is not empty
  
  // TODO: Create Note and call provider's createNote()
  
  // TODO: Show success message
  
  // TODO: Navigate back to notes list with pushReplacementNamed
  // This prevents users from returning to the create screen
}
```

**Question:** Should you use `pop()` or `pushReplacementNamed('/notes-list')`? What's the difference in user experience?

## Step 7: Test the Navigation

Test each navigation path:

**Navigation Flow:**
- [ ] HomeScreen opens when app launches
- [ ] Tap "Go to Notes" navigates to NoteListScreen
- [ ] Tap a note navigates to NoteDetailScreen with the correct note
- [ ] Edit and save updates the note and the list
- [ ] Tap create button navigates to CreateNoteScreen
- [ ] Create a note and save navigates back to the list with the new note visible
- [ ] Delete a note removes it and the list updates
- [ ] Delete from detail screen navigates back to the list
- [ ] Back button works as expected at each screen

**Edge Cases:**
- [ ] Navigate to detail screen, delete the note elsewhere, return to detail—it should detect the note is gone and handle gracefully
- [ ] Navigate deep (list → detail → create), then pop back—you should be in the right place

## Understanding the Refactor

What changed and why?

**Before:** Screens constructed each other directly.
```dart
Navigator.push(
  context,
  MaterialPageRoute(builder: (_) => NoteDetailScreen(note: note)),
);
```

**After:** Screens are looked up by name.
```dart
Navigator.pushNamed(context, '/note-detail', arguments: note.title);
```

**Benefits:**
1. Routes are centralized (easier to see app structure)
2. Minimal data passed through routes (just the title, not the whole note)
3. Screens fetch full data from the provider
4. Easy to add deep linking later
5. Easier to add route guards (check permissions before navigating)

**Key Insight:** Routing and state management are separate concerns. Routes move users between screens. The provider manages the data. Neither depends on the other—they work together cleanly.

## Design Decisions

As you refactor, you made choices:

**Minimal Route Arguments:** Why pass only the note title instead of the entire note object?

**Data Fetching:** Should screens fetch data in `build()` or `initState()`? When should they handle missing data?

**Navigation After CRUD:** After CREATE, should you pop or push the list screen? After DELETE, should you pop automatically or let the user click back?

**Route Hierarchy:** Should you have intermediate screens (like HomeScreen) or go directly to NoteListScreen?

Each choice affects user experience and code maintainability.

## Extending Navigation

Once you have named routes working, consider:

1. **Deep Linking:** Handle URLs like `app://notes/MyNote` by parsing the path and navigating to `/note-detail` with the note title.

2. **Route Guards:** Add permission checks before navigating to certain screens.

3. **GoRouter:** For larger apps, switch to GoRouter package for more powerful routing.

4. **Tab Navigation:** If you add a search or settings screen, use `BottomNavigationBar` to switch between tabs.

5. **Animation:** Customize route transitions with `PageRouteBuilder` for custom animations.

## Next Steps

This refactor prepares you for the Best Practices chapter, which will cover:
- Testing navigation flows
- Handling complex navigation scenarios
- Performance optimization
- Architecture patterns for large apps

For now, focus on understanding how named routes centralize navigation logic and how routing and state management work together.
