
// Pega os logs do servidor e adiciona na tela dinamicamente no endereço /nothing_here
// atualiza a cada 5 segundos

document.addEventListener('DOMContentLoaded', () => {
    const logContainer = document.getElementById('log-container');

    function addLog(log) {
        const logElement = document.createElement('div');
        logElement.classList.add('log');

        logElement.innerHTML = `
            <div class="log-time">Time: ${log.current_time}</div>
            <div class="log-ip">IP: ${log.user_ip}</div>
            <div class="log-agent">Agent: ${log.user_agent}</div>
            <div class="log-path">Path: ${log.path}</div>
            <div class="log-fingerprint">Fingerprint: ${log.fingerprint}</div>
            <div class="log-coment">Coment: ${log.coment}</div>
        `;

        logContainer.appendChild(logElement);
    }

    // pega os logs do servidor pelo endereço /logs
    function fetchLogs() {
        fetch('/just-logs')
            .then(response => response.json())
            .then(data => {
                logContainer.innerHTML = ''; // Clear existing logs
                data.forEach(log => addLog(log));
            })
            .catch(error => console.error('Error fetching logs:', error));
    }

    // Fetch logs every 5 seconds
    setInterval(fetchLogs, 5000);
    fetchLogs(); // Initial fetch
});
