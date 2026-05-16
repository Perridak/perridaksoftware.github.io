# Best Practices

Building a Flutter app that works is one thing. Building one that scales, remains maintainable, and doesn't degrade over time requires discipline about best practices. This chapter identifies the patterns and anti-patterns that separate production-quality apps from prototypes.

Throughout this tutorial, we've covered practices in context—using `const` constructors, separating concerns with state management, centralizing routing. This chapter distils the most critical practices and highlights the pain points that cause real-world projects to struggle.

## Test-Driven Development: The Foundation

Before diving into specific patterns, we need to address the practice that underpins everything else: testing.

Many developers approach testing as an afterthought—something to do after the code is written, if there's time. Research consistently shows this is backwards. Test-Driven Development (TDD), where tests are written before implementation, reduces the number of defects introduced during development and leads to more maintainable code. Empirical studies show that TDD can reduce defects and lead to more maintainable code, with mature programmers who have used both test-first and test-last approaches preferring test-first.

The mechanism is straightforward: when you write tests first, you clarify what you're building before you build it. The test becomes your specification. You can't write good tests for poorly designed code, so writing tests first naturally pushes you toward better design. More importantly, TDD results show significant improvements in code coverage and maintainability for TDD groups, with the approach offering a consistent framework across controlled and naturalistic studies.

The payoff compounds. Early defect detection is cheaper than late detection. Refactoring with tests is safe—if your tests still pass, you haven't broken anything. Maintenance is easier because tests document how code should behave.

This doesn't mean writing tests for everything or achieving 100% coverage. It means starting with tests for critical logic, building the habit, and gradually expanding. If you're not practicing TDD now, make it your next learning goal. The Testing chapter (Chapter 7) covers practical approaches.

## The Pain Points: What Actually Breaks Projects

Research into real-world Flutter and Dart projects reveals consistent failure patterns. These aren't advanced edge cases—they're foundational mistakes that happen repeatedly because they're easy to make.

### Memory Leaks and Resource Disposal

This is the most frequent issue seen in many projects: some classes in Flutter allocate resources that Dart's garbage collector doesn't automatically clean up, including AnimationController, TextEditingController, ScrollController, FocusNode, and StreamSubscription.

**Symptom**

Your app gets laggy over time. Users navigate between screens dozens of times and notice performance degradation. Memory use climbs. Eventually, the app crashes.

**Cause**

You forgot to dispose of a controller or subscription. In `initState()` you created it; in `dispose()` you should have cleaned it up. It's trivial but easy to miss, especially when you have several resources.

**Fix**

Adopt a checklist. Every `initState()` needs a matching `dispose()`. Static analysis tools can catch this. Make it habit: allocate in `initState()`, dispose in `dispose()`.

### setState() Misuse

Calling setState() unnecessarily or outside the widget lifecycle is a common mistake that leads to poor performance issues, unnecessary widget rebuilds, or runtime errors. Placing logic-heavy code or API calls inside the build() method is incorrect—the build() method should be pure and light, with logic delegated to initState() or separate controllers.

**Symptom**

Your UI rebuilds constantly. Network requests happen every frame. The app feels janky or unresponsive.

**Cause**

You're putting side effects in `build()` or calling `setState()` too often or in the wrong place.

**Fix**

Keep `build()` pure. It should only construct UI from current state, never cause side effects. Move API calls to `initState()`. For app-wide state, use your state manager (Provider). For local state that updates frequently, consider `ChangeNotifier` or `ValueNotifier` to decouple state changes from rebuilds.

### Poor Architecture: Code in main.dart

Dumping all code into main.dart makes the app impossible to scale and maintain. The solution is to adopt MVC, MVVM, or Clean Architecture—separating UI, business logic, and services.

**Symptom**

As your app grows, main.dart becomes thousands of lines. Adding a new feature requires editing five files you didn't expect to touch. Tests become impossible to write.

**Cause**

No architecture decision early. Code grows organically without structure.

**Fix**

Adopt a structure from the start. This tutorial's architecture (models, providers, screens, widgets) is a good baseline. As your app grows, refine it. Some teams use MVVM or Clean Architecture. The key is consistency: every feature follows the same structure.

### Unhandled Errors and Poor Error Handling

A common mistake is using just print(e) instead of proper error handling, which causes apps to silently crash in production. The solution is using try-catch blocks, adding FlutterError.onError and PlatformDispatcher.instance.onError, and integrating Firebase Crashlytics for real-time crash reporting.

**Symptom**

Users report that features don't work, but you have no logs. API calls fail silently. Forms disappear without explanation.

**Cause**

You catch exceptions but don't log them or show the user. Production builds have no visibility into errors.

**Fix**

Set up error handling globally. Add `FlutterError.onError` in your `main()` to catch Flutter framework errors. Use `PlatformDispatcher.instance.onError` for Dart errors. For production, integrate crash reporting (Firebase Crashlytics is standard). Always show users something when things break—a message, a retry button, guidance on next steps.

### Responsive Design Oversights

Only testing on your own phone or a single emulator causes UI to break on other devices. The solution is testing on different screen sizes and orientations, using both Android and iOS emulators, and leveraging MediaQuery and LayoutBuilder for responsive UIs.

**Symptom**

Your app looks beautiful on your phone but is unreadable on tablets. Text overflows. Buttons are too small. Landscape mode is broken.

**Cause**

Hardcoded values. You built for one screen size and didn't test others.

**Fix**

Use `MediaQuery` to check screen dimensions. Use `LayoutBuilder` for responsive layouts. Test on multiple devices from the start—it's easier to build right than to fix later. The Flutter DevTools include device emulation.

### Dependency Management

Installing a package for every little feature bloats apps with outdated dependencies and maintenance issues. The solution is preferring core Flutter features first and checking a package's maintenance status, GitHub activity, and last update before adding it.

**Symptom**

Your `pubspec.yaml` has 50 dependencies. A critical security issue in an obscure package affects you. Upgrading one package breaks three others.

**Cause**

Every problem looks like a nail when you have a package manager. You add a package for toast notifications, another for HTTP, another for logging—when Flutter core or simpler solutions exist.

**Fix**

Ask "does Flutter already do this?" before reaching for a package. Evaluate packages by maintenance, GitHub activity, and community use. Prefer packages with clear ownership and regular updates. Keep dependencies minimal.

## Practices We've Already Covered

Throughout this tutorial, we've introduced practices in their appropriate context. These remain foundational:

**Use `const` constructors** when possible. This prevents unnecessary rebuilds and is one of the highest-impact optimizations available.

**Break large widgets into smaller ones.** If your `build()` method exceeds 50 lines, extract sections into separate widget classes. This improves readability and testability.

**Prefer immutability.** When updating state, create new objects instead of mutating existing ones. This makes state changes explicit and prevents subtle bugs.

**Centralize navigation.** Define all routes in one place. This makes your app's structure visible and enables features like deep linking.

**Separate routing from data.** Routes move users between screens. Providers manage data. Don't conflate them.

**Validate early and often.** Validate user input before performing operations. Prevent bad data from entering your system.

**Handle null explicitly.** Dart's null safety is powerful but requires thought. Use `?` and `??` intentionally. Avoid silently treating null as "no error."

## The Meta-Practice: Code Review

The common thread through all these practices is that they're easy to miss alone but hard to miss in code review. Most common mistakes can be detected with static analysis tools such as DCM (Dart Code Metrics).

Whether you're a solo developer or on a team, treat code review as non-negotiable. If you're building alone, reviewing your own code after a day or two provides fresh eyes. If you're on a team, review each other's code. Code review catches mistakes early, spreads knowledge, and enforces standards.

Use linting tools. Configure your `analysis_options.yaml` to enforce rules. Let the tools catch the easy stuff so humans can focus on logic and design.

## Continuous Growth

These practices aren't rules carved in stone. They're patterns that work in the real world. As you build more apps, you'll discover what works for your team and your domain. The key is being deliberate: make conscious choices about architecture, testing, and standards rather than letting code grow organically.

Software engineering is young compared to other disciplines. We're still learning what works. TDD is more established now than it was ten years ago because evidence accumulated. The practices in this chapter reflect current knowledge, but stay curious. Read about others' experiences. Experiment. Share what you learn.

---

## Next Steps

You now have the core knowledge to build real Flutter apps. The remaining chapters cover specialized topics—testing techniques, advanced widgets, persistence, and external data sources. But everything you need for production-quality apps is here.

Start small. Build an app using these practices. You'll discover which ones matter most to you. Then keep learning.
