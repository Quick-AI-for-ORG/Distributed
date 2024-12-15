const error = document.getElementById('error-message');
error.style.display = 'none';


const cancelButton = document.querySelector('.cancelButton');

cancelButton.addEventListener('click', async (event) => {
  event.preventDefault();
  const response = await fetch('/disconnectPlayer', {
    method: 'GET',
    headers: {
        'Content-Type': 'application/json',
    }
})
    
const result = await response.json();

if (result.isSuccess) {
    console.log('Success : ' + result.message);
    window.location.href = '/';
} else {
    console.log('Failure : ' + result.message);
    error.innerText = 'Failure : ' + result.message
    error.style.display = 'block';
  }
});

// async function loadPlayers() {
//    const response = await fetch('/requestServer', {
//     method: 'POST',
//     headers: {
//         'Content-Type': 'application/json'
//     },
//     body: JSON.stringify({ 
//         playerName: capitalizedPlayerName,
//         gameSession: gameSessionId
//     })
// });


//     setTimeout(loadPlayers, 1000);
// }


// await loadPlayers();