# Markdown Notes Project Part B — Flutter UI

## Overview

This is Part B of your Markdown Note-Taking App. In Part A (Dart Basics), you built a command-line app with in-memory note storage. Now you'll convert that logic into a Flutter UI where users can view notes, edit their content, delete notes, and see a searchable note list.

**Scope:** Build a functional reading and editing interface. Adding new notes will come later in the State Management chapter.

## Learning Objectives

By completing this project, you will:

1. **Understand widget composition** — Assemble multiple widgets into a cohesive interface
2. **Manage layout** — Use Row, Column, ListView, and spacing widgets effectively
3. **Implement interactivity** — Handle user input with TextField, buttons, and GestureDetector
4. **Apply styling** — Use themes, colors, and Material Design patterns
5. **Handle state locally** — Use StatefulWidget to manage editing state
6. **Build a practical app** — Create a real, functional interface users can interact with

## Project Structure

Your Flutter app will have:

```
lib/
├── main.dart              // App entry point, MaterialApp setup
├── models/
│   └── note.dart          // Note data class (from Part A)
├── screens/
│   ├── note_list_screen.dart    // List of notes with search
│   └── note_detail_screen.dart  // Single note viewing/editing
└── widgets/
    └── note_card.dart     // Reusable note preview card
```

## Core Components

### Note Model

Reuse the `Note` class from Part A:

```dart
class Note {
  String title;
  String content;
  String folder;
  DateTime created;
  List<String> tags;
  
  Note({
    required this.title,
    required this.content,
    required this.folder,
    required this.tags,
  }) : created = DateTime.now();
}
```

### Main App Structure

```dart
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp();

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Markdown Notes',
      theme: ThemeData(
        useMaterial3: true,
        primarySwatch: Colors.blue,
      ),
      home: NoteListScreen(),
    );
  }
}
```

### NoteListScreen (Main Screen)

Display all notes in a searchable list. Users can:
- See all notes
- Search by title or content
- Tap a note to view/edit it
- Delete notes with a swipe or long-press

**Key widgets:**
- `Scaffold` — Top-level structure
- `AppBar` — Title and search icon
- `ListView.builder` — Scrollable list of notes
- `SearchBar` or `TextField` — Search functionality
- `Dismissible` — Swipe-to-delete

**Implementation hints:**

```dart
class NoteListScreen extends StatefulWidget {
  @override
  State<NoteListScreen> createState() => _NoteListScreenState();
}

class _NoteListScreenState extends State<NoteListScreen> {
  List<Note> allNotes = []; // Load from Part A logic
  List<Note> filteredNotes = [];
  String searchQuery = '';

  void _filterNotes(String query) {
    setState(() {
      searchQuery = query;
      filteredNotes = allNotes
        .where((note) => 
          note.title.toLowerCase().contains(query.toLowerCase()) ||
          note.content.toLowerCase().contains(query.toLowerCase())
        )
        .toList();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('My Notes'),
        elevation: 0,
      ),
      body: Column(
        children: [
          // Search field
          Padding(
            padding: EdgeInsets.all(16),
            child: TextField(
              decoration: InputDecoration(
                hintText: 'Search notes...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(8),
                ),
              ),
              onChanged: _filterNotes,
            ),
          ),
          // Note list
          Expanded(
            child: filteredNotes.isEmpty
              ? Center(child: Text('No notes found'))
              : ListView.builder(
                  itemCount: filteredNotes.length,
                  itemBuilder: (context, index) {
                    final note = filteredNotes[index];
                    return NoteCard(
                      note: note,
                      onTap: () => _openNote(note),
                      onDelete: () => _deleteNote(note),
                    );
                  },
                ),
          ),
        ],
      ),
    );
  }

  void _openNote(Note note) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => NoteDetailScreen(note: note),
      ),
    );
  }

  void _deleteNote(Note note) {
    setState(() {
      allNotes.remove(note);
      filteredNotes.remove(note);
    });
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Note deleted')),
    );
  }
}
```

### NoteCard Widget

A reusable card showing note preview:

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
      onDismissed: (_) => onDelete(),
      background: Container(
        color: Colors.red,
        alignment: Alignment.centerRight,
        padding: EdgeInsets.only(right: 16),
        child: Icon(Icons.delete, color: Colors.white),
      ),
      child: Card(
        margin: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
        child: ListTile(
          title: Text(note.title, style: TextStyle(fontWeight: FontWeight.bold)),
          subtitle: Text(
            note.content.length > 100
              ? note.content.substring(0, 100) + '...'
              : note.content,
            maxLines: 2,
            overflow: TextOverflow.ellipsis,
          ),
          trailing: Icon(Icons.chevron_right),
          onTap: onTap,
        ),
      ),
    );
  }
}
```

### NoteDetailScreen (Viewing/Editing)

Display a single note with editing capabilities. Users can:
- Read the full note content
- Edit the title and content
- Delete the note
- See metadata (created date, tags, folder)

**Key widgets:**
- `StatefulWidget` to manage editing state
- `TextField` for title and content editing
- `IconButton` for save/delete actions
- `AppBar` with action buttons
- `FloatingActionButton` or `ElevatedButton` for save

**Implementation hints:**

```dart
class NoteDetailScreen extends StatefulWidget {
  final Note note;

  const NoteDetailScreen({required this.note});

  @override
  State<NoteDetailScreen> createState() => _NoteDetailScreenState();
}

class _NoteDetailScreenState extends State<NoteDetailScreen> {
  late TextEditingController _titleController;
  late TextEditingController _contentController;
  bool _isEditing = false;

  @override
  void initState() {
    super.initState();
    _titleController = TextEditingController(text: widget.note.title);
    _contentController = TextEditingController(text: widget.note.content);
  }

  @override
  void dispose() {
    _titleController.dispose();
    _contentController.dispose();
    super.dispose();
  }

  void _saveNote() {
    widget.note.title = _titleController.text;
    widget.note.content = _contentController.text;
    setState(() => _isEditing = false);
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Note saved')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_isEditing ? 'Edit Note' : 'View Note'),
        actions: [
          if (_isEditing)
            IconButton(
              icon: Icon(Icons.check),
              onPressed: _saveNote,
            )
          else
            IconButton(
              icon: Icon(Icons.edit),
              onPressed: () => setState(() => _isEditing = true),
            ),
          IconButton(
            icon: Icon(Icons.delete),
            onPressed: () {
              Navigator.pop(context);
              // Note deletion is handled in parent screen
            },
          ),
        ],
      ),
      body: SingleChildScrollView(
        padding: EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            // Title field
            _isEditing
              ? TextField(
                  controller: _titleController,
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                  decoration: InputDecoration(
                    hintText: 'Note title',
                    border: OutlineInputBorder(),
                  ),
                )
              : Text(
                  widget.note.title,
                  style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                ),
            SizedBox(height: 16),
            
            // Metadata
            if (!_isEditing) ...[
              Wrap(
                spacing: 8,
                children: [
                  Chip(label: Text('Folder: ${widget.note.folder}')),
                  if (widget.note.tags.isNotEmpty)
                    ...widget.note.tags.map((tag) => Chip(label: Text(tag))),
                ],
              ),
              SizedBox(height: 16),
            ],
            
            // Content field
            _isEditing
              ? TextField(
                  controller: _contentController,
                  maxLines: null,
                  decoration: InputDecoration(
                    hintText: 'Note content',
                    border: OutlineInputBorder(),
                  ),
                )
              : Text(widget.note.content),
          ],
        ),
      ),
    );
  }
}
```

## Implementation Steps

### Step 1: Create Note Model (10 mins)
- Copy the `Note` class from Part A
- Ensure it has all necessary fields and methods

### Step 2: Set Up Main App (5 mins)
- Create `main.dart` with `MaterialApp`
- Set up basic theme
- Create `NoteListScreen` placeholder

### Step 3: Build NoteListScreen (20 mins)
- Create `Scaffold` with `AppBar`
- Add search `TextField`
- Implement `ListView.builder` with sample notes
- Handle filtering and display

### Step 4: Create NoteCard Widget (10 mins)
- Build reusable card for note preview
- Add swipe-to-delete with `Dismissible`
- Style with `Card` and `ListTile`

### Step 5: Build NoteDetailScreen (20 mins)
- Create view mode (read-only display)
- Create edit mode (editable TextFields)
- Toggle between modes
- Add save and delete functionality

### Step 6: Connect Navigation (5 mins)
- Wire up `NoteCard` onTap to navigate to detail screen
- Handle back navigation
- Refresh list after edits/deletions

### Step 7: Test and Polish (10 mins)
- Create sample notes for testing
- Test search, edit, delete workflows
- Verify UI responsiveness

**Total: ~60 minutes of hands-on coding**

## Testing Checklist

- [ ] App launches without errors
- [ ] Search filters notes by title and content
- [ ] Tapping a note opens detail screen
- [ ] Editing mode activates when edit button is pressed
- [ ] Saving updates note title and content
- [ ] Swiping note dismisses it and shows delete confirmation
- [ ] Back navigation returns to list
- [ ] List refreshes after edit or delete
- [ ] All buttons are clearly visible and functional
- [ ] Layout is readable on different screen sizes

## Stretch Goals

- [ ] Add basic markdown rendering (bold, italic, code blocks)
- [ ] Implement note preview with formatted text
- [ ] Add floating action button to jump to top of list
- [ ] Persist notes to device storage (SharedPreferences)
- [ ] Add folder filtering to the list screen

## Key Learning Points

You'll learn how to:

1. **Compose complex UIs** from simple widgets
2. **Manage local state** with `StatefulWidget` and `setState`
3. **Use common Material Design patterns** (AppBar, FAB, Snackbar)
4. **Handle user input** effectively
5. **Navigate between screens** with `Navigator`
6. **Style and theme** your app
7. **Implement common workflows** (CRUD operations at read/update/delete level)

## How This Evolves

In future chapters, you'll expand this app:

- **State Management Chapter:** Replace local `setState` with Provider or Riverpod for better scalability
- **Routing Chapter:** Add proper named routes and deep linking
- **Adding notes:** Implement the "Create" part of CRUD
- **Persistence:** Add SQLite storage instead of in-memory
- **Best Practices Chapter:** Refactor for testability and maintainability

For now, focus on building a solid UI that demonstrates widget composition and interactivity.
