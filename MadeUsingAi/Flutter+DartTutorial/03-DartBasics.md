# Dart Basics

Dart is a statically-typed, object-oriented language designed for building fast, multi-platform applications. It combines the best parts of languages you likely know—type safety, functional programming, and a pragmatic syntax that feels familiar if you've worked with other modern languages.

This chapter covers everything an experienced developer needs to confidently write Dart code, from variables and functions to advanced features like mixins and extension methods. We'll highlight where Dart differs from other languages you may be more at home with, and flag gotchas that can trip up developers coming from other backgrounds.

## Variables, Types, and Null Safety

### Declaring Variables

Dart offers several ways to declare variables, each with different semantics:

```dart
void main() {
  // Dynamic typing with type inference
  var name = 'Alice';           // Inferred as String
  var count = 42;               // Inferred as int
  
  // Explicit typing
  String greeting = 'Hello';
  int age = 30;
  double salary = 50000.0;
  bool isActive = true;
  
  // Type-agnostic (dynamic)
  dynamic mystery = 'could be anything';
  mystery = 42;                 // No error—dynamic accepts any type
  
  print(name);
}
```

**The difference between `var`, explicit types, and `dynamic`:**

- **`var`**: Type is inferred at declaration and **fixed thereafter**. Once `var name = 'Alice'`, the variable is a `String` for its entire lifetime. This is the preferred approach when the type is obvious from context.
- **Explicit types** (`String`, `int`, etc.): Make intent clear. Recommended for function parameters and return types, and when type inference would be ambiguous.
- **`dynamic`**: Disables type checking. Any method can be called on it at runtime. Avoid this unless absolutely necessary—it defeats the purpose of Dart's type system.

**Watch out for:** If you're coming from JavaScript where `let` and `const` allow flexible reassignment, Dart's `var` locks the type at declaration. The variable itself can be reassigned to different values, but only of the same type. Trying `var x = 'hello'; x = 42;` will fail at compile time. In Kotlin, this is similar—`var` infers and locks the type, though Kotlin's type system is slightly more flexible with supertypes.

### Null Safety: Dart's Defining Feature

Dart enforces **sound null safety** by default. A variable cannot be `null` unless you explicitly say it can be:

```dart
void main() {
  String name = 'Alice';        // Non-nullable—must always have a String value
  String? nickname = null;      // Nullable—can be null or a String
  
  // This compiles:
  nickname = 'Ali';
  nickname = null;
  
  // This causes a compile error:
  // String wrong = null;       // ERROR: null cannot be assigned to non-nullable String
}
```

When you have a nullable variable, you must check for null before using it:

```dart
void main() {
  String? nickname = getUserNickname();
  
  // This won't compile—nickname might be null:
  // print(nickname.length);    // ERROR
  
  // Option 1: Null check
  if (nickname != null) {
    print(nickname.length);     // Safe—type system knows it's not null here
  }
  
  // Option 2: Null-coalescing operator
  print(nickname?.length);      // Evaluates to null if nickname is null
  
  // Option 3: Null-coalescing assignment
  print(nickname ?? 'Anonymous');  // Use 'Anonymous' if nickname is null
}

String? getUserNickname() => null;
```

**Be aware of:** This is a major departure from many other languages. In JavaScript, `null` and `undefined` are constantly lurking, requiring runtime checks. Dart makes null safety a **compile-time guarantee**—the type system prevents entire classes of bugs before your code runs. C# has nullable reference types (similar syntax with `?`), but those are optional and came much later. Dart has had sound null safety since 2021 and it's mandatory, by design.

### Collections

Dart provides three main collection types:

```dart
void main() {
  // Lists (ordered, mutable)
  List<String> names = ['Alice', 'Bob', 'Charlie'];
  List<int> numbers = [1, 2, 3];
  var mixed = [1, 'two', 3.0];  // Inferred as List<Object>
  
  // Maps (key-value pairs)
  Map<String, int> ages = {
    'Alice': 30,
    'Bob': 25,
  };
  var person = {'name': 'Alice', 'age': 30};  // Inferred as Map<String, Object>
  
  // Sets (unordered, unique)
  Set<String> uniqueNames = {'Alice', 'Bob', 'Alice'};  // Duplicate removed
  var numbers = {1, 2, 3};  // Inferred as Set<int>
  
  print(names[0]);           // 'Alice'
  print(ages['Alice']);      // 30
  print(uniqueNames);        // {Alice, Bob}
}
```

**Type parameters matter:** Lists and Maps are generic. `List<String>` is a list of strings; `List<dynamic>` is a list of anything. Be explicit about what you're storing.

**Be aware of:** Set literal syntax `{1, 2, 3}` looks identical to a map literal `{'a': 1}`. Dart infers the type based on context. If you want a set and Dart infers a map (or vice versa), explicitly annotate: `Set<int> numbers = {1, 2, 3};`.

### Immutability with `final` and `const`

```dart
void main() {
  // final: immutable after initialization
  final String name = 'Alice';
  // name = 'Bob';               // ERROR: cannot be reassigned
  
  // const: compile-time constant, implicitly final
  const int maxAttempts = 3;
  // maxAttempts = 5;            // ERROR
  
  // final without type (type is inferred)
  final count = 42;
  
  // const collections are deeply immutable
  const List<int> numbers = [1, 2, 3];
  // numbers[0] = 10;            // ERROR: cannot modify const list
  
  // final collections can be modified
  final List<int> mutable = [1, 2, 3];
  mutable[0] = 10;              // OK
  mutable.add(4);               // OK
}
```

**The distinction:**
- **`final`**: Runtime constant. Once assigned, cannot be reassigned. The variable itself is immutable, but if it holds a list or object, those contents can change.
- **`const`**: Compile-time constant. Deeply immutable. If you reassign a const to a different const, Dart might even reuse the same object in memory.

**Pro tip:** If you come from other languages where `const` is used liberally, recalibrate your thinking. Dart's `const` is stricter—it requires a compile-time constant value. If you're constructing an object at runtime (even with known values), use `final`, not `const`. This distinction prevents bugs where you accidentally try to modify something you thought was mutable.

## Functions

### Declaring and Calling Functions

```dart
// Explicit return type and parameters
int add(int a, int b) {
  return a + b;
}

// Arrow syntax (=> for single-expression functions)
int multiply(int a, int b) => a * b;

// No return type (defaults to dynamic)
sum(int a, int b) => a + b;         // Avoid this—always specify return type

// Named parameters (in braces)
String greet({String name = 'Guest'}) {
  return 'Hello, $name!';
}

// Required named parameters (Dart 2.12+)
String greetRequired({required String name}) {
  return 'Hello, $name!';
}

// Positional parameters with defaults
void retry(Function callback, [int maxAttempts = 3]) {
  for (int i = 0; i < maxAttempts; i++) {
    try {
      callback();
      return;
    } catch (e) {
      if (i == maxAttempts - 1) rethrow;
    }
  }
}

void main() {
  print(add(5, 3));                    // 8
  print(multiply(5, 3));               // 15
  print(greet(name: 'Alice'));         // Hello, Alice!
  print(greetRequired(name: 'Bob'));   // Hello, Bob!
  retry(() => print('Attempting...'));
}
```

**Named vs. positional parameters:**
- **Positional** (`int a, int b`): Called in order. Optional positional parameters go in square brackets `[int maxAttempts = 3]`.
- **Named** (`{String name = 'Guest'}`): Called by name (`name: 'Alice'`). More readable for functions with many parameters. Use `required` to make a named parameter mandatory.

**Be aware of:** Unlike some other languages you may be more at home with, Dart doesn't allow arbitrary numbers of variadic arguments (no `...args` parameter style). If you need flexible argument counts, use a list parameter instead: `void log(String message, List<Object> args)`.

### First-Class Functions and Closures

Functions are objects. You can pass them around, store them, and return them:

```dart
// Function type annotation
void Function(String) logger = (String msg) {
  print('[LOG] $msg');
};

// Typedef for readability
typedef Callback = void Function(String);

Callback createLogger(String prefix) {
  return (String msg) {
    print('[$prefix] $msg');
  };
}

void main() {
  logger('Hello');                    // [LOG] Hello
  
  Callback appLogger = createLogger('APP');
  appLogger('Starting');              // [APP] Starting
  
  // Higher-order functions
  List<int> numbers = [1, 2, 3];
  var doubled = numbers.map((x) => x * 2);  // [2, 4, 6]
}
```

Closures capture variables from their enclosing scope:

```dart
void main() {
  int multiplier = 2;
  
  Function multiply = (int x) => x * multiplier;
  
  print(multiply(5));                 // 10
  
  multiplier = 3;
  print(multiply(5));                 // 15 (closure sees the updated value)
}
```

**Pro tip:** Closures in Dart work similarly to other languages you may be more at home with, but Dart's type system is stricter. Always annotate function types when storing functions in variables—don't rely on inference. This makes your code more maintainable and catches type errors earlier.

## Object-Oriented Programming

### Classes and Constructors

```dart
class Person {
  String name;
  int age;
  
  // Standard constructor
  Person(String name, int age) {
    this.name = name;
    this.age = age;
  }
  
  // Syntactic sugar for above
  Person.shorthand(this.name, this.age);
  
  // Named constructor
  Person.newborn(this.name) : age = 0;
  
  // Factory constructor (for custom creation logic)
  factory Person.fromString(String data) {
    final parts = data.split(',');
    return Person(parts[0], int.parse(parts[1]));
  }
  
  String greet() => 'Hello, I am $name';
}

void main() {
  var person1 = Person('Alice', 30);
  var person2 = Person.shorthand('Bob', 25);
  var person3 = Person.newborn('Charlie');
  var person4 = Person.fromString('Diana,28');
}
```

**Constructor patterns:**
- **Standard**: Explicit `this` assignment.
- **Shorthand**: `Person(this.name, this.age)` automatically assigns parameters to fields.
- **Named constructors**: `Person.newborn()` for special creation logic.
- **Factory constructors**: Return instances with custom logic, possibly returning cached or subclass instances.

**Gotcha:** Dart requires you to initialize all non-nullable fields. If a field has no default and isn't initialized in the constructor, you'll get a compile error. Use nullable types (`String?`) or `late` for fields initialized later.

### Inheritance and Polymorphism

```dart
class Animal {
  String name;
  
  Animal(this.name);
  
  void speak() {
    print('$name makes a sound');
  }
}

class Dog extends Animal {
  @override
  void speak() {
    print('$name barks');
  }
}

void main() {
  Animal animal = Dog('Rex');
  animal.speak();                     // Rex barks
}
```

**Be aware of:** Unlike C# where `override` is required, Dart doesn't mandate the `@override` annotation—it's optional. However, using it is best practice because it makes your intent explicit and helps catch typos in method names at compile time.

### Abstract Classes and Interfaces

Dart doesn't have a separate `interface` keyword. Any class can be used as an interface:

```dart
abstract class Animal {
  String name;
  
  Animal(this.name);
  
  void speak();                       // Abstract method (no body)
  
  void move() {
    print('$name moves');            // Concrete method
  }
}

class Dog implements Animal {
  @override
  String name;
  
  Dog(this.name);
  
  @override
  void speak() => print('$name barks');
}

void main() {
  // Animal animal = Animal('Generic');  // ERROR: cannot instantiate abstract class
  Dog dog = Dog('Rex');
  dog.speak();
}
```

**Watch out for:** When using `implements`, you must implement all abstract members, even if the abstract class provides default implementations. If you want to inherit some behaviour, use `extends` instead. This distinction matters—`implements` says "you're a type of this", while `extends` says "you are this, with some changes".

### Mixins: Composition Over Multiple Inheritance

Dart doesn't support multiple inheritance, but mixins allow you to reuse code across unrelated classes:

```dart
mixin Swimmer {
  void swim() => print('Swimming');
}

mixin Flyer {
  void fly() => print('Flying');
}

class Bird with Flyer {
  String name;
  Bird(this.name);
}

class Duck with Swimmer, Flyer {
  String name;
  Duck(this.name);
}

void main() {
  var duck = Duck('Donald');
  duck.swim();                        // Swimming
  duck.fly();                         // Flying
}
```

**When to use mixins:**
- Share methods across unrelated classes.
- Avoid the "diamond problem" of multiple inheritance.
- Keep concerns separate (e.g., "things that can swim" as a mixin).

**Be aware of:** Mixins are applied left-to-right with `with`. If two mixins define the same method, the rightmost wins. Order matters, and this can be a source of subtle bugs if you're not careful about mixin composition.

## Advanced Type System

### Generics

Generics allow you to write reusable code that works with different types:

```dart
class Box<T> {
  T? content;
  
  void put(T item) {
    content = item;
  }
  
  T? get() {
    return content;
  }
}

// Generic functions
T first<T>(List<T> items) {
  return items[0];
}

void main() {
  var stringBox = Box<String>();
  stringBox.put('Hello');
  print(stringBox.get());             // Hello
  
  var intBox = Box<int>();
  intBox.put(42);
  print(intBox.get());                // 42
  
  print(first([1, 2, 3]));            // 1
  print(first(['a', 'b', 'c']));      // a
}
```

Type parameters can have bounds:

```dart
class Repository<T extends Object> {
  // T must extend Object (or implement an interface)
}
```

**Watch out for:** Dart uses type erasure—at runtime, `List<String>` and `List<int>` are the same object. You cannot do runtime type checks like `if (items is List<String>)`. You can check `if (items is List)`, but not the type parameter. This is common across compiled languages, but can surprise developers coming from runtime-typed languages.

### Extension Methods

Extension methods let you add methods to existing classes without subclassing:

```dart
extension StringExtensions on String {
  String capitalize() {
    return '${this[0].toUpperCase()}${substring(1)}';
  }
  
  bool isValidEmail() {
    return contains('@');
  }
}

extension ListExtensions<T> on List<T> {
  T? firstOrNull() {
    return isEmpty ? null : first;
  }
}

void main() {
  print('hello'.capitalize());        // Hello
  print('test@example.com'.isValidEmail());  // true
  
  print([1, 2, 3].firstOrNull());     // 1
  print(<int>[].firstOrNull());       // null
}
```

**Be aware of:** Extension methods are resolved statically. If you assign a String to a `dynamic` variable, calling the extension method won't work. The type system must know it's a String at compile time to find the extension. This is by design—it keeps the system predictable.

## Asynchronous Programming

### Futures and Async/Await

A `Future` represents a value (or error) that will be available at some point in the future:

```dart
// Simulating an async operation
Future<String> fetchUserName(int userId) async {
  // In real code, this would fetch from an API
  await Future.delayed(Duration(seconds: 1));
  return 'User #$userId';
}

void main() async {
  // Option 1: Using await
  String name = await fetchUserName(1);
  print(name);
  
  // Option 2: Using .then() callback
  fetchUserName(2).then((name) {
    print(name);
  });
  
  // Option 3: Chain multiple async operations
  var name = await fetchUserName(3);
  var details = await fetchUserDetails(name);
  print(details);
}

Future<String> fetchUserDetails(String name) async {
  await Future.delayed(Duration(milliseconds: 500));
  return 'Details for $name';
}
```

**`async` and `await`:**
- **`async`**: Marks a function as asynchronous. It automatically wraps the return value in a `Future`.
- **`await`**: Pauses execution until a `Future` completes, then returns its value.

**Pro tip:** You can only use `await` inside an `async` function. If you want to use `await` in `main()`, `main()` must be declared `async`. This is different from some other languages where the entire runtime context is async—in Dart, async is opt-in per function.

### Handling Errors

```dart
Future<int> divide(int a, int b) async {
  if (b == 0) {
    throw ArgumentError('Divisor cannot be zero');
  }
  return a ~/ b;  // Integer division
}

void main() async {
  // Try/catch with async
  try {
    int result = await divide(10, 2);
    print(result);                    // 5
  } catch (e) {
    print('Error: $e');
  }
  
  // .catchError() for Futures
  divide(10, 0).catchError((e) {
    print('Caught: $e');
  });
}
```

### Streams

A `Stream` is like a `Future`, but it can emit multiple values over time:

```dart
Stream<int> countUp(int n) async* {
  for (int i = 1; i <= n; i++) {
    await Future.delayed(Duration(milliseconds: 100));
    yield i;
  }
}

void main() async {
  // Listen to a stream
  await for (int count in countUp(5)) {
    print(count);                     // 1, 2, 3, 4, 5
  }
  
  // Or use .listen()
  countUp(3).listen((count) {
    print('Count: $count');
  });
}
```

**Be aware of:** Streams are lazy—nothing happens until you listen. If you don't call `.listen()` or use `await for`, the stream never executes. This can be confusing if you create a stream and expect it to run automatically. Always explicitly listen to activate a stream.

## String Interpolation and Formatting

```dart
void main() {
  String name = 'Alice';
  int age = 30;
  
  // String interpolation with $
  print('Name: $name, Age: $age');
  
  // Expressions in interpolation
  print('In 5 years: ${age + 5}');
  
  // Method calls
  print('Upper: ${name.toUpperCase()}');
  
  // Multi-line strings
  String multiline = '''
    Line 1
    Line 2
    Line 3
  ''';
  print(multiline);
  
  // Raw strings (no interpolation)
  print(r'This is $name');             // Prints: This is $name
}
```

## Exception Handling

```dart
void main() {
  try {
    int result = 10 ~/ 0;             // Integer division by zero
  } on IntegerDivisionByZeroException {
    print('Cannot divide by zero');
  } on FormatException {
    print('Invalid format');
  } catch (e) {
    print('Unknown error: $e');
  } finally {
    print('Cleanup');
  }
}
```

**Dart exceptions:**
- Throw any object (though `Exception` is conventional).
- Catch specific exception types with `on`.
- Use generic `catch` for anything.

## Control Flow

```dart
void main() {
  int x = 5;
  
  // If/else as expression
  String result = x > 0 ? 'positive' : 'non-positive';
  
  // For loops
  for (int i = 0; i < 3; i++) {
    print(i);
  }
  
  // For-in (like for...of in JavaScript)
  List<String> names = ['Alice', 'Bob'];
  for (String name in names) {
    print(name);
  }
  
  // While and do-while
  int count = 0;
  while (count < 3) {
    print(count++);
  }
  
  // Switch
  switch (x) {
    case 1:
    case 2:
      print('One or two');
      break;
    case 5:
      print('Five');
      break;
    default:
      print('Other');
  }
}
```

## Operators and Special Syntax

```dart
void main() {
  // Null-coalescing operator
  String? nickname = null;
  print(nickname ?? 'Anonymous');     // Anonymous
  
  // Null-aware operators
  String? text = 'hello';
  print(text?.length);                // 5 (or null if text is null)
  print(text?.toUpperCase());         // HELLO
  
  // Cascade operator (..): call multiple methods on same object
  var buffer = StringBuffer();
  buffer
    ..write('Hello')
    ..write(' ')
    ..write('World');
  print(buffer.toString());           // Hello World
  
  // Spread operator (...)
  List<int> numbers1 = [1, 2, 3];
  List<int> numbers2 = [0, ...numbers1, 4];  // [0, 1, 2, 3, 4]
}
```

**Cascade operator (`..)` is unique to Dart** and very useful for configuring objects:

```dart
class TextStyle {
  String? fontFamily;
  int? fontSize;
  bool? bold;
}

void main() {
  var style = TextStyle()
    ..fontFamily = 'Arial'
    ..fontSize = 16
    ..bold = true;
}
```

## Enums

```dart
enum Status {
  pending,
  active,
  completed,
}

void main() {
  Status status = Status.active;
  
  switch (status) {
    case Status.pending:
      print('Waiting...');
      break;
    case Status.active:
      print('Running...');
      break;
    case Status.completed:
      print('Done!');
      break;
  }
}
```

Dart 2.17+ supports enhanced enums with properties and methods:

```dart
enum Status {
  pending('Waiting'),
  active('Running'),
  completed('Done');
  
  final String label;
  
  const Status(this.label);
}

void main() {
  print(Status.active.label);         // Running
}
```

## Key Takeaways

1. **Type safety by default**: Dart forces you to think about types upfront, preventing whole categories of runtime errors.
2. **Null safety is built-in**: Use `?` to allow nulls; otherwise, nulls are compile-time errors.
3. **Pragmatic syntax**: Dart's syntax is designed for developer productivity without sacrificing safety.
4. **Functional programming**: First-class functions, closures, and functional methods on collections are first-class citizens.
5. **Async-first**: Futures and async/await are integrated into the language, not afterthoughts.
6. **Mixins over multiple inheritance**: Dart's answer to code reuse without the complexity of multiple inheritance.

This foundation prepares you to write Dart code confidently for both command-line apps and Flutter.

---

## Hands-On Project

Ready to apply what you've learned? Work through the [Markdown Notes Project Part A](markdown-notes-project-part-a.html) to build a complete command-line note-taking application. You'll reinforce these concepts through 60 minutes of practical coding that demonstrates classes, collections, null safety, and file I/O in a real-world context.
