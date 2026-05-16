# Databases

Building useful software requires persisting data. This chapter teaches how to work with databases in Flutter, starting with the simplest local option (SQLite), then showing how NoSQL offers a modern alternative for both local and cloud use, and finally demonstrating how to connect to enterprise databases.

The progression is intentional: master local storage first, then scale your thinking to cloud alternatives and enterprise backends. The architecture lesson is the same everywhere—you'll see that pattern repeated across all database types.

## Part 1: SQLite for Local Storage

SQLite is the most widely used database in mobile development. It's lightweight, requires no server setup, stores data directly on the device, and works on every platform Flutter supports.

### Why SQLite?

SQLite gives you:

- **Offline-first capability:** Your app works without internet. Sync data when connectivity returns.
- **Fast queries:** Data lives on the device. No network latency.
- **Simple setup:** No server to manage. The database is a file on the device.
- **SQL familiarity:** If you know SQL, you know SQLite.

SQLite is ideal for apps where the device is the primary data store: note-taking apps, to-do lists, offline-capable news readers, or any app where each user has their own local data.

### Setting Up SQLite

Flutter accesses SQLite through the `sqflite` package:

```yaml
dependencies:
  sqflite: ^2.3.0
  path_provider: ^2.1.0
  path: ^1.8.0
```

The `path_provider` package helps locate where to store the database file on the device.

### The Architecture Pattern

Regardless of database type, a sound architecture separates concerns:

```
UI Layer (Widgets)
    ↓
State Management (Provider, BLoC, etc.)
    ↓
Repository (hides database implementation)
    ↓
Database Helper / Data Layer
    ↓
SQLite
```

This matters because if you ever migrate from SQLite to a cloud database, only the repository implementation changes. Everything else stays the same.

### Creating a Database

Define your data model first:

```dart
class Note {
  final int? id; // null until saved
  final String title;
  final String content;
  final String folder;
  final List<String> tags;

  const Note({
    this.id,
    required this.title,
    required this.content,
    required this.folder,
    required this.tags,
  });

  // Convert to/from database map
  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'title': title,
      'content': content,
      'folder': folder,
      'tags': tags.join(','), // Store as comma-separated string
    };
  }

  static Note fromMap(Map<String, dynamic> map) {
    return Note(
      id: map['id'],
      title: map['title'],
      content: map['content'],
      folder: map['folder'],
      tags: (map['tags'] as String).split(','),
    );
  }
}
```

Now create a database helper to manage the connection and operations:

```dart
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';

class DatabaseHelper {
  static const String _databaseName = 'notes.db';
  static const int _databaseVersion = 1;
  static const String _tableName = 'notes';

  // Singleton pattern: one database instance for the app
  static final DatabaseHelper _instance = DatabaseHelper._internal();

  factory DatabaseHelper() {
    return _instance;
  }

  DatabaseHelper._internal();

  Database? _database;

  // Lazy initialization: database is opened when first accessed
  Future<Database> get database async {
    _database ??= await _initializeDatabase();
    return _database!;
  }

  Future<Database> _initializeDatabase() async {
    // Get the database location on the device
    final databasePath = await getDatabasesPath();
    final path = join(databasePath, _databaseName);

    // Open the database, creating it if it doesn't exist
    return openDatabase(
      path,
      version: _databaseVersion,
      onCreate: _onCreate,
      onUpgrade: _onUpgrade,
    );
  }

  // Called once when database is first created
  Future<void> _onCreate(Database db, int version) async {
    await db.execute('''
      CREATE TABLE $_tableName (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        folder TEXT NOT NULL,
        tags TEXT NOT NULL
      )
    ''');
  }

  // Called when database version changes
  Future<void> _onUpgrade(Database db, int oldVersion, int newVersion) async {
    // Handle schema migrations when you add columns or tables
    if (oldVersion < 2) {
      // Example: await db.execute('ALTER TABLE $_tableName ADD COLUMN new_column TEXT');
    }
  }
}
```

### CRUD Operations

Create a repository to encapsulate database operations:

```dart
class NoteRepository {
  final DatabaseHelper _dbHelper = DatabaseHelper();

  // Create (Insert)
  Future<int> createNote(Note note) async {
    final db = await _dbHelper.database;
    return await db.insert('notes', note.toMap());
  }

  // Read (Query all)
  Future<List<Note>> getAllNotes() async {
    final db = await _dbHelper.database;
    final maps = await db.query('notes');
    return [for (final map in maps) Note.fromMap(map)];
  }

  // Read (Query one)
  Future<Note?> getNoteById(int id) async {
    final db = await _dbHelper.database;
    final maps = await db.query(
      'notes',
      where: 'id = ?',
      whereArgs: [id],
    );
    return maps.isNotEmpty ? Note.fromMap(maps.first) : null;
  }

  // Update
  Future<void> updateNote(Note note) async {
    final db = await _dbHelper.database;
    await db.update(
      'notes',
      note.toMap(),
      where: 'id = ?',
      whereArgs: [note.id],
    );
  }

  // Delete
  Future<void> deleteNote(int id) async {
    final db = await _dbHelper.database;
    await db.delete('notes', where: 'id = ?', whereArgs: [id]);
  }
}
```

### Using the Repository in Your App

With Provider for state management:

```dart
class NoteProvider extends ChangeNotifier {
  final NoteRepository _repository = NoteRepository();
  List<Note> _notes = [];

  List<Note> get notes => _notes;

  Future<void> loadNotes() async {
    _notes = await _repository.getAllNotes();
    notifyListeners();
  }

  Future<void> addNote(Note note) async {
    await _repository.createNote(note);
    await loadNotes();
  }

  Future<void> updateNote(Note note) async {
    await _repository.updateNote(note);
    await loadNotes();
  }

  Future<void> deleteNote(int id) async {
    await _repository.deleteNote(id);
    await loadNotes();
  }
}
```

In a widget, use `StreamBuilder` or `Consumer` to display notes:

```dart
class NoteListScreen extends StatefulWidget {
  @override
  State<NoteListScreen> createState() => _NoteListScreenState();
}

class _NoteListScreenState extends State<NoteListScreen> {
  @override
  void initState() {
    super.initState();
    // Load notes when screen opens
    context.read<NoteProvider>().loadNotes();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Notes')),
      body: Consumer<NoteProvider>(
        builder: (context, provider, child) {
          return ListView.builder(
            itemCount: provider.notes.length,
            itemBuilder: (context, index) {
              final note = provider.notes[index];
              return ListTile(
                title: Text(note.title),
                subtitle: Text(note.content),
                onTap: () => Navigator.push(context, MaterialPageRoute(
                  builder: (_) => NoteDetailScreen(note: note),
                )),
                trailing: IconButton(
                  icon: Icon(Icons.delete),
                  onPressed: () => provider.deleteNote(note.id!),
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () => Navigator.push(context, MaterialPageRoute(
          builder: (_) => CreateNoteScreen(),
        )),
        child: Icon(Icons.add),
      ),
    );
  }
}
```

### SQLite Benefits and Drawbacks

**Benefits:**
- No server required. Works offline. Data stays on the device.
- ACID compliance ensures data integrity.
- Fast queries—no network latency.
- Widely tested and battle-hardened in production apps.

**Drawbacks:**
- Single-device data. No built-in synchronization between devices.
- Not suitable for massive datasets (SQLite is optimized for single-user, not high concurrency).
- Schema changes require migrations.

**When to use:** Apps with offline-first requirements, where each user's data lives on their device.

---

## Part 2: NoSQL—A Modern Alternative

NoSQL databases challenge the relational model, offering flexibility at the cost of strict schemas. They excel at both local and cloud storage, making them a bridge between SQLite and enterprise databases.

### Local NoSQL: Hive

Hive is a lightweight, high-performance NoSQL database written in Dart. It's simpler than SQLite for many use cases.

```yaml
dependencies:
  hive: ^2.2.0
  hive_flutter: ^1.1.0
```

**Setup:**

```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  Hive.registerAdapter(NoteAdapter());
  runApp(MyApp());
}
```

**Define your model with annotations:**

```dart
import 'package:hive/hive.dart';

@HiveType(typeId: 0)
class Note {
  @HiveField(0)
  final int id;

  @HiveField(1)
  final String title;

  @HiveField(2)
  final String content;

  @HiveField(3)
  final String folder;

  @HiveField(4)
  final List<String> tags;

  Note({
    required this.id,
    required this.title,
    required this.content,
    required this.folder,
    required this.tags,
  });
}
```

Generate the adapter with `flutter pub run build_runner build`.

**Operations are simple:**

```dart
class NoteRepository {
  static const String _boxName = 'notes';

  // Create
  Future<void> createNote(Note note) async {
    final box = await Hive.openBox<Note>(_boxName);
    await box.put(note.id, note); // Key-value: id → Note
  }

  // Read
  Future<List<Note>> getAllNotes() async {
    final box = await Hive.openBox<Note>(_boxName);
    return box.values.toList();
  }

  // Update
  Future<void> updateNote(Note note) async {
    final box = await Hive.openBox<Note>(_boxName);
    await box.put(note.id, note);
  }

  // Delete
  Future<void> deleteNote(int id) async {
    final box = await Hive.openBox<Note>(_boxName);
    await box.delete(id);
  }
}
```

### Cloud NoSQL: Firebase Firestore

Firestore is Google's cloud NoSQL database. It's the bridge between local Hive and enterprise databases—you get cloud storage with offline support.

**Setup:**

```yaml
dependencies:
  firebase_core: ^3.0.0
  cloud_firestore: ^5.0.0
```

Initialize Firebase in `main()`:

```dart
import 'package:firebase_core/firebase_core.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();
  runApp(MyApp());
}
```

**Use Firestore in your repository:**

```dart
class NoteRepository {
  final FirebaseFirestore _firestore = FirebaseFirestore.instance;
  static const String _collection = 'notes';

  // Create
  Future<void> createNote(Note note) async {
    await _firestore.collection(_collection).doc(note.id.toString()).set({
      'title': note.title,
      'content': note.content,
      'folder': note.folder,
      'tags': note.tags,
    });
  }

  // Read (with real-time updates)
  Stream<List<Note>> notesStream() {
    return _firestore.collection(_collection).snapshots().map((snapshot) {
      return [
        for (final doc in snapshot.docs)
          Note(
            id: int.parse(doc.id),
            title: doc['title'],
            content: doc['content'],
            folder: doc['folder'],
            tags: List<String>.from(doc['tags']),
          )
      ];
    });
  }

  // Update
  Future<void> updateNote(Note note) async {
    await _firestore.collection(_collection).doc(note.id.toString()).update({
      'title': note.title,
      'content': note.content,
      'folder': note.folder,
      'tags': note.tags,
    });
  }

  // Delete
  Future<void> deleteNote(int id) async {
    await _firestore.collection(_collection).doc(id.toString()).delete();
  }
}
```

**Using Firestore in widgets with StreamBuilder:**

```dart
class NoteListScreen extends StatelessWidget {
  final NoteRepository _repository = NoteRepository();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Notes')),
      body: StreamBuilder<List<Note>>(
        stream: _repository.notesStream(),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return Center(child: CircularProgressIndicator());
          }
          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }
          final notes = snapshot.data ?? [];
          return ListView.builder(
            itemCount: notes.length,
            itemBuilder: (context, index) {
              final note = notes[index];
              return ListTile(
                title: Text(note.title),
                subtitle: Text(note.content),
                trailing: IconButton(
                  icon: Icon(Icons.delete),
                  onPressed: () => _repository.deleteNote(note.id),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
```

### NoSQL Benefits and Drawbacks

**Benefits:**
- **Flexible schema:** Add fields without migrations. Great for evolving requirements.
- **Cloud + offline:** Firestore syncs automatically. Works offline, syncs when connected.
- **Real-time updates:** Changes push to all clients instantly (Firestore).
- **Simple for simple data:** No complex joins. Great for document-oriented data.

**Drawbacks:**
- **No strong consistency guarantees:** Eventual consistency can surprise you (distributed systems trade-off).
- **Cost at scale:** Firebase charges per read/write. High-traffic apps get expensive.
- **Limited querying:** Can't do complex joins like SQL databases.
- **Vendor lock-in:** With Firebase, you're tied to Google Cloud.

**When to use:** Real-time collaborative apps (Firebase), offline-first mobile apps (Hive), or when your data structure is hierarchical and doesn't require complex relationships.

---

## Part 3: Enterprise Databases

Enterprise databases (MySQL, PostgreSQL, Oracle, SQL Server) live on servers. Your Flutter app can't connect directly—security requires a backend intermediary.

### The Architecture Pattern

```
Flutter App
    ↓ (HTTP/REST or GraphQL)
Backend API (Node, Django, Java, Go, etc.)
    ↓ (Database Driver)
Enterprise Database
```

Your Flutter app sends requests to an API. The API queries the database and returns data. This separation ensures:

- Database credentials stay server-side (secure)
- You can scale the backend independently
- Multiple clients can share the same database

### Connecting to MySQL

Example: Your backend is a REST API running on a server.

**In Flutter, create an API service:**

```dart
import 'package:http/http.dart' as http;
import 'dart:convert';

class ApiService {
  static const String _baseUrl = 'https://api.example.com';

  // Fetch all notes
  Future<List<Note>> getNotes() async {
    final response = await http.get(
      Uri.parse('$_baseUrl/notes'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode == 200) {
      final List<dynamic> data = jsonDecode(response.body);
      return [for (final item in data) Note.fromJson(item)];
    } else {
      throw Exception('Failed to load notes');
    }
  }

  // Create a note
  Future<Note> createNote(Note note) async {
    final response = await http.post(
      Uri.parse('$_baseUrl/notes'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(note.toJson()),
    );

    if (response.statusCode == 201) {
      return Note.fromJson(jsonDecode(response.body));
    } else {
      throw Exception('Failed to create note');
    }
  }

  // Update a note
  Future<void> updateNote(int id, Note note) async {
    final response = await http.put(
      Uri.parse('$_baseUrl/notes/$id'),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer $token',
      },
      body: jsonEncode(note.toJson()),
    );

    if (response.statusCode != 200) {
      throw Exception('Failed to update note');
    }
  }

  // Delete a note
  Future<void> deleteNote(int id) async {
    final response = await http.delete(
      Uri.parse('$_baseUrl/notes/$id'),
      headers: {'Authorization': 'Bearer $token'},
    );

    if (response.statusCode != 204) {
      throw Exception('Failed to delete note');
    }
  }
}
```

**Your repository abstracts the API:**

```dart
class NoteRepository {
  final ApiService _apiService = ApiService();

  Future<List<Note>> getAllNotes() => _apiService.getNotes();
  Future<Note> createNote(Note note) => _apiService.createNote(note);
  Future<void> updateNote(int id, Note note) => _apiService.updateNote(id, note);
  Future<void> deleteNote(int id) => _apiService.deleteNote(id);
}
```

**Your state management uses the repository:**

```dart
class NoteProvider extends ChangeNotifier {
  final NoteRepository _repository = NoteRepository();
  List<Note> _notes = [];
  bool _isLoading = false;

  List<Note> get notes => _notes;
  bool get isLoading => _isLoading;

  Future<void> loadNotes() async {
    _isLoading = true;
    notifyListeners();
    _notes = await _repository.getAllNotes();
    _isLoading = false;
    notifyListeners();
  }

  Future<void> addNote(Note note) async {
    await _repository.createNote(note);
    await loadNotes();
  }
}
```

**In widgets, use FutureBuilder for async operations:**

```dart
class NoteListScreen extends StatefulWidget {
  @override
  State<NoteListScreen> createState() => _NoteListScreenState();
}

class _NoteListScreenState extends State<NoteListScreen> {
  @override
  void initState() {
    super.initState();
    context.read<NoteProvider>().loadNotes();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Notes')),
      body: Consumer<NoteProvider>(
        builder: (context, provider, child) {
          if (provider.isLoading) {
            return Center(child: CircularProgressIndicator());
          }
          return ListView.builder(
            itemCount: provider.notes.length,
            itemBuilder: (context, index) {
              final note = provider.notes[index];
              return ListTile(
                title: Text(note.title),
                subtitle: Text(note.content),
                trailing: IconButton(
                  icon: Icon(Icons.delete),
                  onPressed: () => provider.deleteNote(note.id!),
                ),
              );
            },
          );
        },
      ),
    );
  }
}
```

### The Same Pattern Works for All Enterprise Databases

Whether your backend connects to MySQL, PostgreSQL, Oracle, or SQL Server, the Flutter code is identical. Only the backend changes. This is the power of the repository pattern.

- **MySQL backend** → Same Flutter code
- **PostgreSQL backend** → Same Flutter code
- **SQL Server backend** → Same Flutter code

### Enterprise Database Benefits and Drawbacks

**Benefits:**
- **Centralized data:** One source of truth. All clients see the same data.
- **ACID compliance:** Strong consistency and data integrity.
- **Powerful querying:** Complex joins, aggregations, transactions.
- **Scalability:** Designed for high concurrency and large datasets.

**Drawbacks:**
- **Offline doesn't work:** App requires internet for all operations.
- **API is a bottleneck:** Network latency adds to every operation.
- **Server costs:** You maintain and pay for server infrastructure.
- **Complexity:** Requires a backend developer and infrastructure knowledge.

**When to use:** Multi-user apps where all users share the same data (CRM, collaboration tools, social networks). Apps with high consistency requirements (financial transactions).

---

## Comparison: Choosing the Right Database

| Aspect | SQLite | Hive | Firestore | Enterprise DB |
|--------|--------|------|-----------|---------------|
| **Storage** | Local device | Local device | Cloud | Server |
| **Multi-user** | No | No | Yes | Yes |
| **Offline** | Yes | Yes | Yes (cached) | No |
| **Real-time sync** | Manual | Manual | Automatic | Via API |
| **Setup complexity** | Low | Low | Medium (Firebase setup) | High (backend required) |
| **Query power** | SQL (strong) | Basic (key-value) | Document queries | SQL (very strong) |
| **Cost** | Free | Free | Scales with usage | Infrastructure costs |
| **Best for** | Offline apps, local notes | Simple local storage | Real-time collab | Multi-user, enterprise |

---

## Architecture Principles

Regardless of which database you choose, follow these principles:

1. **Separate concerns:** Database logic lives in repositories, not widgets.
2. **Swap implementations:** Your app shouldn't care if you use SQLite or Firestore. Only the repository knows.
3. **Use the same state management:** Provider, BLoC, or Riverpod manages data the same way regardless of database.
4. **Handle errors:** Network failures (enterprise), sync conflicts (cloud), or schema mismatches (local).

By building with this architecture from the start, migrating from one database to another becomes straightforward.

---

## Hands-On Next Steps

In the project guides, we'll implement the Markdown Notes app with SQLite first. This teaches you the foundation. Later, you can explore swapping in Hive or Firestore by changing only the repository—the rest of your app stays unchanged.

Start local. Master the patterns. Scale when needed.
