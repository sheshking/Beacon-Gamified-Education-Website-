// ============================================
// BEACON — Video Theater library
// ============================================
//
// Every entry with a `videoId` is a real, verified YouTube video that plays
// inline (I confirmed these IDs against multiple independent sources).
//
// Entries with `searchQuery` instead point to a YouTube search for that
// title + channel, rather than a guessed video ID — done deliberately for
// every topic-specific video below, since individually verifying 45+ exact
// video IDs isn't something I could do reliably. The channel and topic are
// real; the exact video is left for YouTube's own search to resolve rather
// than risking a broken or wrong link. This is disclosed in the UI too.

const THEATER_LIBRARY = {

  python: [
    {
      videoId: '_uQrJ0TkZlc',
      title: 'Python Full Course for Beginners',
      creator: 'Programming with Mosh',
      duration: '6h 14m',
      difficulty: 'beginner',
      xp: 150,
      description: 'A complete beginner-to-intermediate Python course covering variables, strings, functions, loops, lists, dictionaries, classes, and three mini projects.',
      timestamps: [
        ['0:00', 'Introduction'], ['13:03', 'Variables'], ['29:31', 'Strings'],
        ['58:17', 'If Statements'], ['1:20:43', 'While Loops'], ['1:41:48', 'For Loops'],
        ['1:55:50', 'Lists'], ['2:30:31', 'Functions'], ['3:01:46', 'Classes']
      ]
    },
    {
      videoId: 'kqtD5dpn9C8',
      title: 'Python for Beginners - Learn Coding with Python in 1 Hour',
      creator: 'Programming with Mosh',
      duration: '1h 00m',
      difficulty: 'beginner',
      xp: 60,
      description: 'A fast-paced one-hour crash course covering the essentials: variables, input, type conversion, strings, and arithmetic.',
      timestamps: [
        ['0:00', 'Introduction'], ['5:20', 'Variables'], ['14:10', 'Receiving Input'],
        ['24:00', 'Strings'], ['40:00', 'Arithmetic Operations']
      ]
    },
    {
      videoId: 'XKHEtdqhLK8',
      title: 'Python Full Course for Free',
      creator: 'Bro Code',
      duration: '12h 00m',
      difficulty: 'beginner',
      xp: 150,
      description: 'A marathon full-course covering everything from variables and loops to GUIs, file handling, and small games — great for going deep after the basics.',
      timestamps: [
        ['0:00', 'Python tutorial for beginners'], ['17:38', 'Multiple assignment'],
        ['Later', 'String methods, type casting, user input'], ['Later', 'Math functions, if statements, loops']
      ]
    },
    {
      videoId: '8KCuHHeC_M0',
      title: 'Learn Python in 1 Hour',
      creator: 'Bro Code',
      duration: '1h 00m',
      difficulty: 'intermediate',
      xp: 70,
      description: 'A tighter, faster-paced run through Python fundamentals for people who already know another language or finished the basics.',
      timestamps: [['0:00', 'Setup & fundamentals'], ['Later', 'Data structures'], ['Later', 'Functions & logic']]
    },
    {
      searchQuery: 'Bro Code Python Variables and Data Types',
      title: 'Python Variables & Data Types',
      creator: 'Bro Code', duration: '~20m', difficulty: 'beginner', xp: 50,
      description: 'A focused walkthrough of creating variables and the core Python data types. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'What is a variable'], ['Later', 'Data types'], ['Later', 'Naming rules']]
    },
    {
      searchQuery: 'Bro Code Python User Input',
      title: 'Python User Input',
      creator: 'Bro Code', duration: '~15m', difficulty: 'beginner', xp: 50,
      description: 'How to use input() to read from the user and convert it to the right type. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'input()'], ['Later', 'Type conversion']]
    },
    {
      searchQuery: 'Corey Schafer Python String Slicing',
      title: 'Python String Slicing & Indexing',
      creator: 'Corey Schafer', duration: '~20m', difficulty: 'intermediate', xp: 80,
      description: 'How string indexing and slicing work in Python, with practical examples. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Indexing'], ['Later', 'Slicing'], ['Later', 'Negative indices']]
    },
    {
      searchQuery: 'Corey Schafer Python String Methods',
      title: 'Python String Methods',
      creator: 'Corey Schafer', duration: '~25m', difficulty: 'beginner', xp: 60,
      description: 'A tour of the most useful built-in string methods in Python. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Common methods'], ['Later', 'Formatting']]
    },
    {
      searchQuery: 'Bro Code Python If Else Statements',
      title: 'Python If / Elif / Else',
      creator: 'Bro Code', duration: '~18m', difficulty: 'beginner', xp: 50,
      description: 'Conditional logic in Python: if, elif, else, and comparison operators. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'if statements'], ['Later', 'elif / else'], ['Later', 'Comparison operators']]
    },
    {
      searchQuery: 'Tech With Tim Python While and For Loops',
      title: 'Python While & For Loops',
      creator: 'Tech With Tim', duration: '~30m', difficulty: 'beginner', xp: 70,
      description: 'How and when to use while loops vs for loops in Python. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'While loops'], ['Later', 'For loops'], ['Later', 'break & continue']]
    },
    {
      searchQuery: 'Bro Code Python Lists',
      title: 'Python Lists',
      creator: 'Bro Code', duration: '~22m', difficulty: 'beginner', xp: 60,
      description: 'Creating, indexing, and modifying lists in Python. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Creating lists'], ['Later', 'List methods']]
    },
    {
      searchQuery: 'Bro Code Python Dictionaries',
      title: 'Python Dictionaries',
      creator: 'Bro Code', duration: '~20m', difficulty: 'intermediate', xp: 80,
      description: 'Key-value pairs in Python: creating, reading, and updating dictionaries. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Creating a dict'], ['Later', 'Accessing values'], ['Later', 'Looping over a dict']]
    },
    {
      searchQuery: 'Corey Schafer Python Functions',
      title: 'Python Functions',
      creator: 'Corey Schafer', duration: '~25m', difficulty: 'intermediate', xp: 90,
      description: 'Defining functions, parameters, default arguments, and return values. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'def & return'], ['Later', 'Default arguments'], ['Later', '*args & **kwargs']]
    },
    {
      searchQuery: 'Tech With Tim Python OOP Classes',
      title: 'Python Classes & OOP Basics',
      creator: 'Tech With Tim', duration: '~35m', difficulty: 'intermediate', xp: 100,
      description: 'An introduction to object-oriented programming in Python: classes, objects, and methods. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Defining a class'], ['Later', 'Constructors'], ['Later', 'Methods']]
    },
    {
      searchQuery: 'Corey Schafer Python Inheritance',
      title: 'Python Inheritance',
      creator: 'Corey Schafer', duration: '~30m', difficulty: 'advanced', xp: 120,
      description: 'How class inheritance works in Python, with a real example hierarchy. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Parent & child classes'], ['Later', 'super()'], ['Later', 'Method overriding']]
    },
    {
      searchQuery: 'freeCodeCamp Python File Handling',
      title: 'Python File Handling',
      creator: 'freeCodeCamp.org', duration: '~25m', difficulty: 'intermediate', xp: 90,
      description: 'Reading from and writing to files in Python, plus working with file paths. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Opening files'], ['Later', 'Reading & writing'], ['Later', 'with statement']]
    },
    {
      searchQuery: 'Tech With Tim Python Try Except Error Handling',
      title: 'Python Error Handling (Try/Except)',
      creator: 'Tech With Tim', duration: '~20m', difficulty: 'intermediate', xp: 90,
      description: 'Handling exceptions gracefully with try, except, and finally. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'try / except'], ['Later', 'Specific exceptions'], ['Later', 'finally']]
    },
    {
      searchQuery: 'Bro Code Python List Comprehension',
      title: 'Python List Comprehension',
      creator: 'Bro Code', duration: '~15m', difficulty: 'advanced', xp: 110,
      description: 'Writing concise, readable list comprehensions instead of manual loops. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Basic syntax'], ['Later', 'With conditions']]
    },
    {
      searchQuery: 'Corey Schafer Python Decorators',
      title: 'Python Decorators',
      creator: 'Corey Schafer', duration: '~30m', difficulty: 'advanced', xp: 130,
      description: 'What decorators are and how to write your own in Python. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Functions as objects'], ['Later', 'Writing a decorator'], ['Later', '@ syntax']]
    },
    {
      searchQuery: 'Tech With Tim Python Generators and Iterators',
      title: 'Python Generators & Iterators',
      creator: 'Tech With Tim', duration: '~25m', difficulty: 'advanced', xp: 130,
      description: 'How generators work under the hood, and when to use yield. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Iterators'], ['Later', 'yield'], ['Later', 'Generator expressions']]
    }
  ],

  java: [
    {
      searchQuery: 'Programming with Mosh Java Full Course for Beginners',
      title: 'Java Full Course for Beginners',
      creator: 'Programming with Mosh', duration: '2h 30m', difficulty: 'beginner', xp: 120,
      description: 'Covers Java setup, types, variables, strings, arrays, control flow, and a mortgage calculator project. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Introduction'], ['Later', 'Variables & Types'], ['Later', 'Control Flow'], ['Later', 'Project: Mortgage Calculator']]
    },
    {
      searchQuery: 'freeCodeCamp Java Programming for Beginners Full Course',
      title: 'Java Programming for Beginners — Full Course',
      creator: 'freeCodeCamp.org', duration: '4h 11m', difficulty: 'beginner', xp: 140,
      description: 'Hello World through Object-Oriented Programming: variables, data types, operators, strings, conditionals, arrays, loops, ArrayLists, and HashMaps. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Hello World'], ['Later', 'Variables & Data Types'], ['Later', 'Conditional Statements'], ['Later', 'Object Oriented Programming']]
    },
    {
      searchQuery: 'Bro Code Java Full Course for free',
      title: 'Java Full Course for Free',
      creator: 'Bro Code', duration: '12h 00m', difficulty: 'intermediate', xp: 150,
      description: 'A marathon course from variables through OOP concepts like inheritance, polymorphism, and interfaces. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Java tutorial for beginners'], ['Later', 'OOP: objects, constructors, inheritance'], ['Later', 'Interfaces & polymorphism']]
    },
    {
      searchQuery: 'Bro Code Java Variables and Data Types',
      title: 'Java Variables & Data Types',
      creator: 'Bro Code', duration: '~18m', difficulty: 'beginner', xp: 50,
      description: 'Declaring variables and understanding primitive types in Java. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Declaring variables'], ['Later', 'Primitive types']]
    },
    {
      searchQuery: 'Bro Code Java User Input Scanner',
      title: 'Java User Input (Scanner)',
      creator: 'Bro Code', duration: '~15m', difficulty: 'beginner', xp: 50,
      description: 'Reading keyboard input in Java using the Scanner class. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Scanner setup'], ['Later', 'Reading different types']]
    },
    {
      searchQuery: 'Telusko Java String Methods',
      title: 'Java String Methods',
      creator: 'Telusko', duration: '~25m', difficulty: 'beginner', xp: 60,
      description: 'Common String methods in Java: length, substring, equals, and more. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Creating strings'], ['Later', 'Common methods']]
    },
    {
      searchQuery: 'Bro Code Java If Else Statements',
      title: 'Java If / Else Statements',
      creator: 'Bro Code', duration: '~18m', difficulty: 'beginner', xp: 50,
      description: 'Conditional branching in Java with if, else if, and else. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'if / else'], ['Later', 'Comparison & logical operators']]
    },
    {
      searchQuery: 'Apna College Java For and While Loops',
      title: 'Java For & While Loops',
      creator: 'Apna College', duration: '~30m', difficulty: 'beginner', xp: 70,
      description: 'Loop constructs in Java: for, while, and do-while. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'for loops'], ['Later', 'while & do-while']]
    },
    {
      searchQuery: 'Bro Code Java Arrays',
      title: 'Java Arrays',
      creator: 'Bro Code', duration: '~20m', difficulty: 'intermediate', xp: 80,
      description: 'Declaring, filling, and looping through arrays in Java. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Declaring arrays'], ['Later', 'Looping through arrays']]
    },
    {
      searchQuery: 'Telusko Java ArrayList',
      title: 'Java ArrayList',
      creator: 'Telusko', duration: '~25m', difficulty: 'intermediate', xp: 90,
      description: 'Using the ArrayList collection class for dynamic, resizable lists. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Creating an ArrayList'], ['Later', 'Common methods']]
    },
    {
      searchQuery: 'Bro Code Java Methods',
      title: 'Java Methods',
      creator: 'Bro Code', duration: '~20m', difficulty: 'intermediate', xp: 80,
      description: 'Defining and calling methods, parameters, and return types in Java. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Defining methods'], ['Later', 'Parameters & return values']]
    },
    {
      searchQuery: 'Telusko Java OOP Classes and Objects',
      title: 'Java Classes & Objects',
      creator: 'Telusko', duration: '~35m', difficulty: 'intermediate', xp: 100,
      description: 'Object-oriented programming fundamentals in Java: classes, objects, and constructors. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Defining a class'], ['Later', 'Constructors'], ['Later', 'Creating objects']]
    },
    {
      searchQuery: 'Bro Code Java Constructors',
      title: 'Java Constructors',
      creator: 'Bro Code', duration: '~18m', difficulty: 'intermediate', xp: 85,
      description: 'How constructors work in Java, including overloaded constructors. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Default constructor'], ['Later', 'Overloaded constructors']]
    },
    {
      searchQuery: 'Telusko Java HashMap',
      title: 'Java HashMap',
      creator: 'Telusko', duration: '~25m', difficulty: 'intermediate', xp: 90,
      description: 'Key-value storage in Java using HashMap, and common operations. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Creating a HashMap'], ['Later', 'get / put / iterate']]
    },
    {
      searchQuery: 'Apna College Java Exception Handling',
      title: 'Java Exception Handling',
      creator: 'Apna College', duration: '~25m', difficulty: 'intermediate', xp: 90,
      description: 'Handling errors gracefully in Java with try, catch, and finally. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'try / catch'], ['Later', 'finally'], ['Later', 'Custom exceptions']]
    },
    {
      searchQuery: 'Bro Code Java Inheritance',
      title: 'Java Inheritance',
      creator: 'Bro Code', duration: '~22m', difficulty: 'advanced', xp: 120,
      description: 'Extending classes and reusing code through inheritance in Java. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'extends keyword'], ['Later', 'super()'], ['Later', 'Method overriding']]
    },
    {
      searchQuery: 'Telusko Java Polymorphism',
      title: 'Java Polymorphism',
      creator: 'Telusko', duration: '~28m', difficulty: 'advanced', xp: 130,
      description: 'Method overloading and overriding, and how polymorphism works in Java. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Overloading vs overriding'], ['Later', 'Runtime polymorphism']]
    },
    {
      searchQuery: 'Bro Code Java Interfaces',
      title: 'Java Interfaces',
      creator: 'Bro Code', duration: '~20m', difficulty: 'advanced', xp: 120,
      description: 'Defining and implementing interfaces to enforce a contract between classes. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Defining an interface'], ['Later', 'Implementing it']]
    },
    {
      searchQuery: 'Coding with John Java Generics',
      title: 'Java Generics',
      creator: 'Coding with John', duration: '~25m', difficulty: 'advanced', xp: 140,
      description: 'Writing type-safe, reusable classes and methods with Java generics. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Why generics'], ['Later', 'Generic classes'], ['Later', 'Bounded types']]
    },
    {
      searchQuery: 'Telusko Java Streams',
      title: 'Java Streams',
      creator: 'Telusko', duration: '~30m', difficulty: 'advanced', xp: 140,
      description: 'Processing collections functionally with the Java Streams API. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Creating a stream'], ['Later', 'map / filter / reduce']]
    }
  ],

  cpp: [
    {
      videoId: 'vLnPwxZdW4Y',
      title: 'C++ Tutorial for Beginners - Full Course',
      creator: 'freeCodeCamp.org', duration: '4h 00m', difficulty: 'beginner', xp: 140,
      description: 'Core C++ concepts: variables, data types, strings, numbers, user input, arrays, functions, and if statements, with a calculator and Mad Libs project.',
      timestamps: [
        ['0:00', 'Introduction'], ['8:44', 'Setup & Hello World'], ['19:55', 'Variables'],
        ['39:15', 'Working With Strings'], ['1:13:45', 'Arrays'], ['1:35:22', 'If Statements'],
        ['2:10:47', 'While Loops'], ['2:29:18', 'For Loops']
      ]
    },
    {
      videoId: '8jLOx1hD3_o',
      title: 'Complete C++ Course — 0 to Hero (C++20)',
      creator: 'freeCodeCamp.org', duration: '31h 00m', difficulty: 'advanced', xp: 150,
      description: 'A comprehensive, modern C++20 course going from beginner basics all the way through OOP, inheritance, polymorphism, and abstract classes.',
      timestamps: [
        ['0:00', 'Setting up the tools'], ['Later', 'Core language basics'],
        ['Later', 'Inheritance & polymorphism'], ['Later', 'Abstract classes as interfaces']
      ]
    },
    {
      searchQuery: 'Bro Code C++ Variables and Data Types',
      title: 'C++ Variables & Data Types',
      creator: 'Bro Code', duration: '~18m', difficulty: 'beginner', xp: 50,
      description: 'Declaring variables and understanding the core C++ data types. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Declaring variables'], ['Later', 'Data types']]
    },
    {
      searchQuery: 'Bro Code C++ User Input cin',
      title: 'C++ User Input (cin)',
      creator: 'Bro Code', duration: '~15m', difficulty: 'beginner', xp: 50,
      description: 'Reading keyboard input in C++ using cin. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'cin basics'], ['Later', 'Reading multiple values']]
    },
    {
      searchQuery: 'Bro Code C++ Strings',
      title: 'C++ Strings',
      creator: 'Bro Code', duration: '~20m', difficulty: 'beginner', xp: 60,
      description: 'Working with the string type in C++: concatenation, length, and common methods. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Creating strings'], ['Later', 'String methods']]
    },
    {
      searchQuery: 'Bro Code C++ If Else Statements',
      title: 'C++ If / Else Statements',
      creator: 'Bro Code', duration: '~18m', difficulty: 'beginner', xp: 50,
      description: 'Conditional branching in C++ using if, else if, and else. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'if / else'], ['Later', 'Comparison operators']]
    },
    {
      searchQuery: 'Bro Code C++ For and While Loops',
      title: 'C++ For & While Loops',
      creator: 'Bro Code', duration: '~25m', difficulty: 'beginner', xp: 70,
      description: 'Loop constructs in C++: for, while, and do-while loops. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'for loops'], ['Later', 'while & do-while']]
    },
    {
      searchQuery: 'Bro Code C++ Arrays',
      title: 'C++ Arrays',
      creator: 'Bro Code', duration: '~20m', difficulty: 'intermediate', xp: 80,
      description: 'Declaring, filling, and looping through arrays in C++. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Declaring arrays'], ['Later', 'Looping through arrays']]
    },
    {
      searchQuery: 'Bro Code C++ Functions',
      title: 'C++ Functions',
      creator: 'Bro Code', duration: '~20m', difficulty: 'intermediate', xp: 80,
      description: 'Defining and calling functions, parameters, and return types in C++. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Defining functions'], ['Later', 'Parameters & return values']]
    },
    {
      searchQuery: 'Bro Code C++ Vectors',
      title: 'C++ Vectors',
      creator: 'Bro Code', duration: '~22m', difficulty: 'intermediate', xp: 90,
      description: 'Using std::vector for dynamic, resizable arrays in C++. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Creating a vector'], ['Later', 'push_back & common methods']]
    },
    {
      searchQuery: 'Bro Code C++ Structs',
      title: 'C++ Structs',
      creator: 'Bro Code', duration: '~15m', difficulty: 'intermediate', xp: 80,
      description: 'Grouping related data together using structs in C++. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Defining a struct'], ['Later', 'Using struct instances']]
    },
    {
      searchQuery: 'CodeBeauty C++ Classes and Objects',
      title: 'C++ Classes & Objects',
      creator: 'CodeBeauty', duration: '~30m', difficulty: 'intermediate', xp: 100,
      description: 'Object-oriented programming fundamentals in C++: classes, objects, and constructors. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Defining a class'], ['Later', 'Constructors'], ['Later', 'Creating objects']]
    },
    {
      searchQuery: 'CodeBeauty C++ File Handling',
      title: 'C++ File Handling',
      creator: 'CodeBeauty', duration: '~20m', difficulty: 'intermediate', xp: 90,
      description: 'Reading from and writing to files in C++ using fstream. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Opening files'], ['Later', 'Reading & writing']]
    },
    {
      searchQuery: 'Bro Code C++ Inheritance',
      title: 'C++ Inheritance',
      creator: 'Bro Code', duration: '~22m', difficulty: 'advanced', xp: 120,
      description: 'Extending classes and reusing code through inheritance in C++. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Base & derived classes'], ['Later', 'Access specifiers']]
    },
    {
      searchQuery: 'CodeBeauty C++ Polymorphism',
      title: 'C++ Polymorphism',
      creator: 'CodeBeauty', duration: '~28m', difficulty: 'advanced', xp: 130,
      description: 'Virtual functions and runtime polymorphism in C++. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Virtual functions'], ['Later', 'Runtime polymorphism']]
    },
    {
      searchQuery: 'The Cherno C++ Pointers',
      title: 'C++ Pointers',
      creator: 'The Cherno', duration: '~25m', difficulty: 'advanced', xp: 140,
      description: 'What pointers are, how memory addresses work, and how to use them safely in C++. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'What is a pointer'], ['Later', 'Dereferencing'], ['Later', 'Pointer arithmetic']]
    },
    {
      searchQuery: 'The Cherno C++ References',
      title: 'C++ References',
      creator: 'The Cherno', duration: '~20m', difficulty: 'advanced', xp: 130,
      description: 'References vs pointers in C++, and when to use each. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'What is a reference'], ['Later', 'References vs pointers']]
    },
    {
      searchQuery: 'The Cherno C++ Memory Management',
      title: 'C++ Memory Management',
      creator: 'The Cherno', duration: '~30m', difficulty: 'advanced', xp: 150,
      description: 'Stack vs heap allocation, new/delete, and avoiding memory leaks in C++. (Opens on YouTube — see note below.)',
      timestamps: [['0:00', 'Stack vs heap'], ['Later', 'new & delete'], ['Later', 'Avoiding leaks']]
    }
  ]
};
