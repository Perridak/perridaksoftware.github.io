# Testing

Testing is how you verify that your code works before users discover it doesn't. This chapter teaches testing with a Test-Driven Development (TDD) focus—writing tests before implementation to clarify what you're building and ensure it works from the start.

TDD isn't the only approach. Behavior-Driven Development (BDD) uses similar principles but emphasizes natural-language scenarios that communicate with non-technical stakeholders. Both complement each other. This chapter teaches TDD fundamentals and introduces BDD as a complementary technique.

## Understanding Test Types

Flutter has three levels of testing, each serving a different purpose.

**Unit tests** verify that a single function, method, or class works correctly. They're fast, run without a device, and test pure Dart code in isolation. Example: testing that a `Counter` class increments correctly.

**Widget tests** (called component tests in general Dart) verify that widgets and UI components behave correctly. They render widgets in a virtual environment without a real device, simulating user interactions. Example: testing that a button tap increments a counter on screen.

**Integration tests** verify that your entire app works end-to-end. They run on real or simulated devices and test complete workflows. Example: testing that a user can log in, navigate to their notes, and create a new note.

The test pyramid guides test distribution: write many unit tests (fast, cheap to run), fewer widget tests (medium speed and cost), and few integration tests (slow, expensive). Aim for roughly 70% unit, 20% widget, 10% integration.

This chapter focuses on unit testing, the foundation. Widget and integration testing use the same principles but require the Flutter test framework.

## The Test Package and Framework

Dart's `test` package provides the core framework for writing tests. Flutter projects include `flutter_test`, which extends `test` with utilities for widget testing.

### Setting Up

For pure Dart tests (no widgets), add the `test` package to dev dependencies:

```yaml
dev_dependencies:
  test: ^1.25.0
```

For Flutter projects, `flutter_test` comes automatically with the SDK.

### File Organization

By convention, test files live in a `test/` directory at your project root, mirroring your source structure:

```
lib/
├── models/
│   └── note.dart
├── providers/
│   └── notes_provider.dart
test/
├── models/
│   └── note_test.dart
├── providers/
│   └── notes_provider_test.dart
```

Test files always end with `_test.dart`. This naming convention is how the test runner discovers and runs them.

## Writing Your First Test

The basic structure of a test is simple:

```dart
import 'package:test/test.dart';

void main() {
  test('description of what should happen', () {
    // Arrange: set up test data
    final result = 2 + 3;
    
    // Assert: verify the result
    expect(result, 5);
  });
}
```

Every test has three parts:

1. **Arrange:** Set up the code under test. Create objects, initialize state, mock dependencies.
2. **Act:** Execute the code you're testing.
3. **Assert:** Verify the result matches expectations using `expect()`.

Running tests is straightforward:

```bash
# Run all tests in the test/ directory
flutter test

# Or for pure Dart projects
dart test
```

## Test Naming: Why It Matters

Test names influence how you think about testing. The naming convention you choose subtly shapes what you test and how thoroughly.

### Imperative Style: testFeatureDoesX

Imperative names describe what the code does:

```dart
test('counterIncrements', () { ... });
test('noteListDisplaysAllNotes', () { ... });
test('userCanEditNoteTitle', () { ... });
```

This style is procedural—it describes actions. Imperative names make sense when you're thinking about implementation details.

### Declarative/BDD Style: FeatureShouldDoXWhen

Declarative (BDD-style) names describe requirements and conditions:

```dart
test('counter should increment when button is pressed', () { ... });
test('note list should display all notes when app starts', () { ... });
test('user should be able to edit note title after tapping edit', () { ... });
```

This style is requirements-focused. It uses "should" to state expected behavior and "when" to specify conditions. These names read like specifications that non-technical stakeholders can understand.

### Why the Difference Matters

Imperative names focus on implementation: "What does the code do?" Declarative names focus on requirements: "What should the system do?" This seemingly minor difference has real consequences:

- **Imperative tests** risk testing implementation details rather than actual behavior. You might verify that a method is called, not that the user sees what they expect.
- **Declarative tests** naturally lead to testing behavior that matters. If you're writing "should display all notes when app starts," you're forced to verify that notes actually appear, not just that a method is called.

Research in BDD shows that requirement-focused naming improves test coverage and maintainability. Tests become living documentation—someone unfamiliar with the code can read the test name and understand what the system should do.

**Recommendation:** Use declarative naming with "should" and "when." It naturally guides you toward testing requirements rather than implementation.

## Testing Patterns: Arrange-Act-Assert and Given-When-Then

The Arrange-Act-Assert (AAA) pattern is the fundamental structure:

```dart
test('NotesProvider should add note when createNote is called', () {
  // Arrange
  final provider = NotesProvider();
  final note = Note(title: 'Test', content: 'Content', folder: 'General', tags: []);
  
  // Act
  provider.createNote(note);
  
  // Assert
  expect(provider.notes.length, 1);
  expect(provider.notes.first.title, 'Test');
});
```

BDD extends this with Given-When-Then language that maps directly to AAA:

```dart
test('NotesProvider should contain note WHEN note is created', () {
  // Given: provider exists
  final provider = NotesProvider();
  final note = Note(title: 'Test', content: 'Content', folder: 'General', tags: []);
  
  // When: note is created
  provider.createNote(note);
  
  // Then: provider contains the note
  expect(provider.notes.length, 1);
});
```

Both patterns say the same thing. Use AAA for consistency with Dart conventions. Use Given-When-Then when communicating with non-technical stakeholders or when your test's logic is complex and benefits from explicit labeling.

## Mocking: Testing in Isolation

When your code depends on external services (APIs, databases, file systems), you can't test them directly—you need them to be available, predictable, and fast. Mocking solves this by creating fake versions of dependencies.

The `mockito` package is the standard mocking library for Dart:

```yaml
dev_dependencies:
  mockito: ^5.4.0
  build_runner: ^2.4.0
```

### Creating and Using Mocks

```dart
import 'package:mockito/mockito.dart';
import 'package:test/test.dart';

// Create a mock class
class MockApiClient extends Mock implements ApiClient {}

void main() {
  test('NotesProvider should fetch notes from API', () async {
    // Arrange: set up the mock
    final mockClient = MockApiClient();
    when(mockClient.fetchNotes()).thenAnswer((_) async => [
      Note(title: 'Note 1', content: 'Content', folder: 'General', tags: []),
    ]);
    
    final provider = NotesProvider(client: mockClient);
    
    // Act: fetch notes
    await provider.fetchNotes();
    
    // Assert: verify the notes were fetched
    expect(provider.notes.length, 1);
    verify(mockClient.fetchNotes()).called(1);
  });
}
```

Key methods:

- `when(mock.method()).thenAnswer(...)` — Define what the mock returns
- `verify(mock.method()).called(n)` — Verify a method was called `n` times
- `any()` — Match any argument

Mocking isolates your code from external dependencies, making tests fast and reliable.

## Test Organization with Groups

As your test suite grows, organize tests into logical groups:

```dart
void main() {
  group('NotesProvider', () {
    group('addNote', () {
      test('should add note to list when called', () { ... });
      test('should call notifyListeners when note is added', () { ... });
      test('should throw exception if note title is empty', () { ... });
    });
    
    group('deleteNote', () {
      test('should remove note from list', () { ... });
      test('should not error if note does not exist', () { ... });
    });
  });
}
```

Groups make test output readable and help organize related tests together. You can run tests by group: `flutter test --name="addNote"`.

## Writing Testable Code

Not all code is equally testable. Some patterns make testing harder:

**Tight coupling:** Code that creates its own dependencies (e.g., `ApiClient client = ApiClient()`) is hard to mock.

```dart
// Hard to test - creates its own client
class NotesProvider {
  final client = ApiClient();
  
  Future<void> fetchNotes() async {
    // Must use real ApiClient
  }
}

// Easy to test - accepts client as dependency
class NotesProvider {
  final ApiClient client;
  
  NotesProvider(this.client);
  
  Future<void> fetchNotes() async {
    // Can inject mock ApiClient
  }
}
```

**Side effects in constructors:** Code that performs I/O or state changes in `__init__` or constructors is hard to test.

**Mixed concerns:** A method that calculates, fetches, and displays is hard to test. Separate concerns into smaller methods.

Good testable code has clear inputs and outputs, dependencies injected, and a single responsibility per function or class. This is exactly what good architecture provides.

## Test-Driven Development in Practice

TDD has a rhythm: Red → Green → Refactor.

1. **Red:** Write a test for code that doesn't exist yet. The test fails.
2. **Green:** Write the minimal code to make the test pass.
3. **Refactor:** Improve the code without changing behavior. Tests still pass.

This might seem backwards—how do you test code before it exists? But it's powerful:

```dart
// Red: write the test first
test('Counter should increment from 0 to 1', () {
  final counter = Counter();
  counter.increment();
  expect(counter.value, 1);
});

// This test fails because Counter doesn't exist or doesn't work
// Green: write minimal code to pass
class Counter {
  int value = 0;
  void increment() => value++;
}

// Now the test passes
// Refactor: improve without breaking tests
class Counter {
  int _value = 0;
  int get value => _value;
  void increment() => _value++;
}
```

TDD naturally guides you toward clean, testable code because you're thinking about how to test it from the start. It also prevents over-engineering—you only write code needed to pass tests.

## Beyond Unit Tests: BDD for Behavior

When unit tests alone aren't enough to verify behavior, BDD approaches bridge the gap. Instead of testing implementation, BDD tests scenarios in natural language:

```gherkin
Feature: Create Notes
  Scenario: User creates a new note
    Given I am on the notes list screen
    When I tap the create button
    And I enter a title "My Note"
    And I enter content "This is a test"
    And I tap save
    Then I should see "My Note" in the list
```

Tools like `flutter_gherkin` parse these scenarios and generate widget tests. BDD forces you to think about user behavior rather than code mechanics.

BDD is powerful for complex workflows and communication with non-technical stakeholders. For most unit testing, declarative test naming (with "should" and "when") brings many BDD benefits without the extra tooling.

## Best Practices

1. **Test one thing per test.** A test with multiple assertions is testing multiple behaviors. If it fails, you don't know which behavior broke.

2. **Keep tests independent.** Tests shouldn't depend on each other. You should be able to run any test in any order.

3. **Use descriptive names.** Your test names are documentation. Someone reading them should understand what the code should do.

4. **Avoid testing implementation details.** Test behavior. If you're verifying that a specific method was called, you're testing implementation, not behavior.

5. **Mock external dependencies.** Your tests should run fast and not depend on external services. Mock APIs, databases, and file systems.

6. **Maintain your tests.** Tests are code. Refactor them when you refactor production code. Update tests when behavior changes.

---

## Hands-On Application

Testing is best learned by doing. As you build the Markdown Notes app in the project sections, apply these principles:

- Write a test for each piece of logic (providers, models, utilities)
- Use mocking for any external dependencies
- Use declarative test names with "should" and "when"
- Organize tests into logical groups
- Aim for high coverage of critical logic

Start with unit tests of your providers. Then add widget tests of your screens. Finally, add a few integration tests of complete workflows.

Testing is a skill. You'll get faster at it with practice, and the confidence that comes from a well-tested codebase is worth the investment.
