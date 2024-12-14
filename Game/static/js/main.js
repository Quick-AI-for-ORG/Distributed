const gameSession = document.getElementById('gameSession');
const playerName = document.getElementById('playerName');
const form = document.getElementById('container');
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let gameSessionValue = gameSession.value.trim(); 
    let gameSessionId = gameSessionValue ? gameSessionValue : null;

    const response = await fetch('/requestServer', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
            playerName: playerName.value.trim(),
            gameSession: gameSessionId
        })
    });

    const result = await response.json();

    if (result.isSuccess) {
        console.log('Success : ' + result.message);
        window.location.href = '/gameSettings';
    } else {
        console.log('Failure : ' + result.message);
    }
});
