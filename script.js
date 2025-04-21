async function loadTrainLines() {
    try {
      const response = await fetch('./lines.json');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const lines = await response.json();
  
      const container = document.getElementById('lines-container');
      container.innerHTML = ''; // clear existing content
  
      // Mapping for statuses
      const statusMapping = {
        'On Time': { class: 'on-time', icon: '✅' },
        'Delayed': { class: 'delayed', icon: '⚠️' },
        'Cancelled': { class: 'cancelled', icon: '❌' },
        'Maintenance': { class: 'maintenance', icon: '🛠️' }, // New class for maintenance
      };
  
      lines.forEach(line => {
        const lineElement = document.createElement('div');
        lineElement.className = 'line';
  
        const { class: statusClass = '', icon = '' } = statusMapping[line.status] || {};
  
        // Create line header
        const lineHeader = document.createElement('div');
        lineHeader.classList.add('line-header');
  
        const lineName = document.createElement('span');
        lineName.classList.add('line-name');
        lineName.textContent = line.name;
  
        const lineStatus = document.createElement('span');
        lineStatus.classList.add('line-status', statusClass);
        lineStatus.textContent = `${icon} ${line.status}`;
  
        lineHeader.appendChild(lineName);
        lineHeader.appendChild(lineStatus);
  
        // Create line notice
        if (line.notice) {
          const lineNotice = document.createElement('div');
          lineNotice.classList.add('line-notice');
          lineNotice.textContent = line.notice;
          lineElement.appendChild(lineNotice);
        }
  
        // Append line header and notice (if any)
        lineElement.appendChild(lineHeader);
        container.appendChild(lineElement);
      });
    } catch (error) {
      console.error('Error loading train lines:', error);
    }
  }
  
  loadTrainLines();
  console.log("test");
  