document.addEventListener('DOMContentLoaded', () => {
    const output = document.getElementById('output');
    const input = document.getElementById('command-input');
    const clearButton = document.getElementById('clearButton');
    const docsButton = document.getElementById('docsButton');
    const exampleLinks = document.querySelectorAll('.example-link');

    function appendOutput(text, isCommand = false) {
        const line = document.createElement('div');
        line.className = isCommand ? 'input' : 'output';
        line.innerHTML = isCommand ? `<span class="prompt">&gt;</span> ${text}` : text;
        output.appendChild(line);
        output.scrollTop = output.scrollHeight;
    }

    async function executeCommand(command) {
        appendOutput(command, true);

        try {
            const response = await fetch('/execute', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ code: command }),
            });

            const data = await response.json();
            
            if (data.error) {
                appendOutput(`Error: ${data.error}`, false);
            } else if (data.result) {
                appendOutput(data.result, false);
            }
        } catch (error) {
            appendOutput(`Error: ${error.message}`, false);
        }
    }

    input.addEventListener('keydown', async (e) => {
        if (e.key === 'Enter') {
            const command = input.value.trim();
            if (!command) return;

            input.value = '';
            await executeCommand(command);
        }
    });

    clearButton.addEventListener('click', (e) => {
        e.preventDefault();
        output.innerHTML = '';
    });

    docsButton.addEventListener('click', (e) => {
        e.preventDefault();
        appendOutput("Documentation feature coming soon!", false);
    });

    exampleLinks.forEach(link => {
        link.addEventListener('click', async (e) => {
            e.preventDefault();
            const example = link.getAttribute('data-example');
            let code;

            switch (example) {
                case 'hello-world':
                    code = 'parley hello';
                    break;
                case 'arithmetic':
                    code = 'parley 2 + 3 * 4';
                    break;
                case 'variables':
                    code = 'hoist x = 5\nif x > 3 do parley x';
                    break;
                case 'nested-if':
                    code = 'if 2 + 3 ?= 5 do parley 5 is equal to 7\n';
                    break;
                default:
                    code = 'parley "No example selected"';
            }

            const lines = code.split('\n');
            for (const line of lines) {
                await executeCommand(line.trim());
            }
        });
    });
});

