// ------------------------ track mouse events --------------------------

// Função para enviar dados de interação para o servidor
function sendInteractionData(data) {
    fetch('/track_interaction', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
}

// Capturando eventos de clique
document.addEventListener('click', function(event) {
    const data = {
        event: 'click',
        x: event.clientX,
        y: event.clientY,
        timestamp: Date.now()
    };
    sendInteractionData(data);
});

// Capturando movimentos do mouse
document.addEventListener('mousemove', function(event) {
    const data = {
        event: 'mousemove',
        x: event.clientX,
        y: event.clientY,
        timestamp: Date.now()
    };
    sendInteractionData(data);
});

// Capturando eventos de rolagem
document.addEventListener('scroll', function(event) {
    const data = {
        event: 'scroll',
        scrollX: window.scrollX,
        scrollY: window.scrollY,
        timestamp: Date.now()
    };
    sendInteractionData(data);
});
