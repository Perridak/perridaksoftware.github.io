#!/usr/bin/env dart

// Markdown Note-Taking App - CLI Implementation
// This is the Dart Basics project. In later chapters, this evolves into a Flutter app.

import 'dart:io';

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

  String toMarkdown() {
    final tagString = tags.isNotEmpty ? '\n\nTags: ${tags.join(", ")}' : '';
    return '# $title\n\n$content$tagString';
  }

  @override
  String toString() => '$title (in $folder)';
}

class NoteFolder {
  String name;
  List<Note> notes = [];

  NoteFolder(this.name);

  void addNote(Note note) => notes.add(note);

  void removeNote(String title) {
    notes.removeWhere((note) => note.title == title);
  }

  Note? getNote(String title) {
    try {
      return notes.firstWhere((note) => note.title == title);
    } catch (e) {
      return null;
    }
  }

  List<Note> searchByTag(String tag) {
    return notes.where((note) => note.tags.contains(tag)).toList();
  }

  List<Note> searchByContent(String query) {
    return notes
        .where((note) =>
            note.title.contains(query) || note.content.contains(query))
        .toList();
  }

  @override
  String toString() => 'Folder: $name (${notes.length} notes)';
}

class NoteApp {
  Map<String, NoteFolder> folders = {};
  String? currentFolder;
  bool unsavedChanges = false;

  NoteApp() {
    _createDefaultFolders();
  }

  void _createDefaultFolders() {
    folders['Personal'] = NoteFolder('Personal');
    folders['Work'] = NoteFolder('Work');
    folders['Ideas'] = NoteFolder('Ideas');
    currentFolder = 'Personal';
  }

  void createFolder(String name) {
    if (folders.containsKey(name)) {
      print('Error: Folder "$name" already exists.');
      return;
    }
    folders[name] = NoteFolder(name);
    print('✓ Created folder: $name');
  }

  void listFolders() {
    print('\n📁 Folders:');
    for (var folder in folders.values) {
      final marker = folder.name == currentFolder ? '> ' : '  ';
      print('$marker${folder.name} (${folder.notes.length} notes)');
    }
  }

  void switchFolder(String name) {
    if (!folders.containsKey(name)) {
      print('Error: Folder "$name" not found.');
      return;
    }
    currentFolder = name;
    print('✓ Switched to folder: $name');
  }

  void createNote(String title, String content, List<String> tags) {
    final folder = folders[currentFolder!];
    if (folder!.getNote(title) != null) {
      print('Error: Note "$title" already exists in this folder.');
      return;
    }
    final note = Note(
      title: title,
      content: content,
      folder: currentFolder!,
      tags: tags,
    );
    folder.addNote(note);
    unsavedChanges = true;
    print('✓ Created note: "$title"');
  }

  void deleteNote(String title) {
    final folder = folders[currentFolder!];
    final note = folder!.getNote(title);
    if (note == null) {
      print('Error: Note "$title" not found.');
      return;
    }
    folder.removeNote(title);
    unsavedChanges = true;
    print('✓ Deleted note: "$title"');
  }

  void listNotes() {
    final folder = folders[currentFolder!];
    if (folder!.notes.isEmpty) {
      print('\nNo notes in ${currentFolder!}.');
      return;
    }
    print('\n📝 Notes in ${currentFolder!}:');
    for (int i = 0; i < folder.notes.length; i++) {
      final note = folder.notes[i];
      final tags =
          note.tags.isNotEmpty ? ' [${note.tags.join(", ")}]' : '';
      print('  ${i + 1}. ${note.title}$tags');
    }
  }

  void viewNote(String title) {
    final folder = folders[currentFolder!];
    final note = folder!.getNote(title);
    if (note == null) {
      print('Error: Note "$title" not found.');
      return;
    }
    print('\n${'=' * 50}');
    print(note.toMarkdown());
    print('${'=' * 50}');
  }

  void searchNotes(String query) {
    final folder = folders[currentFolder!];
    final results = folder!.searchByContent(query);
    if (results.isEmpty) {
      print('No notes found matching "$query".');
      return;
    }
    print('\n🔍 Search results for "$query":');
    for (var note in results) {
      print('  - ${note.title}');
    }
  }

  void searchByTag(String tag) {
    List<Note> results = [];
    for (var folder in folders.values) {
      results.addAll(folder.searchByTag(tag));
    }
    if (results.isEmpty) {
      print('No notes found with tag "#$tag".');
      return;
    }
    print('\n🏷️  Notes with tag "#$tag":');
    for (var note in results) {
      print('  - ${note.title} (in ${note.folder})');
    }
  }

  void exportNote(String title, String filename) {
    final folder = folders[currentFolder!];
    final note = folder!.getNote(title);
    if (note == null) {
      print('Error: Note "$title" not found.');
      return;
    }

    try {
      final file = File(filename);
      file.writeAsStringSync(note.toMarkdown());
      print('✓ Exported note to: $filename');
    } catch (e) {
      print('Error exporting note: $e');
    }
  }

  void saveSession(String filename) {
    try {
      final buffer = StringBuffer();
      for (var folderName in folders.keys) {
        final folder = folders[folderName]!;
        buffer.writeln('=== FOLDER: $folderName ===');
        for (var note in folder.notes) {
          buffer.writeln('\n--- NOTE: ${note.title} ---');
          buffer.writeln('TAGS: ${note.tags.join(",")}');
          buffer.writeln(note.content);
        }
        buffer.writeln('\n');
      }
      final file = File(filename);
      file.writeAsStringSync(buffer.toString());
      unsavedChanges = false;
      print('✓ Session saved to: $filename');
    } catch (e) {
      print('Error saving session: $e');
    }
  }

  void stats() {
    int totalNotes = 0;
    int totalWords = 0;
    Map<String, int> tagCount = {};

    for (var folder in folders.values) {
      totalNotes += folder.notes.length;
      for (var note in folder.notes) {
        totalWords += note.content.split(' ').length;
        for (var tag in note.tags) {
          tagCount[tag] = (tagCount[tag] ?? 0) + 1;
        }
      }
    }

    print('\n📊 Statistics:');
    print('  Total notes: $totalNotes');
    print('  Total words: $totalWords');
    print('  Folders: ${folders.length}');
    if (tagCount.isNotEmpty) {
      print('  Most used tags: ${tagCount.entries.first.key} (${tagCount.entries.first.value})');
    }
  }

  void help() {
    print('''
╔════════════════════════════════════════════════════════╗
║           📓 Markdown Note-Taking App                  ║
╚════════════════════════════════════════════════════════╝

Commands:
  new <title> <content> [tag1,tag2]  - Create a new note
  list                               - List notes in current folder
  view <title>                       - View a note
  delete <title>                     - Delete a note
  search <query>                     - Search notes by content
  tag <tag>                          - Search notes by tag
  export <title> <filename>          - Export note to file
  
Folder commands:
  folders                            - List all folders
  folder <name>                      - Create new folder
  use <name>                         - Switch to folder
  
Session commands:
  save <filename>                    - Save all notes to file
  stats                              - Show statistics
  
  help                               - Show this help
  exit                               - Exit the app

Example:
  new "My First Note" "This is the content" "personal,dart"
''');
  }
}

void main() {
  final app = NoteApp();
  final stdin = io.stdin;

  print('''
╔════════════════════════════════════════════════════════╗
║           📓 Markdown Note-Taking App                  ║
║              Type 'help' for commands                  ║
╚════════════════════════════════════════════════════════╝
''');

  // Demo: Add some sample notes
  app.createNote(
    'Dart Learning Progress',
    'Started learning Dart today. Variables and null safety are impressive concepts.',
    ['dart', 'learning'],
  );
  app.createNote(
    'Flutter Project Ideas',
    'Ideas for learning project: Note-taking app, To-do list, Budget tracker.',
    ['flutter', 'ideas'],
  );

  while (true) {
    stdout.write('\n[$currentFolder] > ');
    final input = stdin.readLineSync();

    if (input == null || input.isEmpty) continue;

    final parts = input.split(' ');
    final command = parts[0].toLowerCase();

    try {
      switch (command) {
        case 'help':
          app.help();

        case 'new':
          if (parts.length < 3) {
            print('Usage: new <title> <content> [tag1,tag2]');
          } else {
            final title = parts[1];
            final content = parts.sublist(2).join(' ');
            final tags = parts.length > 3 && parts.last.contains(',')
                ? parts.last.split(',')
                : <String>[];
            app.createNote(title, content, tags);
          }
          break;

        case 'list':
          app.listNotes();
          break;

        case 'view':
          if (parts.length < 2) {
            print('Usage: view <title>');
          } else {
            app.viewNote(parts.sublist(1).join(' '));
          }
          break;

        case 'delete':
          if (parts.length < 2) {
            print('Usage: delete <title>');
          } else {
            app.deleteNote(parts.sublist(1).join(' '));
          }
          break;

        case 'search':
          if (parts.length < 2) {
            print('Usage: search <query>');
          } else {
            app.searchNotes(parts.sublist(1).join(' '));
          }
          break;

        case 'tag':
          if (parts.length < 2) {
            print('Usage: tag <tagname>');
          } else {
            app.searchByTag(parts[1]);
          }
          break;

        case 'export':
          if (parts.length < 3) {
            print('Usage: export <title> <filename>');
          } else {
            final title = parts[1];
            final filename = parts[2];
            app.exportNote(title, filename);
          }
          break;

        case 'folders':
          app.listFolders();
          break;

        case 'folder':
          if (parts.length < 2) {
            print('Usage: folder <name>');
          } else {
            app.createFolder(parts.sublist(1).join(' '));
          }
          break;

        case 'use':
          if (parts.length < 2) {
            print('Usage: use <folder>');
          } else {
            app.switchFolder(parts[1]);
          }
          break;

        case 'save':
          if (parts.length < 2) {
            print('Usage: save <filename>');
          } else {
            app.saveSession(parts[1]);
          }
          break;

        case 'stats':
          app.stats();
          break;

        case 'exit':
          if (app.unsavedChanges) {
            stdout.write('You have unsaved changes. Exit anyway? (y/n): ');
            final confirm = stdin.readLineSync();
            if (confirm?.toLowerCase() == 'y') {
              print('Goodbye!');
              exit(0);
            }
          } else {
            print('Goodbye!');
            exit(0);
          }
          break;

        default:
          print('Unknown command: $command. Type "help" for available commands.');
      }
    } catch (e) {
      print('Error: $e');
    }
  }
}
