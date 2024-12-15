const input = document.querySelector('#game-input')
const button = document.querySelector('#sendButton')
const area = document.querySelector('#player-message')

const sendUpdate = async () => {
    const response = await fetch('/sendUpdate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            input:""
        })
    });

    const result = await response.json();

    if (result.isSuccess) {
        console.log('Success : ' + result.message);
        area.innerHTML = result.input.join('\n');
    } else {
        console.log('Failure : ' + result.message);
    }
};

// Call the function every 2 seconds
setInterval(sendUpdate, 2000);
button.addEventListener('click', async (event) => {
    event.preventDefault();
    await sendUpdate();
    input.value = '';
});