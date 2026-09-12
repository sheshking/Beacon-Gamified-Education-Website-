// ============================================
// BEACON — C++ lesson data (Basics & Input/O)
// ============================================

const BEACON_LESSONS = {
  langKey: 'cpp',
  langLabel: 'C++',
  sections: [
    {
      key: 'basics',
      label: '[B] Basics & Input/O',
      lessons: [
        {
          id: 'L1', title: '1. Hello World', xp: 10,
          concept: "cout << sends text to the terminal; endl moves the cursor to a new line afterward.",
          example: "cout << \"BEACON\" << endl;\n--> Expected Terminal Output: \"BEACON\"",
          instruction: "Print 'BEACON' to boot the system.",
          starter: "cout << \"BEACON\" << endl;",
          expected: "BEACON",
          hint: "cout << \"BEACON\" << endl;",
          solution: "cout << \"BEACON\" << endl;"
        },
        {
          id: 'L2', title: '2. Simple Numbers', xp: 10,
          concept: "Numbers print without quotes — quotes are only for text.",
          example: "cout << 42 << endl;\n--> Expected Terminal Output: \"42\"",
          instruction: "Print the number 42 to check the XP counter.",
          starter: "// print the number 42\n",
          expected: "42",
          hint: "cout << 42 << endl;",
          solution: "cout << 42 << endl;"
        },
        {
          id: 'L3', title: '3. Double Print', xp: 10,
          concept: "Each cout statement can end its line with endl before the next one starts.",
          example: "cout << \"Player One\" << endl;\ncout << \"Ready\" << endl;\n--> Expected Terminal Output:\n\"Player One\"\n\"Ready\"",
          instruction: 'Print "Player One", then print "Ready" on the next line.',
          starter: '// print "Player One" then "Ready"\n',
          expected: "Player One\nReady",
          hint: "Use two cout lines, one per phrase, each ending with << endl;.",
          solution: "cout << \"Player One\" << endl;\ncout << \"Ready\" << endl;"
        },
        {
          id: 'L4', title: '4. Print Math', xp: 10,
          concept: "C++ evaluates the expression before sending it to cout.",
          example: "cout << 6 * 7 << endl;\n--> Expected Terminal Output: \"42\"",
          instruction: "Print the result of 6 * 7.",
          starter: "// print the result of 6 * 7\n",
          expected: "42",
          hint: "cout << 6 * 7 << endl;",
          solution: "cout << 6 * 7 << endl;"
        },
        {
          id: 'L5', title: '5. Multiline String', xp: 10,
          concept: "Two cout statements in a row produce two separate lines of output.",
          example: "cout << \"Loading...\" << endl;\ncout << \"100% Complete\" << endl;\n--> Expected Terminal Output:\n\"Loading...\"\n\"100% Complete\"",
          instruction: 'Print two lines: "Loading..." then "100% Complete".',
          starter: "// print two lines: Loading... then 100% Complete\n",
          expected: "Loading...\n100% Complete",
          hint: "Print \"Loading...\" and \"100% Complete\" with two separate cout statements.",
          solution: "cout << \"Loading...\" << endl;\ncout << \"100% Complete\" << endl;"
        },
        {
          id: 'L6', title: '6. Variable Creation', xp: 10,
          concept: "Declare a variable with its type, e.g. int xp = 100;, then print it with cout.",
          example: "int xp = 100;\ncout << xp << endl;\n--> Expected Terminal Output: \"100\"",
          instruction: "Create a variable named xp set to 100, then print it.",
          starter: "// create int xp = 100, then print it\n",
          expected: "100",
          hint: "int xp = 100; then cout << xp << endl;",
          solution: "int xp = 100;\ncout << xp << endl;"
        },
        {
          id: 'L7', title: '7. String Variables', xp: 10,
          concept: "Text variables use the string type (lowercase in C++).",
          example: "string name = \"Beacon\";\ncout << name << endl;\n--> Expected Terminal Output: \"Beacon\"",
          instruction: 'Create a variable named "name" set to "Beacon", then print it.',
          starter: "// create string name = \"Beacon\", then print it\n",
          expected: "Beacon",
          hint: "string name = \"Beacon\"; then cout << name << endl;",
          solution: "string name = \"Beacon\";\ncout << name << endl;"
        },
        {
          id: 'L8', title: '8. Variable Math', xp: 10,
          concept: "You can add int variables directly inside a cout statement.",
          example: "int a = 5;\nint b = 3;\ncout << a + b << endl;\n--> Expected Terminal Output: \"8\"",
          instruction: "Create a = 5 and b = 3, then print their sum.",
          starter: "// create int a = 5, b = 3, then print a + b\n",
          expected: "8",
          hint: "int a = 5; int b = 3; then cout << a + b << endl;",
          solution: "int a = 5;\nint b = 3;\ncout << a + b << endl;"
        },
        {
          id: 'L9', title: '9. Reassigning Vars', xp: 10,
          concept: "Reassign a variable by writing its name again with a new value — no type keyword needed the second time.",
          example: "int level = 1;\nlevel = 2;\ncout << level << endl;\n--> Expected Terminal Output: \"2\"",
          instruction: "Set level to 1, reassign it to 2, then print level.",
          starter: "// set int level = 1, reassign level = 2, then print level\n",
          expected: "2",
          hint: "int level = 1; level = 2; then cout << level << endl;",
          solution: "int level = 1;\nlevel = 2;\ncout << level << endl;"
        },
        {
          id: 'L10', title: '10. Combined Echo', xp: 10,
          concept: "Chain multiple << operators in one cout statement to combine strings and numbers.",
          example: "string name = \"Nova\";\nint xp = 50;\ncout << name << \" earned \" << xp << \" XP\" << endl;\n--> Expected Terminal Output: \"Nova earned 50 XP\"",
          instruction: 'Create name = "Nova" and xp = 50, then print: Nova earned 50 XP',
          starter: "// create string name = \"Nova\", int xp = 50\n// print: Nova earned 50 XP\n",
          expected: "Nova earned 50 XP",
          hint: "cout << name << \" earned \" << xp << \" XP\" << endl;",
          solution: "string name = \"Nova\";\nint xp = 50;\ncout << name << \" earned \" << xp << \" XP\" << endl;"
        }
      ]
    },
    {
      key: 'control-flow', label: '[C] Control Flow (coming soon)', locked: true, lessons: []
    },
    {
      key: 'functions', label: '[D] Functions (coming soon)', locked: true, lessons: []
    }
  ]
};

// ============================================
// BEACON — Boss Fight question bank (C++)
// ============================================

const BEACON_BOSS = {
  langKey: 'cpp',
  questions: [
    {
      type: 'debug', id: 'B1',
      prompt: "This statement is missing something C++ requires. What's the fix?",
      code: "cout << \"BEACON\" << endl",
      options: [
        { id: 'a', text: "Add a semicolon at the end" },
        { id: 'b', text: "Change cout to Cout" },
        { id: 'c', text: "Remove the quotes" },
        { id: 'd', text: "Remove endl" }
      ],
      correctOptionId: 'a'
    },
    {
      type: 'debug', id: 'B2',
      prompt: "This code should print the sum of a and b (8), but it doesn't. What's the bug?",
      code: "int a = 5;\nint b = 3;\ncout << a - b << endl;",
      options: [
        { id: 'a', text: "a - b should be a + b" },
        { id: 'b', text: "a and b need to be strings" },
        { id: 'c', text: "cout should be Cout" },
        { id: 'd', text: "5 and 3 should be in quotes" }
      ],
      correctOptionId: 'a'
    },
    {
      type: 'debug', id: 'B3',
      prompt: "This statement is missing something C++ requires. What's the fix?",
      code: "string name = \"Beacon\";\ncout << name << endl",
      options: [
        { id: 'a', text: "Add a semicolon after the cout line" },
        { id: 'b', text: "string should be capitalized" },
        { id: 'c', text: "cout needs two << operators minimum" },
        { id: 'd', text: "name should be quoted when printed" }
      ],
      correctOptionId: 'a'
    },
    {
      type: 'code', id: 'B4',
      prompt: "Create an int variable called score set to 75, then print it.",
      starter: "// your code here\n",
      expected: "75"
    },
    {
      type: 'code', id: 'B5',
      prompt: 'Create string name = "Beacon" and int level = 3, then print: Beacon is level 3',
      starter: "// your code here\n",
      expected: "Beacon is level 3"
    }
  ]
};
