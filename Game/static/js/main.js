const error = document.getElementById('error-message');
error.style.display = 'none';
const gameSession = document.getElementById('gameSession');
const playerName = document.getElementById('playerName');
const form = document.getElementById('container');

function capitalizeWords(str) {
    return str
        .split(' ') // Split the string into an array of words
        .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()) // Capitalize the first letter of each word
        .join(' '); // Join the words back into a single string
}

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let gameSessionValue = gameSession.value.trim(); 
    let gameSessionId = gameSessionValue ? gameSessionValue : null;

    // Capitalize player name
    const capitalizedPlayerName = capitalizeWords(playerName.value.trim());

    const response = await fetch('/requestServer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            playerName: capitalizedPlayerName,
            gameSession: gameSessionId
        })
    });

    const result = await response.json();

    if (result.isSuccess) {
        console.log('Success : ' + result.message);
        if (!gameSession.value)
            window.location.href = '/gameSettings';
        else if (gameSession.value)
            window.location.href = '/lobby';
    } else {
        console.log('Failure : ' + result.message);
        error.innerText = 'Failure : ' + result.message
        error.style.display = 'block';

    }
});
