function showToast(message) {
    const toaster = document.getElementById('toaster');
    toaster.textContent = message || 'Success';
    toaster.classList.add('show');
    setTimeout(() => {
        toaster.classList.remove('show');
    }, 5000);
}

function startService(service) {
    fetch(`/start/${service}`)
        .then(response => response.json())
        .then(data => {
            showToast(data.message);
            refreshStatus(service);
        });
}

function stopService(service) {
    fetch(`/stop/${service}`)
        .then(response => response.json())
        .then(data => {
            showToast(data.message);
            refreshStatus(service);
        });
}

function refreshStatus(service) {
    fetch(`/status/${service}`)
        .then(response => response.json())
        .then(data => {
            updateStatus(service, data.status);
        });
}

function updateStatus(service, status) {
    const statusElement = document.getElementById(`status-${service}`);
    statusElement.textContent = status;
    statusElement.className = 'status ' + status;
}

// Check status of all services on page load
document.addEventListener('DOMContentLoaded', (event) => {
    const services = document.querySelectorAll('.service');
    services.forEach(service => {
        const serviceName = service.id.replace('service-', '');
        refreshStatus(serviceName);
    });
});