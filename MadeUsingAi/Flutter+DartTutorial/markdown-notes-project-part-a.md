# Markdown Note-Taking App — Dart Basics Project

## Overview

This is your hands-on project for the **Dart Basics** chapter. You'll build a command-line note-taking application that demonstrates core Dart concepts including classes, collections, functions, and file I/O.

The app stores notes in memory with the ability to save and load sessions from disk. In later chapters, you'll evolve this into a full Flutter application with persistent storage and a rich UI.

## Learning Objectives

By completing this project, you will:

1. **Design classes** that represent domain objects (`Note`, `NoteFolder`, `NoteApp`)
2. **Use collections** (`List<T>`, `Map<String, T>`, `Set<T>`) to organize data
3. **Implement methods** that search, filter, and manipulate data
4. **Handle nullable types** safely with Dart's null safety
5. **Perform file I/O** to save and load sessions
6. **Build a simple CLI interface** using string commands and `stdin`/`stdout`
7. **Apply OOP principles** like encapsulation and separation of concerns

## Project Structure

```
markdown_notes_app.dart
├── Note class              // Represents a single note
├── NoteFolder class        // Represents a folder containing notes
├── NoteApp class           // Main app logic and command handling
└── main() function         // CLI loop and user interaction
```

## Key Classes

### Note

Represents a single note with title, content, folder, creation date, and tags.

**Responsibilities:**
- Store note metadata
- Convert note to Markdown format
- Provide string representation

**Concepts covered:**
- Required named parameters
- Initialization with default values (`DateTime.now()`)
- String interpolation
- Collections (List of tags)

### NoteFolder

Represents a folder containing multiple notes. Provides methods to add, remove, and search notes.

**Responsibilities:**
- Manage a collection of notes
- Search notes by title, content, or tag
- Report folder statistics

**Concepts covered:**
- Collections (`List<Note>`)
- Methods that filter and search (`where()`, `firstWhere()`)
- Nullable return types (`Note?`)

### NoteApp

The main application controller. Manages folders, handles commands, and maintains app state.

**Responsibilities:**
- Create and switch between folders
- Create, delete, and view notes
- Search across the entire app
- Save and load sessions
- Provide help and statistics

**Concepts covered:**
- Maps (`Map<String, NoteFolder>`)
- Method organization (CRUD operations)
- State management (current folder, unsaved changes)
- File I/O for save/load
- Control flow and error handling

## Implementation Steps

### Step 1: Define the Note Class (15 mins)

Create a `Note` class with:
- Properties: `title`, `content`, `folder`, `created`, `tags`
- Constructor with required named parameters
- `toMarkdown()` method that formats the note
- `toString()` method for display

**Key concepts:** Classes, named parameters, DateTime, List<String>

### Step 2: Define the NoteFolder Class (15 mins)

Create a `NoteFolder` class with:
- Properties: `name` and `notes` (List<Note>)
- `addNote()` and `removeNote()` methods
- `getNote()` method that returns `Note?` (nullable)
- `searchByTag()` and `searchByContent()` methods using `.where()`

**Key concepts:** Collections, generics, filtering, null safety

### Step 3: Build the NoteApp Class (20 mins)

Create a `NoteApp` class with:
- Properties: `folders` (Map<String, NoteFolder>), `currentFolder`, `unsavedChanges`
- Methods for folder management: `createFolder()`, `switchFolder()`, `listFolders()`
- Methods for note operations: `createNote()`, `deleteNote()`, `listNotes()`, `viewNote()`
- Search methods: `searchNotes()`, `searchByTag()`

**Key concepts:** Maps, OOP design, state management, control flow

### Step 4: Add File I/O (10 mins)

Add methods for:
- `saveSession(filename)` — Save all notes to a text file
- `exportNote(title, filename)` — Export a single note

**Key concepts:** File I/O, exception handling, string building

### Step 5: Build the CLI Loop (10 mins)

In `main()`:
- Create a `NoteApp` instance
- Implement a loop that reads user input
- Parse commands and call appropriate methods
- Display results to the user
- Handle the "exit" command with unsaved changes check

**Key concepts:** stdin/stdout, string parsing, control flow, exception handling

## Commands to Implement

| Command | Purpose | Example |
|---------|---------|---------|
| `new <title> <content> [tags]` | Create a note | `new "Ideas" "Great app concept" "flutter,ideas"` |
| `list` | Show notes in current folder | `list` |
| `view <title>` | Display full note | `view "Ideas"` |
| `delete <title>` | Remove a note | `delete "Ideas"` |
| `search <query>` | Find notes by content | `search "flutter"` |
| `tag <tagname>` | Find notes by tag | `tag "flutter"` |
| `export <title> <file>` | Save note to file | `export "Ideas" notes.md` |
| `folders` | List all folders | `folders` |
| `folder <name>` | Create new folder | `folder "Archive"` |
| `use <name>` | Switch folder | `use "Work"` |
| `save <file>` | Save session | `save session.txt` |
| `stats` | Show statistics | `stats` |
| `help` | Show help | `help` |
| `exit` | Quit the app | `exit` |

## Development Checklist

- [ ] Note class created with all properties
- [ ] NoteFolder class with add, remove, get methods
- [ ] NoteFolder search methods implemented
- [ ] NoteApp class structure set up
- [ ] Folder management methods work
- [ ] Note CRUD operations work
- [ ] Search functionality across folders works
- [ ] File I/O (save/export) implemented
- [ ] CLI loop processes commands
- [ ] Error handling for invalid commands
- [ ] Help text displays correctly
- [ ] Unsaved changes tracking works
- [ ] All commands tested and working

## Testing Scenarios

1. **Create and list**: Create 3 notes, list them
2. **Search**: Search by content keyword, verify results
3. **Tag search**: Add tags to notes, search by tag across folders
4. **Folder switching**: Create a new folder, switch to it, add notes, verify they're separate
5. **Export**: Export a note to a file, view the file contents
6. **Save session**: Save all notes, verify the file is readable
7. **Exit with changes**: Modify notes and exit without saving, verify the warning appears

## Stretch Goals (Optional)

- [ ] Edit existing notes
- [ ] Backlinks between notes (`[[@title]]` syntax)
- [ ] Date-based queries ("notes from last week")
- [ ] Markdown rendering/preview
- [ ] Import notes from external files
- [ ] Note categories or hierarchies

## How This Evolves

In future chapters, you'll transform this app:

1. **Flutter Widgets** — Convert CLI to graphical UI with text input fields and buttons
2. **State Management** — Use Provider or Riverpod instead of in-memory storage
3. **Routing & Navigation** — Add multiple screens (notes list, note detail, search results)
4. **Best Practices** — Add SQLite storage, error handling, testing, and documentation

The core logic you build here will form the foundation of your Flutter app.

## Common Mistakes to Avoid

1. **Forgetting null safety**: Remember that `Note?` means nullable; check before using `?.`
2. **Not tracking unsaved changes**: The app should warn before exiting with modifications
3. **Case-sensitive commands**: Be consistent with command parsing (consider `.toLowerCase()`)
4. **Not validating input**: Check that required parameters exist before using them
5. **Silent failures**: Always provide feedback to the user (success/error messages)

## Helpful Tips

- Use `print()` liberally for debugging and user feedback
- Leverage `.where()` and `.firstWhere()` on lists for filtering
- Null coalescing (`??`) helps with default values
- String interpolation (`'$variable'`) makes output cleaner
- The cascade operator (`..`) can chain multiple operations on an object

## Estimated Time

- Understanding the project: 10 minutes
- Implementing Note class: 15 minutes
- Implementing NoteFolder class: 20 minutes
- Implementing NoteApp class: 25 minutes
- Building CLI loop: 15 minutes
- Testing and debugging: 15 minutes

**Total: 60 minutes of hands-on coding practice**

This aligns with the chapter's goal of reinforcing concepts through practical application.
