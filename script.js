async function loadTrainLines() {
    const response = await fetch('./lines.json');
    const lines = await response.json();

    const suspendedcontainer = document.getElementById('suspended');
    const okcontainer = document.getElementById('running');

    lines.forEach(line => {
        switch (line.status) {
            case "Suspended":
                suspendedcontainer.style.display = "block"
                var newline = document.createElement("span")
                newline.classList.add("line")
                newline.style.backgroundColor = line.color
                newline.innerHTML = "<b style='color: #fff;'>" + line.name + "</b>"
                newline.onclick = function() {
                    alert(line.notice)
                }
                suspendedcontainer.appendChild(newline)
                break;
            case "Running":
                var newline = document.createElement("span")
                newline.classList.add("line")
                newline.style.backgroundColor = line.color
                newline.innerHTML = "<b style='color: #fff;'>" + line.name + "</b>"
                okcontainer.appendChild(newline)
                break;
        
            default:
                console.log(line.name + " has an invalid status")
                break;
        }
    });
}

loadTrainLines();
