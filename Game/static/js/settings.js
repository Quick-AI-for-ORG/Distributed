const error = document.getElementById('error-message');
error.style.display = 'none';

let checkboxes = document.querySelectorAll('input[type="checkbox"]');
let radios = document.querySelectorAll('input[type="radio"]');


const form = document.querySelector('form');
form.addEventListener('submit', async (event) => {
    event.preventDefault();

    let selectedPacks = [];
    for (let checkbox of checkboxes) {
      if (checkbox.checked) {
        selectedPacks.push(checkbox.value);
      }
    }
    if (selectedPacks.length === 0) {
        for (let checkbox of checkboxes) {
            selectedPacks.push(checkbox.value);
        }
    }
    let selectedDuration = null;
    for (let radio of radios) {
      if (radio.checked) {
        selectedDuration = radio.value;
        break;
      }
    }


    const response = await fetch('/createGame', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            wordPacks: selectedPacks,
            duration: selectedDuration
        }),
    })
        
    const result = await response.json();

    if (result.isSuccess) {
        console.log('Success : ' + result.message);
        window.location.href = '/lobby';
    } else {
        console.log('Failure : ' + result.message);
       
        error.innerText = 'Failure : ' + result.message
        error.style.display = 'block';
      }
});
