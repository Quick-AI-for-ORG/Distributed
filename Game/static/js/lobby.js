const error = document.getElementById('error-message');
error.style.display = 'none';

async function loadPlayers() {
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


    setTimeout(loadPlayers, 1000);
}


await loadPlayers();