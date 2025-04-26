function fetchLines() {
    let linesData = [];
    fetch('/lines.json')
        .then(response => response.json())
        .then(linesArray => {
            linesData = linesArray;
            const lines = {};
            linesArray.forEach(line => {
                lines[line.name] = line.color;
            });

            document.querySelectorAll('.line-item').forEach(element => {
                const lineName = element.dataset.line;
                if (lines[lineName]) {
                    element.style.backgroundColor = lines[lineName];
                }
            });

            const modal = document.getElementById("modal");
            const modalContent = document.getElementById("modal-inner");

            document.querySelectorAll(".line").forEach(lineElement => {
                lineElement.addEventListener("click", () => {
                    const clickedLineName = lineElement.dataset.line;
                    const lineData = linesData.find(line => line.name === clickedLineName);

                    if (lineData) {
                        const statusEmoji = (() => {
                            switch(lineData.status) {
                                case 'Running': return '✅';
                                case 'Possible delays': return '⚠️';
                                case 'No scheduled service': return '🌙';
                                case 'Suspended': return '🚫';
                                default: return '';
                            }
                        })();

                        modalContent.innerHTML = `
                            <div style="display: flex; align-items: center">
                                <h1 class="line-modal" style="background-color: ${lineData.color}">${lineData.name}</h1>
                                <span style="margin-left: 16px">${lineData.operator || ''}</span>
                            </div>
                            <h3>${statusEmoji} ${lineData.status || 'No description available'}</h3>
                            <p>${lineData.notice || 'No notice available'}</p>
                            <hr>
                        `;

                        if (!lineData.stations || lineData.stations.length === 0) {
                            modalContent.innerHTML += `<p>Station list not available</p>`;
                        } else {
                            modalContent.innerHTML += `<h2>Stations</h2>`;
                            const ul = document.createElement("ul");
                            lineData.stations.forEach(station => {
                                const li = document.createElement("li");
                                if (station.includes('<del>')) {
                                    li.innerHTML = station;
                                } else {
                                    li.textContent = station;
                                }
                                ul.appendChild(li);
                            });
                            modalContent.appendChild(ul);
                        }

                        modal.style.display = "block";
                        document.body.classList.add('blur');
                        setTimeout(() => {
                            modal.classList.add('show');
                        }, 10);
                    }
                });
            });

            document.getElementById("close").onclick = () => {
                closeModal();
            };

            window.onclick = (event) => {
                if (event.target == modal) {
                    closeModal();
                }
            };

            window.addEventListener('keydown', (event) => {
                if (event.key === "Escape") {
                    closeModal();
                }
            });

            function closeModal() {
                modal.classList.remove('show');
                setTimeout(() => {
                    modal.style.display = "none";
                }, 300);
            }
        })
        .catch(error => {
            console.error('Error fetching lines:', error);
        });
}