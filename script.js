async function loadTrainLines() {
  const response = await fetch('./lines.json');
  const lines = await response.json();
  
  const container = document.getElementById('lines-container');
  container.innerHTML = ''; // clear existing content

  const statusBoard = document.createElement('div');
  statusBoard.className = 'status-board';

  lines.forEach(line => {
    const lineElement = document.createElement('div');
    lineElement.className = 'line';

    const lineNameElement = document.createElement('div');
    lineNameElement.className = 'line-name';
    lineNameElement.textContent = line.name;

    const statusElement = document.createElement('div');
    statusElement.className = `status ${line.status.toLowerCase()}`;

    let iconUrl = '';
    let altText = '';

    switch (line.status) {
      case 'On Time':
        iconUrl = 'https://img.icons8.com/color/48/000000/checked--v1.png';
        altText = 'On Time Icon';
        break;
      case 'Delayed':
        iconUrl = 'https://img.icons8.com/color/48/000000/error--v1.png';
        altText = 'Delayed Icon';
        break;
      case 'Cancelled':
        iconUrl = 'https://img.icons8.com/color/48/000000/cancel--v1.png';
        altText = 'Cancelled Icon';
        break;
      case 'Maintenance':
        iconUrl = 'https://img.icons8.com/color/48/000000/maintenance.png';
        altText = 'Maintenance Icon';
        break;
      default:
        iconUrl = '';
        altText = '';
    }

    const statusIcon = document.createElement('img');
    statusIcon.src = iconUrl;
    statusIcon.className = 'status-icon';
    statusIcon.alt = altText;

    statusElement.appendChild(statusIcon);
    statusElement.appendChild(document.createTextNode(line.status));

    lineElement.appendChild(lineNameElement);
    lineElement.appendChild(statusElement);

    if (line.notice) {
      const noticeElement = document.createElement('div');
      noticeElement.className = 'notice';
      noticeElement.textContent = line.notice;
      lineElement.appendChild(noticeElement);
    }

    statusBoard.appendChild(lineElement);
  });

  container.appendChild(statusBoard);
}

loadTrainLines();
console.log("test");
