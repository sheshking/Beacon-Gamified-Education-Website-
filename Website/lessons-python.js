// ============================================
// BEACON — Python lesson data (Basics & Input/O)
// ============================================

const BEACON_LESSONS = {
  langKey: 'python',
  langLabel: 'Python',
  sections: [
    {
      key: 'basics',
      label: '[B] Basics & Input/O',
      lessons: [
        {
          id: 'L1', title: '1. Hello World', xp: 10,
          concept: "print() sends text to the terminal. Anything inside quotes is displayed exactly as written.",
          example: "print('BEACON')\n--> Expected Terminal Output: \"BEACON\"",
          instruction: "Print 'BEACON' to boot the system.",
          starter: "print('BEACON')",
          expected: "BEACON",
          hint: "Call print() and put BEACON inside quotes, like print('BEACON').",
          solution: "print('BEACON')"
        },
        {
          id: 'L2', title: '2. Simple Numbers', xp: 10,
          concept: "Numbers don't need quotes — print(42) outputs the number itself, not text.",
          example: "print(42)\n--> Expected Terminal Output: \"42\"",
          instruction: "Print the number 42 to check the XP counter.",
          starter: "# print the number 42\n",
          expected: "42",
          hint: "Just write print(42) — no quotes needed for numbers.",
          solution: "print(42)"
        },
        {
          id: 'L3', title: '3. Double Print', xp: 10,
          concept: "Each call to print() starts a new line automatically.",
          example: "print('Player One')\nprint('Ready')\n--> Expected Terminal Output:\n\"Player One\"\n\"Ready\"",
          instruction: 'Print "Player One", then print "Ready" on the next line.',
          starter: '# print "Player One" then "Ready"\n',
          expected: "Player One\nReady",
          hint: "Use two separate print() calls, one for each phrase.",
          solution: "print('Player One')\nprint('Ready')"
        },
        {
          id: 'L4', title: '4. Print Math', xp: 10,
          concept: "Python evaluates math expressions before printing — print(6 * 7) prints the result, 42.",
          example: "print(6 * 7)\n--> Expected Terminal Output: \"42\"",
          instruction: "Print the result of 6 * 7.",
          starter: "# print the result of 6 * 7\n",
          expected: "42",
          hint: "Put the expression 6 * 7 directly inside print() — no need to store it first.",
          solution: "print(6 * 7)"
        },
        {
          id: 'L5', title: '5. Multiline String', xp: 10,
          concept: "Triple quotes ''' ''' let a single string span multiple lines.",
          example: "print('''Loading...\n100% Complete''')\n--> Expected Terminal Output:\n\"Loading...\"\n\"100% Complete\"",
          instruction: "Print a single multi-line string that outputs \"Loading...\" then \"100% Complete\".",
          starter: "# print a triple-quoted multiline string\n",
          expected: "Loading...\n100% Complete",
          hint: "Wrap your text in triple quotes: print('''Loading...\\n100% Complete''').",
          solution: "print('''Loading...\n100% Complete''')"
        },
        {
          id: 'L6', title: '6. Variable Creation', xp: 10,
          concept: "A variable stores a value under a name using =. You can print that name later to see the value.",
          example: "xp = 100\nprint(xp)\n--> Expected Terminal Output: \"100\"",
          instruction: "Create a variable named xp set to 100, then print it.",
          starter: "# create xp = 100, then print it\n",
          expected: "100",
          hint: "Write xp = 100 on one line, then print(xp) on the next.",
          solution: "xp = 100\nprint(xp)"
        },
        {
          id: 'L7', title: '7. String Variables', xp: 10,
          concept: "Variables can hold text too — just wrap the value in quotes when assigning it.",
          example: "name = 'Beacon'\nprint(name)\n--> Expected Terminal Output: \"Beacon\"",
          instruction: 'Create a variable named "name" set to "Beacon", then print it.',
          starter: "# create name = 'Beacon', then print it\n",
          expected: "Beacon",
          hint: "Write name = 'Beacon', then print(name).",
          solution: "name = 'Beacon'\nprint(name)"
        },
        {
          id: 'L8', title: '8. Variable Math', xp: 10,
          concept: "You can do math directly on variables once they're created, just like with numbers.",
          example: "a = 5\nb = 3\nprint(a + b)\n--> Expected Terminal Output: \"8\"",
          instruction: "Create a = 5 and b = 3, then print their sum.",
          starter: "# create a = 5, b = 3, then print a + b\n",
          expected: "8",
          hint: "Create a = 5 and b = 3, then print(a + b).",
          solution: "a = 5\nb = 3\nprint(a + b)"
        },
        {
          id: 'L9', title: '9. Reassigning Vars', xp: 10,
          concept: "Variables can be reassigned — the new value simply replaces the old one.",
          example: "level = 1\nlevel = 2\nprint(level)\n--> Expected Terminal Output: \"2\"",
          instruction: "Set level to 1, reassign it to 2, then print level.",
          starter: "# set level = 1, reassign level = 2, then print level\n",
          expected: "2",
          hint: "Set level = 1, then on the next line set level = 2, then print(level).",
          solution: "level = 1\nlevel = 2\nprint(level)"
        },
        {
          id: 'L10', title: '10. Combined Echo', xp: 10,
          concept: "You can combine strings and numbers with + if you convert the number to text using str() first.",
          example: "name = 'Nova'\nxp = 50\nprint(name + ' earned ' + str(xp) + ' XP')\n--> Expected Terminal Output: \"Nova earned 50 XP\"",
          instruction: 'Create name = "Nova" and xp = 50, then print: Nova earned 50 XP',
          starter: "# create name = 'Nova', xp = 50\n# print: Nova earned 50 XP\n",
          expected: "Nova earned 50 XP",
          hint: "Use str(xp) to turn the number into text before joining it with + to the other strings.",
          solution: "name = 'Nova'\nxp = 50\nprint(name + ' earned ' + str(xp) + ' XP')"
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
// BEACON — Boss Fight question bank (Python)
// ============================================

const BEACON_BOSS = {
  langKey: 'python',
  questions: [
    {
      type: 'debug', id: 'B1',
      prompt: "This line should print BEACON but has a typo. Which is the corrected line?",
      code: "pint('BEACON')",
      options: [
        { id: 'a', text: "pint('BEACON')" },
        { id: 'b', text: "print('BEACON')" },
        { id: 'c', text: "print(BEACON)" },
        { id: 'd', text: "Print('BEACON')" }
      ],
      correctOptionId: 'b'
    },
    {
      type: 'debug', id: 'B2',
      prompt: "This code should print the sum of a and b (8), but it doesn't. What's the bug?",
      code: "a = 5\nb = 3\nprint(a - b)",
      options: [
        { id: 'a', text: "a - b should be a + b" },
        { id: 'b', text: "a and b need quotes" },
        { id: 'c', text: "print() should be Print()" },
        { id: 'd', text: "5 and 3 should be strings" }
      ],
      correctOptionId: 'a'
    },
    {
      type: 'debug', id: 'B3',
      prompt: "This multiline string is broken. What's wrong with it?",
      code: "print('''Loading...\n100% Complete'')",
      options: [
        { id: 'a', text: "The string should end with ''' not ''" },
        { id: 'b', text: "print() can't span multiple lines" },
        { id: 'c', text: "It needs a semicolon at the end" },
        { id: 'd', text: "Should use double quotes instead" }
      ],
      correctOptionId: 'a'
    },
    {
      type: 'code', id: 'B4',
      prompt: "Create a variable called score set to 75, then print it.",
      starter: "# your code here\n",
      expected: "75"
    },
    {
      type: 'code', id: 'B5',
      prompt: 'Create name = \'Beacon\' and level = 3, then print: Beacon is level 3',
      starter: "# your code here\n",
      expected: "Beacon is level 3"
    }
  ]
};
