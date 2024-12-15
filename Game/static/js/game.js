const input = document.querySelector('#game-input');
const button = document.querySelector('#sendButton');
const area = document.querySelector('#player-message');

// Send update function
const sendUpdate = async (inputValue = null) => {
    const response = await fetch('/sendUpdate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            input: inputValue // Send input only if provided, otherwise null
        })
    });

    const result = await response.json();

    if (result.isSuccess) {
        console.log('Success : ' + result.message);
        area.innerHTML = result.input.join('\n'); // Update area with new data
    } else {
        console.log('Failure : ' + result.message);
    }
};

// Button click to send input
button.addEventListener('click', async (event) => {
    event.preventDefault();
    await sendUpdate(input.value); // Send the input value when button is clicked
    input.value = ''; // Clear the input field after sending
});

// Periodically update the area (loading functionality)
setInterval(() => {
    sendUpdate(); // Call without input value to act as "loading"
}, 2000);
