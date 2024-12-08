document.addEventListener('click', function(event) {
    const x = event.clientX;
    const y = event.clientY;

    if (event.target.tagName === 'A' || 
        event.target.tagName === 'BUTTON' || 
        event.target.tagName === 'AREA' || 
        event.target.getAttribute('role') === 'link') {
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
            console.log(`Clicked at x: ${x}, y: ${y} on ${event.target.tagName}`);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    } 
});