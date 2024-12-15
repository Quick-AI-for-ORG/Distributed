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




async function fetchGameStatus() {
  const response = await fetch('/startGame', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
  });
  const result = await response.json();
  if (result.isSuccess) {
    console.log('Success : ' + result.message);
    error.innerText = 'Game Starting in 3 seconds';
    error.style.display = 'block';
    setTimeout(() => {
      window.location.href = '/game';
    }, 3000);
  } else {
    console.log('Failure : ' + result.message);
    error.innerText = 'Failure : ' + result.message
    window.location.href = '/lobby';
  }
}

setInterval(fetchGameStatus, 3000);



