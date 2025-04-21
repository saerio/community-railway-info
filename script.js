async function loadTrainLines() {
    const response = await fetch('./lines.json');
    const lines = await response.json();

    const container = document.getElementById('lines-container');
    container.innerHTML = ''; // clear existing content

    let noticesText = '';
    lines.forEach((line) => {
        if (line.notice) {
            noticesText += `${line.name}: ${line.notice}\n`; // Format with the line name
        }
    });


    // If there are any notices, add them to the existing notice div
    if (noticesText) {
        const noticeElement = document.querySelector('.notice');
        noticeElement.textContent = `NOTICE: ${noticesText}`;
    }

    // Create a wrapper for the status board
    const statusBoard = document.createElement('div');
    statusBoard.className = 'status-board';

    lines.forEach(line => {
        const lineElement = document.createElement('div');
        lineElement.className = 'line';

        // Create the line name element
        const lineName = document.createElement('div');
        lineName.className = 'line-name';
        lineName.textContent = line.name;

        // Create the status element
        const statusElement = document.createElement('div');
        statusElement.className = `status ${line.status.toLowerCase().replace(/\s+/g, '-')}`;

        // Set up the icon and status text based on the line status
        let icon = '';
        switch (line.status) {
            case 'Running':
                icon = 'https://img.icons8.com/color/48/000000/checked--v1.png';
                break;
            case 'Delayed':
                icon = 'https://img.icons8.com/color/48/000000/error--v1.png';
                break;
            case 'Cancelled':
                icon = 'https://img.icons8.com/color/48/000000/cancel--v1.png';
                break;
            case 'Maintenance':
                icon = 'https://img.icons8.com/color/48/000000/maintenance.png';
                break;
            default:
                icon = '';
        }

        // Add icon and status text to the status element
        const iconElement = document.createElement('img');
        iconElement.src = icon;
        iconElement.className = 'status-icon';
        iconElement.alt = `${line.status} Icon`;

        statusElement.appendChild(iconElement);
        statusElement.appendChild(document.createTextNode(line.status));

        // Append elements to the line element
        lineElement.appendChild(lineName);
        lineElement.appendChild(statusElement);

        // Append the line element to the status board
        statusBoard.appendChild(lineElement);
    });

    // Append the status board to the container
    container.appendChild(statusBoard);
}

loadTrainLines();
