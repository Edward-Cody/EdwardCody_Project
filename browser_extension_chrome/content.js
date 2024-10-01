let lastTimestamp = null;
let timeDiff = 100; // 

document.addEventListener('mousemove', function(event) {
    const x = event.clientX;
    const y = event.clientY;
    const currentTimestamp = Date.now();
    
    console.log(lastTimestamp, currentTimestamp, currentTimestamp - lastTimestamp);
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
    if (event.target.tagName === 'A') {
        const url = event.target.href;

        fetch('http://localhost:3000/new_url', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ url: url })
        })
        .then(response => response.json())
        .then(data => {
            //console.log('Response from server:', data);
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
    else{
        fetch('http://localhost:3000/click', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            //body: JSON.stringify({ url: url })
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


    
// Create the GUI container
let guiContainer = document.createElement('div');
guiContainer.id = 'custom-gui';

// Set styles to make it overlay the webpage
guiContainer.style.position = 'fixed';
guiContainer.style.top = '20px';
guiContainer.style.right = '20px';
guiContainer.style.zIndex = '10000';  // Make sure it's on top of other elements
guiContainer.style.width = '300px';
guiContainer.style.height = '150px';
guiContainer.style.backgroundColor = 'rgba(255, 255, 255, 0.9)';
guiContainer.style.border = '1px solid #ccc';
guiContainer.style.boxShadow = '0px 0px 10px rgba(0, 0, 0, 0.1)';
guiContainer.style.padding = '10px';
guiContainer.style.fontFamily = 'Arial, sans-serif';

// Create a close button
let closeButton = document.createElement('button');
closeButton.textContent = 'Close';
closeButton.style.position = 'absolute';
closeButton.style.top = '5px';
closeButton.style.right = '5px';
closeButton.onclick = function() {
  document.body.removeChild(guiContainer);
};

// Add the close button to the container
guiContainer.appendChild(closeButton);

// Add some content (e.g., a form or message)
let message = document.createElement('div');
message.textContent = 'Hello, this is your custom GUI!';
message.style.marginTop = '40px';
message.style.textAlign = 'center';
guiContainer.appendChild(message);

// Append the GUI container to the body
document.body.appendChild(guiContainer);
