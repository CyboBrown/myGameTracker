document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('overlay').addEventListener('click', closePrompt);
});

function showPrompt(clickedElement) {
    const game_id = clickedElement.getAttribute('game-id');
    console.log(game_id)

    // Fetch details from the server using the entryId and populate the prompt
    fetch(`/get_entry_details/${game_id}/`)
        .then(response => response.json())
        .then(data => {
            // Populate the prompt form with data from the server
            document.getElementById('prompt').querySelector('[name="status"]').value = data.status;
            document.getElementById('prompt').querySelector('[name="rating"]').value = data.rating;
            document.getElementById('prompt').querySelector('[name="review"]').value = data.review;

            document.getElementById('prompt').querySelector('[name="game_id"]').value = game_id;
        })
        .catch(error => {
            console.error('Error fetching entry details:', error);
        });

    document.getElementById('prompt').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';
}

function addRecord(gameId) {
    fetch(`/add_entry/${gameId}/`, {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    })
    .catch(error => {
        console.error('Error adding to user list:', error);
    });

    location.reload();
}

 function editRecord() {
    const prompt = document.getElementById('prompt');
    const game_id = prompt.querySelector('[name="game_id"]').value;
    const status = prompt.querySelector('[name="status"]').value;
    const rating = prompt.querySelector('[name="rating"]').value;
    const review = prompt.querySelector('[name="review"]').value;

    // Perform an AJAX request to update the entry on the server
    fetch(`/update_entry/${game_id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `new_status=${encodeURIComponent(status)}&new_score=${encodeURIComponent(rating)}&new_review=${encodeURIComponent(review)}`,
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Entry updated successfully!');
        } else {
            console.log('Failed to update entry. Please try again.');
        }
    })
    .catch(error => {
        console.error('Error updating entry:', error);
    });

    // Hide the prompt after submitting
    document.getElementById('prompt').style.display = 'none';
    location.reload();
 }

function deleteRecord() {
    const prompt = document.getElementById('prompt');
    const game_id = prompt.querySelector('[name="game_id"]').value;

    // Confirm with the user before proceeding with the deletion
    const confirmDelete = confirm('Are you sure you want to delete this entry?');
    if (confirmDelete) {
        // Perform an AJAX request to delete the entry on the server
        fetch(`/delete_entry/${game_id}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
        })
        .then(response => response.json())
        .then(data => {
            // Handle the response (you may want to show a success message or handle errors)
            if (data.success) {
                alert('Entry deleted successfully!');
            } else {
                alert('Failed to delete entry. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error deleting entry:', error);
        });

        // Hide the prompt after deletion
        document.getElementById('prompt').style.display = 'none';
        location.reload();
    }
}

function closePrompt() {
    document.getElementById('prompt').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';
}

window.onclick = function(event) {
    var dropdownContainers = document.querySelectorAll('.dropdown');
    dropdownContainers.forEach(function(container) {
        var dropdownOptions = container.querySelector('.dropdown-options');
        if (dropdownOptions.style.display === 'block' && !event.target.matches('.generic-form-dropdown') && !event.target.matches('.dropdown-options li')) {
        dropdownOptions.style.display = 'none';
        }
    });
}

function toggleDropdown(input) {
    var dropdownOptions = input.nextElementSibling;
    dropdownOptions.style.display = (dropdownOptions.style.display === 'block') ? 'none' : 'block';
}

// Select an option and populate the input field
function selectOption(option) {
    var inputField = option.parentElement.previousElementSibling;
    inputField.value = option.textContent;
    toggleDropdown(inputField);
}
