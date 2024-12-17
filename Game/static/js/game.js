
const input = document.querySelector('#game-input');
const button = document.querySelector('#sendButton');
const area = document.querySelector('#player-message');
const round = document.querySelector('#round');
const message = document.querySelector('#message');
const error = document.querySelector('#error-message');
const role = document.getElementById('role')
const score = document.getElementById('score');
const health = document.getElementById('health');
const container = document.querySelector('#shown');
const quit = document.querySelector('#quit');
const states = document.querySelectorAll('.state')
const skip = document.querySelector('#skip')
skip.disabled = true
// Function to send updates to the server
const sendUpdate = async (inputValue = null) => {
    const result = await fetchRequest('/sendUpdate', 'POST', { input: inputValue });
    handleUpdateResponse(result);
};

// Function to receive updates from the server
const receiveUpdate = async () => {
    const result = await fetchRequest('/recieveUpdate', 'GET');
    handleUpdateResponse(result);
};

// Helper function to make fetch requests
const fetchRequest = async (url, method, body = null) => {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json',
            },
        };

        if (body) options.body = JSON.stringify(body);

        const response = await fetch(url, options);
        return await response.json();

};

// Handle server response
const handleUpdateResponse = (result) => {
    console.log(result.message);
    if (result.isSuccess) {
        area.innerHTML = result.input.join('\n');
        score.innerText = result.score;
        health.innerText = result.health;
        nextRound(result);
    } else {
        console.log(result.message);
        displayMessage(false,result.message);
        if (result.message.includes("No more tries")) {
            input.disabled = true;
            states[0].style.display = 'none';
            states[1].style.display = 'block'
        }
        area.innerHTML = result.input.join('\n');
    if (result.message.includes('End of Game') || result.round === 0 || result.message.include('Failure')) {
        showGameOver();
        input.disabled = true;
        displayMessage(false, `Game Ended. Exitting in 10 seconds`);
        setTimeout(() => {
            window.location.href = '/';
        }, 10000);
    }

    }
};

// Display a message in the message box
const displayMessage = (bool, text) => {
    if (bool === true){
        message.innerText = text;
        message.style.display = 'block';
    }
    else{
        error.innerText = text
        error.style.display = 'block'
    }
};

// Show the game over screen
const showGameOver = () => {
    const gameOverElement = document.getElementById('game-over');
    gameOverElement.style.display = 'block';
};

// Event listeners
button.addEventListener('click', async (event) => {
    event.preventDefault();
    await sendUpdate(input.value);
    input.value = '';
});


skip.addEventListener('click', async (event) => {
    event.preventDefault();
    await sendUpdate("SKIP PLEASE");
    input.value = '';
    });
input.addEventListener('keydown', (event) => {
    if (event.key === 'Enter') {
        button.click();
    }
});

// Periodically fetch updates from the server
setInterval(() => {
    receiveUpdate();
}, 1000);

// Initialize application on window load
document.addEventListener('DOMContentLoaded', async () => {
    const result = await fetchRequest('/roundStart', 'GET');
    unpackAtStart(result);
});

const unpackAtStart = (result) => {
    console.log(result.message);
    round.innerText = result.round    
    if (result.role === "Clue Giver") {
        role.innerText = `Your word is ${result.word}`;
        skip.disabled = false
    }
    else {
        role.innerText = `${result.clueGiver} is the Clue Giver`;
    }
}


const nextRound = (result) => {
    area.innerHTML = result.input.join('\n');
    if (result.message.includes('End of Game') || result.round === 0) {
        showGameOver();
        input.disabled = true;
        displayMessage(false, `${result.message}. Exitting in 10 seconds`);
        setTimeout(() => {
            window.location.href = '/';
        }, 10000);
    }
    else if (round.innerText != result.round) {
        displayMessage(true,`End of ${round.innerText}. Next round starting in 3 seconds.`);
        input.disabled = true;
        setTimeout(() => {
            window.location.href = '/game';
        }, 3000);
    }
}



quit.addEventListener('click', async (event) => {
  event.preventDefault();
  const result = await fetchRequest('/disconnectPlayer', 'GET');
  
  if (result.isSuccess) {
      console.log('Success : ' + result.message);
      window.location.href = '/';
  } else {
      console.log('Failure : ' + result.message);
      error.innerText = 'Failure : ' + result.message
      error.style.display = 'block';
    }
  });


