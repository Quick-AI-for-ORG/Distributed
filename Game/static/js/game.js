const input = document.querySelector('#game-input')
const button = document.querySelector('#sendButton')
const area = document.querySelector('#player-message')

button.addEventListener('click', async (event) => {
    event.preventDefault();
    const response = await fetch('/sendUpdate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            input: input.value
        })
    });

    const result = await response.json();

    if (result.isSuccess) {
        console.log('Success : ' + result.message);
        input.value = '';
        area.innerHTML = result.input.join('\n');
    } else {
        console.log('Failure : ' + result.message);
    }
})