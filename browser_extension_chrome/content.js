let lastTimestamp = null;
let timeDiff = 250; // milliseconds

document.addEventListener('mousemove', function(event) {
    const x = event.clientX;
    const y = event.clientY;
    const currentTimestamp = Date.now();
    
    console.log(lastTimestamp, currentTimestamp, currentTimestamp - lastTimestamp, x, y); // console message
    if(currentTimestamp - lastTimestamp > timeDiff || lastTimestamp === null) {

    
        lastTimestamp = currentTimestamp;
        fetch('http://localhost:3000/write_coordinates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ x: x, y: y })
        })
        .then(response => response.json())
        .then(data => {
            console.log("*");
        })
        .catch(error => {
            console.error('Error:', error);
        });

    }

    
});

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
    } else {
        fetch('http://localhost:3000/click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ x: x, y: y }) // Include cursor position
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