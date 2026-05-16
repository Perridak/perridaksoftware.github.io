# State Management

State is data that changes during your app's runtime and affects what the UI displays. Managing state well separates prototypes from production software. This chapter builds your understanding step by step, from the simplest approach to the patterns used in professional Flutter apps.

We'll start with how `setState()` works, understand why it breaks down as apps grow, then explore two major solutions—Provider and Riverpod. We'll pay special attention to async operations, because managing side effects (API calls, file I/O, timers) is where most complexity lives. Throughout, we'll use CRUD operations (Create, Read, Update, Delete) as our lens for understanding how state management enables real app functionality.

## Understanding State: Two Categories

Before learning how to manage state, you need to distinguish two types of state, because they require different solutions.

### Local State

Local state belongs to a single widget and doesn't need to be shared. Examples: whether a checkbox is ticked, text in an input field, whether an accordion is expanded.

Local state lives in a `StatefulWidget`'s `State` class. It's appropriate for local state because no other widget needs to react to changes:

```dart
class ToggleButton extends StatefulWidget {
  @override
  State<ToggleButton> createState() => _ToggleButtonState();
}

class _ToggleButtonState extends State<ToggleButton> {
  bool _isOn = false;  // Local state

  @override
  Widget build(BuildContext context) {
    return Switch(
      value: _isOn,
      onChanged: (newValue) {
        setState(() {
          _isOn = newValue;  // Update and rebuild
        });
      },
    );
  }
}
```

When `_isOn` changes, `setState()` triggers a rebuild of this widget only. The parent doesn't know or care about `_isOn`—it's truly local.

### App-Wide State

App-wide state is needed by multiple widgets across your app. Examples: the current user's login info, a list of all notes, the app's theme setting. This is the state that powers CRUD operations—the data that your app creates, reads, updates, and deletes.

If you try to manage app-wide state with local `setState()` in individual widgets, you create problems:

```dart
// DON'T DO THIS - antipattern demonstrating the problem

class NoteListScreen extends StatefulWidget {
  @override
  State<NoteListScreen> createState() => _NoteListScreenState();
}

class _NoteListScreenState extends State<NoteListScreen> {
  List<Note> notes = [];  // App-wide data in one screen
  
  @override
  Widget build(BuildContext context) {
    return ListView(
      children: notes.map((note) => Text(note.title)).toList(),
    );
  }
}

class NoteDetailScreen extends StatefulWidget {
  // This screen also needs the notes list to update it (READ operation)
  // The detail screen might also update a note (UPDATE operation)
  // But how do we get the list? We'd have to pass it through the constructor
  // If there are 5 screens between them, every one has to accept and pass it through.
  // This is called "prop drilling" and it becomes unmaintainable.
}
```

The core problem: when data belongs to multiple widgets, using local `setState()` forces you to pass that state through every widget in between, cluttering constructors and making code fragile. This is especially painful for CRUD operations, where multiple screens need to read the data and trigger updates.

## CRUD: The Framework for Understanding App State

CRUD stands for Create, Read, Update, Delete—the four fundamental operations on any collection of data. Understanding CRUD helps clarify what state management needs to do:

- **Create:** Add new data to the collection. A "Create Note" form creates a new note.
- **Read:** Retrieve and display existing data. A note list reads all notes; a detail screen reads one note.
- **Update:** Modify existing data. Editing a note's content updates it.
- **Delete:** Remove data from the collection. Swiping to delete removes a note.

When you're managing app-wide state, you're building a system that handles CRUD operations cleanly across multiple screens. Poor state management makes CRUD painful (passing data through constructors everywhere). Good state management makes CRUD transparent (any widget can access and modify data).

## setState(): The Built-In Mechanism

`setState()` is Flutter's primitive state management tool. It works by marking a widget as "dirty" and scheduling a rebuild. Understanding how it works is essential to understanding why better solutions exist.

### How setState() Works Internally

When you call `setState(() { ... })`:

1. Flutter executes the code inside the lambda
2. Flutter marks the widget as needing rebuild
3. Flutter schedules a rebuild on the next frame
4. `build()` is called again with the new state values
5. The widget tree is compared to the old tree (diffing)
6. Only the parts that changed are updated on screen

Here's a concrete example with a CRUD context (creating a note):

```dart
class CreateNoteForm extends StatefulWidget {
  @override
  State<CreateNoteForm> createState() => _CreateNoteFormState();
}

class _CreateNoteFormState extends State<CreateNoteForm> {
  String title = '';
  String content = '';

  void _saveNote() {
    // CREATE operation: add new note
    // But who holds the list of notes? This widget doesn't.
    // Problem: we can't actually create a note here without prop-drilling
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TextField(onChanged: (value) => setState(() => title = value)),
        TextField(onChanged: (value) => setState(() => content = value)),
        ElevatedButton(onPressed: _saveNote, child: Text('Save')),
      ],
    );
  }
}
```

This illustrates the problem: local form state works fine, but where does the created note go? You'd have to pass a callback through constructors.

### Why setState() Breaks Down for CRUD

As your app grows with CRUD operations, `setState()` becomes problematic:

**Scenario:** You have a NoteListScreen displaying all notes (READ), a NoteDetailScreen displaying one note (READ), a CreateNoteScreen for adding notes (CREATE), and edit functionality for updating (UPDATE) and delete buttons (DELETE).

With `setState()`, managing these CRUD operations across screens requires prop drilling:

```dart
class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<Note> notes = [];  // Holds all the data

  void addNote(Note note) {  // CREATE
    setState(() => notes.add(note));
  }

  void updateNote(String title, Note updated) {  // UPDATE
    setState(() {
      final index = notes.indexWhere((n) => n.title == title);
      if (index != -1) notes[index] = updated;
    });
  }

  void deleteNote(String title) {  // DELETE
    setState(() => notes.removeWhere((n) => n.title == title));
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // READ: display notes
        NoteList(notes: notes, onCreateNote: addNote, onUpdateNote: updateNote, onDeleteNote: deleteNote),
      ],
    );
  }
}

class NoteList extends StatelessWidget {
  final List<Note> notes;
  final Function(Note) onCreateNote;
  final Function(String, Note) onUpdateNote;
  final Function(String) onDeleteNote;

  const NoteList({
    required this.notes,
    required this.onCreateNote,
    required this.onUpdateNote,
    required this.onDeleteNote,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: notes.length,
      itemBuilder: (context, index) {
        final note = notes[index];
        return NoteCard(
          note: note,
          onTap: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (_) => NoteDetailScreen(
                  note: note,
                  onUpdateNote: onUpdateNote,
                  onDeleteNote: onDeleteNote,
                ),
              ),
            );
          },
        );
      },
    );
  }
}

class NoteDetailScreen extends StatelessWidget {
  final Note note;
  final Function(String, Note) onUpdateNote;
  final Function(String) onDeleteNote;

  const NoteDetailScreen({
    required this.note,
    required this.onUpdateNote,
    required this.onDeleteNote,
  });

  @override
  Widget build(BuildContext context) {
    return NoteEditWidget(
      note: note,
      onUpdateNote: onUpdateNote,
      onDeleteNote: onDeleteNote,
    );
  }
}

class NoteEditWidget extends StatefulWidget {
  final Note note;
  final Function(String, Note) onUpdateNote;
  final Function(String) onDeleteNote;

  const NoteEditWidget({
    required this.note,
    required this.onUpdateNote,
    required this.onDeleteNote,
  });

  @override
  State<NoteEditWidget> createState() => _NoteEditWidgetState();
}

class _NoteEditWidgetState extends State<NoteEditWidget> {
  late TextEditingController contentController;

  @override
  void initState() {
    super.initState();
    contentController = TextEditingController(text: widget.note.content);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TextField(controller: contentController),
        ElevatedButton(
          onPressed: () {
            // UPDATE operation via callback
            widget.onUpdateNote(
              widget.note.title,
              Note(title: widget.note.title, content: contentController.text),
            );
          },
          child: Text('Save'),
        ),
        ElevatedButton(
          onPressed: () {
            // DELETE operation via callback
            widget.onDeleteNote(widget.note.title);
          },
          child: Text('Delete'),
        ),
      ],
    );
  }
}
```

Notice how CRUD callbacks are threaded through NoteList → NoteDetailScreen → NoteEditWidget. Every widget in the middle has to accept and pass them through, even though most don't use them. This is prop drilling.

As you add more screens and more CRUD operations, this becomes unmaintainable. The solution is to move CRUD operations to a centralized state manager that any widget can access without passing callbacks through constructors.

## Introducing Dependency Injection: A Better Approach

Before learning Provider and Riverpod, understand the underlying principle they're built on: **dependency injection**. Instead of each widget creating or managing its own dependencies, dependencies are provided from outside.

The traditional problem:
```dart
class MyScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    // Create the state manager ourselves - tightly coupled
    final notesManager = NotesManager();
    return NotesList(notesManager: notesManager);
  }
}
```

The injection approach:
```dart
class MyScreen extends StatelessWidget {
  final NotesManager notesManager;  // Injected - loosely coupled

  const MyScreen({required this.notesManager});

  @override
  Widget build(BuildContext context) {
    return NotesList(notesManager: notesManager);
  }
}
```

This is still prop drilling if you have deep widget trees. The next step is using an **inherited widget** to provide dependencies through the widget tree without passing them through every constructor.

Flutter has a built-in inherited widget pattern, but it's verbose. Provider and Riverpod are wrappers that make it simple.

## Provider: The Industry Standard Solution

Provider is the most-used state management solution in Flutter because it solves the real problems without adding unnecessary complexity. It makes CRUD operations clean and maintainable.

### Core Concept: The Provider

A **provider** is an object that:
1. Holds state (data)
2. Provides operations to modify that state (CRUD methods)
3. Notifies listeners when state changes
4. Is accessible to any widget in the tree without prop drilling

### How Provider Solves CRUD

With Provider, you define a state manager that holds your data and all CRUD operations:

```dart
class NotesManager extends ChangeNotifier {
  List<Note> _notes = [];

  List<Note> get notes => _notes;  // READ operation

  void addNote(Note note) {  // CREATE operation
    _notes.add(note);
    notifyListeners();  // Tell all listeners to rebuild
  }

  void updateNote(String title, Note updated) {  // UPDATE operation
    final index = _notes.indexWhere((n) => n.title == title);
    if (index != -1) {
      _notes[index] = updated;
      notifyListeners();
    }
  }

  void deleteNote(String title) {  // DELETE operation
    _notes.removeWhere((n) => n.title == title);
    notifyListeners();
  }
}
```

Now any widget can access these CRUD operations without prop drilling:

```dart
// In NoteEditWidget, no callbacks passed through constructors
class NoteEditWidget extends StatefulWidget {
  final Note note;

  const NoteEditWidget({required this.note});

  @override
  State<NoteEditWidget> createState() => _NoteEditWidgetState();
}

class _NoteEditWidgetState extends State<NoteEditWidget> {
  late TextEditingController contentController;

  @override
  void initState() {
    super.initState();
    contentController = TextEditingController(text: widget.note.content);
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        TextField(controller: contentController),
        ElevatedButton(
          onPressed: () {
            // UPDATE operation - access manager directly, no prop drilling
            context.read<NotesManager>().updateNote(
              widget.note.title,
              Note(title: widget.note.title, content: contentController.text),
            );
          },
          child: Text('Save'),
        ),
        ElevatedButton(
          onPressed: () {
            // DELETE operation - access manager directly
            context.read<NotesManager>().deleteNote(widget.note.title);
          },
          child: Text('Delete'),
        ),
      ],
    );
  }
}
```

The breakthrough: any widget can call `context.read<NotesManager>()` to access the CRUD operations, no matter how deeply nested. No prop drilling required.

### Understanding `ChangeNotifier`

`ChangeNotifier` is a class that holds mutable state and notifies listeners when it changes. When you call `notifyListeners()`, Flutter tells every widget listening to this notifier to rebuild.

This is the mechanism that makes CRUD transparent: when you CREATE, UPDATE, or DELETE, the notifier notifies all listeners, and the UI automatically reflects the new state.

### Two Ways to Access a Provider

**1. Consumer (for READ operations and display):**

Use `Consumer` when you need to display data from a provider and rebuild when it changes:

```dart
Consumer<NotesManager>(
  builder: (context, notesManager, child) {
    return ListView.builder(
      itemCount: notesManager.notes.length,  // READ operation
      itemBuilder: (context, index) {
        return ListTile(title: Text(notesManager.notes[index].title));
      },
    );
  },
)
```

`Consumer` rebuilds whenever the provider calls `notifyListeners()` (i.e., when CREATE, UPDATE, or DELETE operations happen).

**2. context.read() (for triggering CREATE, UPDATE, DELETE):**

Use `context.read()` when you want to call a CRUD method without causing a rebuild:

```dart
ElevatedButton(
  onPressed: () {
    // CREATE, UPDATE, or DELETE operation
    context.read<NotesManager>().deleteNote(noteTitle);
  },
  child: Text('Delete'),
)
```

When the button is pressed, `deleteNote()` is called. The button doesn't rebuild—but any `Consumer` watching the notes will rebuild to reflect the deletion.

### Understanding the Distinction

This distinction is crucial:

```dart
// Use Consumer when you want to DISPLAY state (READ)
Consumer<NotesManager>(
  builder: (context, notesManager, child) {
    return Text('Notes: ${notesManager.notes.length}');  // Display the count
  },
)

// Use context.read() when you want to CALL A CRUD METHOD
ElevatedButton(
  onPressed: () {
    context.read<NotesManager>().deleteNote(title);  // Call method, don't rebuild button
  },
  child: Text('Delete'),
)
```

If you use `context.read()` in a builder that displays data, the displayed data won't update when state changes. If you use `Consumer` for every method call, you cause unnecessary rebuilds.

### Setting Up Provider in Your App

Add to `pubspec.yaml`:
```yaml
dependencies:
  provider: ^6.0.0
```

In your main app:

```dart
void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp();

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => NotesManager()),
        // Add more providers here as needed
      ],
      child: MaterialApp(
        home: const NoteListScreen(),
      ),
    );
  }
}
```

`MultiProvider` makes all providers available throughout the app. Any widget can access them without prop drilling. Now CREATE, READ, UPDATE, and DELETE operations are clean and maintainable.

## Handling Async Operations

This is where state management becomes complex: managing operations that take time (API calls, file I/O, timers). In CRUD terms, READ operations often require async work (fetching data), and CREATE/UPDATE/DELETE might require persistence (async saving).

When you perform an async CRUD operation, you have three states to track:
1. **Loading** — Request in flight, show a spinner
2. **Success** — Operation completed, show the result
3. **Error** — Request failed, show error message

### The Problem: Multiple State Variables

Without careful design, you end up with fragile code:

```dart
class NotesManager extends ChangeNotifier {
  List<Note> _notes = [];
  bool _isLoading = false;  // For async READ
  String? _error;           // For async operations

  Future<void> fetchNotes() async {  // Async READ operation
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      await Future.delayed(Duration(seconds: 2));
      _notes = [
        Note(title: 'Note 1', content: 'Content'),
        Note(title: 'Note 2', content: 'More content'),
      ];
      _isLoading = false;
    } catch (e) {
      _error = e.toString();
      _isLoading = false;
    }
    notifyListeners();
  }
}
```

The problem: three separate variables for one logical concept (the async state). If you forget to set `_isLoading = false` in one branch, your UI gets stuck in a loading state.

### Better Pattern: Encapsulate Async State

Create a class that represents the three states:

```dart
abstract class AsyncState<T> {
  const AsyncState();
}

class AsyncLoading<T> extends AsyncState<T> {
  const AsyncLoading();
}

class AsyncSuccess<T> extends AsyncState<T> {
  final T data;
  const AsyncSuccess(this.data);
}

class AsyncError<T> extends AsyncState<T> {
  final String message;
  const AsyncError(this.message);
}
```

Now you can represent an async operation with a single variable:

```dart
class NotesManager extends ChangeNotifier {
  AsyncState<List<Note>> _notesState = AsyncLoading();

  AsyncState<List<Note>> get notesState => _notesState;

  Future<void> fetchNotes() async {  // Async READ operation
    _notesState = AsyncLoading();
    notifyListeners();

    try {
      await Future.delayed(Duration(seconds: 2));
      final notes = [
        Note(title: 'Note 1', content: 'Content'),
        Note(title: 'Note 2', content: 'More content'),
      ];
      _notesState = AsyncSuccess(notes);
    } catch (e) {
      _notesState = AsyncError(e.toString());
    }
    notifyListeners();
  }
}
```

Now the state is clear and consistent: `_notesState` always represents the complete async status. It's impossible to accidentally show the wrong UI for a given state.

### Using Async State in Widgets

```dart
Consumer<NotesManager>(
  builder: (context, notesManager, child) {
    final state = notesManager.notesState;

    // Pattern match on the state
    if (state is AsyncLoading) {
      return Center(child: CircularProgressIndicator());
    } else if (state is AsyncError) {
      return Center(child: Text('Error: ${state.message}'));
    } else if (state is AsyncSuccess) {
      return ListView.builder(
        itemCount: state.data.length,
        itemBuilder: (context, index) {
          return ListTile(title: Text(state.data[index].title));
        },
      );
    } else {
      return Container();
    }
  },
)
```

This pattern makes it impossible to accidentally show the wrong UI for a given state.

## Riverpod: The Functional Alternative

Riverpod is a newer state management solution that improves on Provider. It uses functional programming patterns and handles some edge cases Provider doesn't.

### Key Differences from Provider

**Provider:**
- Uses `ChangeNotifier` (object-oriented)
- Requires context to access providers
- Rebuilds widgets that access the provider

**Riverpod:**
- Uses functional providers
- No context needed—access providers directly
- Better for complex state dependencies
- More immutable by default

### How Riverpod Works with CRUD

Riverpod providers are defined as functions that return state:

```dart
// Simple state provider
final counterProvider = StateProvider<int>((ref) => 0);

// Notifier for CRUD operations
class NotesNotifier extends StateNotifier<List<Note>> {
  NotesNotifier() : super([]);

  void addNote(Note note) => state = [...state, note];  // CREATE

  void updateNote(int index, Note updated) => state = [  // UPDATE
    ...state.sublist(0, index),
    updated,
    ...state.sublist(index + 1),
  ];

  void deleteNote(int index) => state = [  // DELETE
    ...state.sublist(0, index),
    ...state.sublist(index + 1),
  ];
}

final notesProvider = StateNotifierProvider<NotesNotifier, List<Note>>(
  (ref) => NotesNotifier(),
);

// For async READ operations
final notesAsyncProvider = FutureProvider<List<Note>>((ref) async {
  await Future.delayed(Duration(seconds: 2));
  return [
    Note(title: 'Note 1', content: 'Content'),
    Note(title: 'Note 2', content: 'More content'),
  ];
});
```

### Using Riverpod in Widgets

```dart
class NotesList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    // READ operation - watch the provider
    final notes = ref.watch(notesProvider);

    return ListView.builder(
      itemCount: notes.length,
      itemBuilder: (context, index) {
        return ListTile(
          title: Text(notes[index].title),
          onTap: () {
            // UPDATE or DELETE operation - read without rebuild
            ref.read(notesProvider.notifier).deleteNote(index);
          },
        );
      },
    );
  }
}
```

**Key advantages:**
- No `context` needed—cleaner code
- Built-in async handling with `FutureProvider` and `AsyncValue`
- Providers can depend on other providers elegantly
- Better for testing

### Async with Riverpod: Built-In Pattern

Riverpod has a built-in pattern for async that's cleaner than manual `AsyncState`:

```dart
final notesProvider = FutureProvider<List<Note>>((ref) async {
  await Future.delayed(Duration(seconds: 2));
  return [
    Note(title: 'Note 1', content: 'Content'),
  ];
});

// In a widget
class NotesList extends ConsumerWidget {
  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final notesAsync = ref.watch(notesProvider);

    // Use .when() to handle loading/error/success
    return notesAsync.when(
      loading: () => Center(child: CircularProgressIndicator()),
      error: (error, stackTrace) => Center(child: Text('Error: $error')),
      data: (notes) => ListView.builder(
        itemCount: notes.length,
        itemBuilder: (context, index) {
          return ListTile(title: Text(notes[index].title));
        },
      ),
    );
  }
}
```

This is more elegant than manually tracking loading/error/data states.

## Choosing Between setState(), Provider, and Riverpod

| Scenario | Best Choice | Why |
|----------|-------------|-----|
| Local state (checkbox, form field) | `setState()` | Simple, no overhead |
| App-wide state with CRUD operations | Provider | Industry standard, mature, handles CRUD cleanly |
| Complex state dependencies | Riverpod | Better composability, built-in async handling |
| New projects prioritizing code quality | Riverpod | Cleaner patterns, easier to test |
| Team already knows Provider | Provider | No reason to switch |

For learning purposes, **start with Provider**. It bridges the gap between `setState()` and modern patterns, and its CRUD patterns are explicit and easy to understand. Once you're comfortable, Riverpod is a natural next step.

## Best Practices for CRUD Operations

1. **Validate before CRUD:** Before creating or updating, validate inputs. Before deleting, confirm with the user.

2. **Use immutability for updates:** Create new objects instead of mutating:
   ```dart
   // Bad - mutating directly
   _notes[index].content = newContent;
   
   // Good - creating new object
   _notes[index] = Note(
     title: _notes[index].title,
     content: newContent,
   );
   ```

3. **Handle async errors gracefully.** Never let errors disappear silently. Always show them or log them.

4. **Use unique identifiers for CRUD.** Identifying notes by title (as in examples) works for tutorials but is fragile. Use unique IDs in production.

5. **Keep CRUD methods focused.** One method per operation. Don't combine CREATE and UPDATE into one method.

6. **Test providers independently.** Providers should be testable without building widgets.

---

## Hands-On Project

Ready to apply state management and CRUD operations? Work through [Markdown Notes Project Part C](markdown-notes-project-part-c.html) to implement a complete note-taking app with Create, Read, Update, and Delete operations using Provider.
