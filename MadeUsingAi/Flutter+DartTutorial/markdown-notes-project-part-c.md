# Markdown Notes Project Part C — CRUD Operations with State Management

## Overview

In Part A, you built CLI logic for managing notes. In Part B, you created a Flutter UI for viewing and editing notes. Now you'll implement the complete **CRUD cycle** (Create, Read, Update, Delete) using Provider for proper state management.

This is a guided project where you'll implement pieces yourself. Code snippets show structure and approach; you'll write the actual implementation.

## Understanding CRUD in This Project

Before you start, understand what each CRUD operation means in the context of this notes app:

**Create (C):** Add a new note to the collection. User fills out a form with title and content, clicks Save, and a new note appears in the list.

**Read (R):** Retrieve and display notes. The list displays all notes (READ many); the detail screen displays one note (READ one).

**Update (U):** Modify an existing note. User edits the title or content and saves changes.

**Delete (D):** Remove a note from the collection. User swipes or clicks a delete button and the note is removed.

The Provider you'll build holds the data and provides methods for each CRUD operation. When any CRUD operation completes, the provider notifies listeners, and the UI automatically reflects the changes.

## Architecture

You'll add a new file to your project structure:

```
lib/
├── main.dart
├── models/
│   └── note.dart
├── providers/
│   └── notes_provider.dart        // NEW: State management with CRUD
├── screens/
│   ├── note_list_screen.dart
│   ├── note_detail_screen.dart
│   └── create_note_screen.dart    // NEW: Create operation
└── widgets/
    └── note_card.dart
```

## Step 1: Set Up Provider

**Your Task:** Add Provider to your project.

Open `pubspec.yaml` and add:
```yaml
dependencies:
  provider: ^6.0.0
```

Then run `flutter pub get`.

## Step 2: Build the Notes Provider

This is the core of state management. The provider implements all four CRUD operations.

**Concept Review:** The provider is a `ChangeNotifier` that:
- Holds the list of notes (the data)
- Implements CREATE, READ, UPDATE, DELETE methods
- Calls `notifyListeners()` after any CRUD operation completes
- Provides getters so widgets can READ the data

**Your Task:** Create `lib/providers/notes_provider.dart`

Start with the structure:

```dart
import 'package:flutter/material.dart';
import '../models/note.dart';

class NotesProvider extends ChangeNotifier {
  List<Note> _notes = [];

  // READ: Getter to access all notes
  List<Note> get notes => _notes;

  // Initialize with sample data
  void initialize() {
    // TODO: Create 2-3 sample notes here
    // Each should have title, content, folder, and tags
  }

  // CREATE: Add a new note
  void createNote(Note note) {
    // TODO: Add note to _notes list
    // TODO: Call notifyListeners() to trigger rebuilds
  }

  // UPDATE: Modify an existing note
  void updateNote(String originalTitle, Note updatedNote) {
    // TODO: Find the note by originalTitle
    // TODO: Replace it with updatedNote
    // TODO: Call notifyListeners()
  }

  // DELETE: Remove a note
  void deleteNote(String title) {
    // TODO: Remove the note with this title
    // TODO: Call notifyListeners()
  }

  // Helper: Find a note by title (useful for READ)
  Note? findNoteByTitle(String title) {
    // TODO: Search _notes and return the note, or null if not found
  }
}

// Create the provider instance
final notesProvider = ChangeNotifierProvider((ref) {
  final provider = NotesProvider();
  provider.initialize();
  return provider;
});
```

**Implementation Guidance:**

For `createNote()`: How do you add an item to a list? What does it mean to "notify listeners"?

For `updateNote()`: You need to find the original note by title, then replace it. How do you update a specific item in a list?

For `deleteNote()`: Use the Dart list method that removes items matching a condition. What's it called?

For `findNoteByTitle()`: Use the list method that returns the first item matching a condition.

Think through each operation before implementing.

## Step 3: Update Main App

Your app needs to provide the `NotesProvider` to all widgets.

**Your Task:** Modify `main.dart` to wrap your app with MultiProvider.

Current code probably looks like:

```dart
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      // ...
      home: NoteListScreen(),
    );
  }
}
```

**Modify it to:**

```dart
import 'package:provider/provider.dart';
import 'providers/notes_provider.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp();

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        // TODO: Add the notesProvider here
      ],
      child: MaterialApp(
        // ... rest of your MaterialApp
      ),
    );
  }
}
```

**Question:** How do you add `notesProvider` to the providers list?

## Step 4: Refactor NoteListScreen to Use Provider (READ)

Your existing `NoteListScreen` probably loads notes some other way. Now it should read them from the provider.

**Your Task:** Update `NoteListScreen` to use `Consumer` to read all notes.

Structure:

```dart
class NoteListScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Notes')),
      body: Consumer<NotesProvider>(
        builder: (context, notesProvider, child) {
          // TODO: Display notesProvider.notes in a ListView
          // Similar to Part B, but reading from the provider
          // If notesProvider.notes is empty, show "No notes"
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          // TODO: Navigate to CreateNoteScreen
        },
        child: Icon(Icons.add),
      ),
    );
  }
}
```

**Questions:**
- How does `Consumer<NotesProvider>` work?
- When does the builder function run?
- How do you access `notesProvider` in the builder?

When deleting a note, call the provider's DELETE method:

```dart
context.read<NotesProvider>().deleteNote(noteTitle);
```

## Step 5: Add Swipe-to-Delete (DELETE)

Enhance your `NoteCard` widget to support swiping to delete.

**Your Task:** Wrap the card in a `Dismissible` widget:

```dart
class NoteCard extends StatelessWidget {
  final Note note;
  final VoidCallback onTap;
  final VoidCallback onDelete;

  const NoteCard({
    required this.note,
    required this.onTap,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Dismissible(
      key: Key(note.title),
      onDismissed: (_) {
        onDelete();
      },
      background: Container(
        color: Colors.red,
        alignment: Alignment.centerRight,
        padding: EdgeInsets.only(right: 16),
        child: Icon(Icons.delete, color: Colors.white),
      ),
      child: Card(
        // TODO: Add your existing card content here
      ),
    );
  }
}
```

When the user swipes, `onDelete` is called. In `NoteListScreen`, pass:

```dart
NoteCard(
  note: note,
  onTap: () => _openNote(note),
  onDelete: () {
    context.read<NotesProvider>().deleteNote(note.title);
  },
)
```

## Step 6: Create the Create Note Screen (CREATE)

This is a new screen where users enter a title and content for a new note.

**Your Task:** Create `lib/screens/create_note_screen.dart`

Structure:

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/note.dart';
import '../providers/notes_provider.dart';

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
    // TODO: Dispose of controllers to prevent memory leaks
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Create Note'),
        actions: [
          IconButton(
            icon: Icon(Icons.check),
            onPressed: _createNote,
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          children: [
            // TODO: Title input field (large, bold style)
            SizedBox(height: 16),
            // TODO: Content input field (larger, multiline)
          ],
        ),
      ),
    );
  }

  void _createNote() {
    // TODO: Validate that title is not empty
    // TODO: Create a Note object from the input
    // TODO: Call context.read<NotesProvider>().createNote(note)
    // TODO: Show success message with SnackBar
    // TODO: Pop the screen with Navigator.pop(context)
  }
}
```

**Implementation Guidance:**

For the title field: Should have style TextStyle(fontSize: 20, fontWeight: FontWeight.bold).

For the content field: Should be multiline (maxLines: null, minLines: 10 or similar).

In `_createNote()`: Validate first. If title is empty, show a SnackBar error. If valid, create a Note with title, content, and default folder ("General"). Then call the CREATE method on the provider.

## Step 7: Update NoteDetailScreen (READ and UPDATE)

Your existing edit functionality should now update via the provider.

**Current code (probably):**
```dart
void _saveNote() {
  widget.note.title = _titleController.text;
  widget.note.content = _contentController.text;
  setState(() => _isEditing = false);
}
```

**Refactor to use provider (UPDATE):**

```dart
void _saveNote() {
  final updatedNote = Note(
    title: _titleController.text,
    content: _contentController.text,
    folder: widget.note.folder,
    tags: widget.note.tags,
  );
  
  // TODO: Call provider's updateNote method
  // Pass original title and updated note
  
  setState(() => _isEditing = false);
}
```

When deleting (DELETE):

```dart
void _deleteNote() {
  context.read<NotesProvider>().deleteNote(widget.note.title);
  Navigator.pop(context);
}
```

## Step 8: Test the Complete CRUD Cycle

Create a checklist for testing all four operations:

**CREATE:**
- [ ] Floating action button navigates to create screen
- [ ] Can enter title and content
- [ ] Clicking check button creates the note
- [ ] New note appears in the list immediately

**READ:**
- [ ] All notes appear on startup
- [ ] Can tap a note to open detail screen
- [ ] Detail screen displays the note's title and content

**UPDATE:**
- [ ] Can edit note title and content
- [ ] Saving updates the note
- [ ] List reflects the updated title
- [ ] Updated note maintains its position or resorts correctly

**DELETE:**
- [ ] Swiping a note shows delete background
- [ ] Completing the swipe removes the note
- [ ] Note no longer appears in the list
- [ ] Delete from detail screen also removes from list

## Understanding What You Built

You've implemented a complete CRUD system:

- **CREATE:** Users fill out a form, click save, and a new note joins the collection.
- **READ:** The list reads and displays all notes; the detail screen reads one note.
- **UPDATE:** Users edit a note and changes are saved back to the provider.
- **DELETE:** Users swipe or click delete and the note is removed.

The provider centralizes all CRUD operations. When any operation completes, the provider notifies listeners, and the UI automatically reflects the changes. No prop-drilling, no callback hell—just clean, maintainable code.

## Design Questions

As you implement, think about these questions:

**Note Identification:** The code uses `title` as an identifier. Is this a good choice? What happens if two notes have the same title?

**Folder Handling:** When creating a note, folder is hardcoded as "General". Should users be able to choose a folder? Where would you add that UI?

**Tags:** Notes have tags but the UI doesn't expose them. Should they be editable?

**Validation:** What validation should happen before CREATE or UPDATE? Should the provider prevent duplicate titles?

**Undo/Redo:** What would it take to add an undo feature?

These questions don't have "right" answers—they depend on your app's requirements. Thinking through them is part of good design.

## Next Steps

Once CRUD works, consider extending it:

1. **Search** — Filter the list by title or content
2. **Sorting** — Sort by date created, alphabetically, etc.
3. **Persistence** — Save notes to disk (SharedPreferences or SQLite)
4. **Async operations** — Implement fetching notes from a server

Each of these can be built on top of the CRUD foundation you've created.

The next chapter (Routing & Navigation) will show how to use proper routing patterns to navigate between screens while managing CRUD state elegantly.
