document.addEventListener('DOMContentLoaded', () => {
    const terminal = document.getElementById('terminal');
    const output = document.getElementById('output');
    const input = document.getElementById('codeInput');
    const docsButton = document.getElementById('docsButton');
    const clearButton = document.getElementById('clearButton');
    const exampleLinks = document.querySelectorAll('.example-link');

    let commandHistory = [];
    let historyIndex = -1;

    const examples = {
        'hello-world': 'print("Ahoy, world!")',
        'arithmetic': `yeet x = 10
yeet y = 5
print(x + y)
print(x - y)
print(x * y)
print(x / y)`,
        'variables': `yeet age = 25
if age >= 18 bet print("Ye be old enough to sail!")
but_if age < 18 bet print("Ye be too young to sail, matey!")`,
        'fibonacci': `yeet a = 0
yeet b = 1
print(a)
print(b)
yeet i = 0
while i < 8 bet
    yeet c = a + b
    print(c)
    yeet a = b
    yeet b = c
    yeet i = i + 1`,
        'factorial': `yeet n = 5
yeet result = 1
yeet i = 1
while i <= n bet
    yeet result = result * i
    yeet i = i + 1
print(result)`
    };

    input.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            e.preventDefault();
            const code = input.value.trim();
            if (!code) return;

            appendToOutput('input', code);
            commandHistory.push(code);
            historyIndex = commandHistory.length;

            try {
                const response = await fetch('/execute', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code }),
                });

                const data = await response.json();

                if (response.ok) {
                    data.result.forEach(item => appendToOutput('output', item));
                } else {
                    appendToOutput('error', data.error);
                }
            } catch (error) {
                appendToOutput('error', 'An error occurred while executing the code.');
            }

            input.value = '';
            terminal.scrollTop = terminal.scrollHeight;
        } else if (e.key === 'ArrowUp') {
            e.preventDefault();
            if (historyIndex > 0) {
                historyIndex--;
                input.value = commandHistory[historyIndex];
            }
        } else if (e.key === 'ArrowDown') {
            e.preventDefault();
            if (historyIndex < commandHistory.length - 1) {
                historyIndex++;
                input.value = commandHistory[historyIndex];
            } else {
                historyIndex = commandHistory.length;
                input.value = '';
            }
        }
    });

    function appendToOutput(type, content) {
        const element = document.createElement('div');
        element.classList.add(type);
        element.textContent = `${type === 'input' ? '> ' : ''}${content}`;
        output.appendChild(element);
    }

    docsButton.addEventListener('click', (e) => {
        e.preventDefault();
        const docsContent = `
            ScurvyScript Documentation:
            
            1. Variable declaration:
               yeet variable_name = value
            
            2. Print statement:
               print(expression)
            
            3. Conditional statements:
               if condition bet action
               but_if condition bet action
               by_chance action
            
            4. Boolean operations:
               with (AND), or (OR), nay (NOT)
            
            5. Comparison operators:
               >, <, >=, <=, ?= (equals)
            
            6. Arithmetic operations:
               +, -, *, /
        `;
        appendToOutput('output', docsContent);
        terminal.scrollTop = terminal.scrollHeight;
    });

    clearButton.addEventListener('click', (e) => {
        e.preventDefault();
        output.innerHTML = '';
        const introElement = document.createElement('div');
        introElement.classList.add('intro');
        introElement.innerHTML = `
            <p>Welcome to ScurvyScript, ye scurvy dog!</p>
            <p>ScurvyScript be a pirate-themed programming language that'll make ye feel like ye're sailing the seven seas of code.</p>
            <p>Here be some basic commands to get ye started:</p>
            <ul>
                <li><code>yeet</code>: Declare a variable, ye landlubber!</li>
                <li><code>print</code>: Show yer message to the crew!</li>
                <li><code>if</code>, <code>but_if</code>, <code>by_chance</code>: Make decisions like a true captain!</li>
                <li><code>with</code>, <code>or</code>, <code>nay</code>: Combine yer thoughts, matey!</li>
            </ul>
            <p>Now set sail and start coding, ye scurvy dog!</p>
        `;
        output.appendChild(introElement);
    });

    exampleLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const exampleCode = examples[e.target.dataset.example];
            input.value = exampleCode;
            input.focus();
        });
    });
});

