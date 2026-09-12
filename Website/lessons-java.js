// ============================================
// BEACON — Java lesson data (Basics & Input/O)
// ============================================

const BEACON_LESSONS = {
  langKey: 'java',
  langLabel: 'Java',
  sections: [
    {
      key: 'basics',
      label: '[B] Basics & Input/O',
      lessons: [
        {
          id: 'L1', title: '1. Hello World', xp: 10,
          concept: "System.out.println() prints text to the terminal and moves to a new line afterward.",
          example: "System.out.println(\"BEACON\");\n--> Expected Terminal Output: \"BEACON\"",
          instruction: "Print 'BEACON' to boot the system.",
          starter: "System.out.println(\"BEACON\");",
          expected: "BEACON",
          hint: "Use System.out.println(\"BEACON\");",
          solution: "System.out.println(\"BEACON\");"
        },
        {
          id: 'L2', title: '2. Simple Numbers', xp: 10,
          concept: "Numbers are printed without quotes — quotes are only for text.",
          example: "System.out.println(42);\n--> Expected Terminal Output: \"42\"",
          instruction: "Print the number 42 to check the XP counter.",
          starter: "// print the number 42\n",
          expected: "42",
          hint: "System.out.println(42);",
          solution: "System.out.println(42);"
        },
        {
          id: 'L3', title: '3. Double Print', xp: 10,
          concept: "Each println() call automatically starts a new line for the next output.",
          example: "System.out.println(\"Player One\");\nSystem.out.println(\"Ready\");\n--> Expected Terminal Output:\n\"Player One\"\n\"Ready\"",
          instruction: 'Print "Player One", then print "Ready" on the next line.',
          starter: '// print "Player One" then "Ready"\n',
          expected: "Player One\nReady",
          hint: "Call System.out.println() twice, once per phrase.",
          solution: "System.out.println(\"Player One\");\nSystem.out.println(\"Ready\");"
        },
        {
          id: 'L4', title: '4. Print Math', xp: 10,
          concept: "Java evaluates the expression inside println() before printing the result.",
          example: "System.out.println(6 * 7);\n--> Expected Terminal Output: \"42\"",
          instruction: "Print the result of 6 * 7.",
          starter: "// print the result of 6 * 7\n",
          expected: "42",
          hint: "System.out.println(6 * 7);",
          solution: "System.out.println(6 * 7);"
        },
        {
          id: 'L5', title: '5. Multiline String', xp: 10,
          concept: "Two separate println() calls produce two lines of output, one after the other.",
          example: "System.out.println(\"Loading...\");\nSystem.out.println(\"100% Complete\");\n--> Expected Terminal Output:\n\"Loading...\"\n\"100% Complete\"",
          instruction: 'Print two lines: "Loading..." then "100% Complete".',
          starter: "// print two lines: Loading... then 100% Complete\n",
          expected: "Loading...\n100% Complete",
          hint: "Print \"Loading...\" and \"100% Complete\" with two separate println() calls.",
          solution: "System.out.println(\"Loading...\");\nSystem.out.println(\"100% Complete\");"
        },
        {
          id: 'L6', title: '6. Variable Creation', xp: 10,
          concept: "Declare a variable with its type, e.g. int xp = 100;, then reference it by name later.",
          example: "int xp = 100;\nSystem.out.println(xp);\n--> Expected Terminal Output: \"100\"",
          instruction: "Create a variable named xp set to 100, then print it.",
          starter: "// create int xp = 100, then print it\n",
          expected: "100",
          hint: "int xp = 100; then System.out.println(xp);",
          solution: "int xp = 100;\nSystem.out.println(xp);"
        },
        {
          id: 'L7', title: '7. String Variables', xp: 10,
          concept: "Text variables use the String type (capital S) instead of int.",
          example: "String name = \"Beacon\";\nSystem.out.println(name);\n--> Expected Terminal Output: \"Beacon\"",
          instruction: 'Create a variable named "name" set to "Beacon", then print it.',
          starter: "// create String name = \"Beacon\", then print it\n",
          expected: "Beacon",
          hint: "String name = \"Beacon\"; then System.out.println(name);",
          solution: "String name = \"Beacon\";\nSystem.out.println(name);"
        },
        {
          id: 'L8', title: '8. Variable Math', xp: 10,
          concept: "You can add int variables directly with + inside println().",
          example: "int a = 5;\nint b = 3;\nSystem.out.println(a + b);\n--> Expected Terminal Output: \"8\"",
          instruction: "Create a = 5 and b = 3, then print their sum.",
          starter: "// create int a = 5, b = 3, then print a + b\n",
          expected: "8",
          hint: "int a = 5; int b = 3; then System.out.println(a + b);",
          solution: "int a = 5;\nint b = 3;\nSystem.out.println(a + b);"
        },
        {
          id: 'L9', title: '9. Reassigning Vars', xp: 10,
          concept: "Reassign a variable by writing its name again with a new value — no type keyword needed the second time.",
          example: "int level = 1;\nlevel = 2;\nSystem.out.println(level);\n--> Expected Terminal Output: \"2\"",
          instruction: "Set level to 1, reassign it to 2, then print level.",
          starter: "// set int level = 1, reassign level = 2, then print level\n",
          expected: "2",
          hint: "int level = 1; level = 2; then System.out.println(level);",
          solution: "int level = 1;\nlevel = 2;\nSystem.out.println(level);"
        },
        {
          id: 'L10', title: '10. Combined Echo', xp: 10,
          concept: "Strings and numbers can be joined with + — Java automatically converts the number to text.",
          example: "String name = \"Nova\";\nint xp = 50;\nSystem.out.println(name + \" earned \" + xp + \" XP\");\n--> Expected Terminal Output: \"Nova earned 50 XP\"",
          instruction: 'Create name = "Nova" and xp = 50, then print: Nova earned 50 XP',
          starter: "// create String name = \"Nova\", int xp = 50\n// print: Nova earned 50 XP\n",
          expected: "Nova earned 50 XP",
          hint: "Join name + \" earned \" + xp + \" XP\" inside a single println() call.",
          solution: "String name = \"Nova\";\nint xp = 50;\nSystem.out.println(name + \" earned \" + xp + \" XP\");"
        }
      ]
    },
    {
      key: 'control-flow', label: '[C] Control Flow (coming soon)', locked: true, lessons: []
    },
    {
      key: 'functions', label: '[D] Methods (coming soon)', locked: true, lessons: []
    }
  ]
};

// ============================================
// BEACON — Boss Fight question bank (Java)
// ============================================

const BEACON_BOSS = {
  langKey: 'java',
  questions: [
    {
      type: 'debug', id: 'B1',
      prompt: "This statement is missing something Java requires. What's the fix?",
      code: "System.out.println(\"BEACON\")",
      options: [
        { id: 'a', text: "Add a semicolon at the end" },
        { id: 'b', text: "Change println to Println" },
        { id: 'c', text: "Remove the quotes" },
        { id: 'd', text: "Add extra parentheses around BEACON" }
      ],
      correctOptionId: 'a'
    },
    {
      type: 'debug', id: 'B2',
      prompt: "This code should print the sum of a and b (8), but it doesn't. What's the bug?",
      code: "int a = 5;\nint b = 3;\nSystem.out.println(a - b);",
      options: [
        { id: 'a', text: "a - b should be a + b" },
        { id: 'b', text: "a and b need to be Strings" },
        { id: 'c', text: "println should be print" },
        { id: 'd', text: "5 and 3 should be in quotes" }
      ],
      correctOptionId: 'a'
    },
    {
      type: 'debug', id: 'B3',
      prompt: "This declaration is missing something Java requires. What's the fix?",
      code: "String name = \"Beacon\"\nSystem.out.println(name);",
      options: [
        { id: 'a', text: "Add a semicolon after the String declaration" },
        { id: 'b', text: "String should be lowercase" },
        { id: 'c', text: "println needs two arguments" },
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
      prompt: 'Create String name = "Beacon" and int level = 3, then print: Beacon is level 3',
      starter: "// your code here\n",
      expected: "Beacon is level 3"
    }
  ]
};
