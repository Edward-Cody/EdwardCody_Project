
document.addEventListener('click', function(event) {
    const x = event.clientX;
    const y = event.clientY;

    if (event.target.tagName === 'A') {
        const url = event.target.href;

        fetch('http://localhost:3000/new_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url, x: x, y: y }) // Include cursor position
        })
        .then(response => response.json())
        .then(data => {
            //console.log('Response from server:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } 
});