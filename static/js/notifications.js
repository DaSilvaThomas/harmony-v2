// Gestion du clignotement des notifications
function checkNotifications() {
    fetch('/notifications/check/')
        .then(response => response.json())
        .then(data => {
            const notifIcon = document.querySelector('.notification-icon');
            if (notifIcon) {
                if (data.has_recent) {
                    notifIcon.classList.add('blink');
                } else {
                    notifIcon.classList.remove('blink');
                }
            }
        })
        .catch(error => console.error('Erreur:', error));
}

// Vérifier toutes les 30 secondes
setInterval(checkNotifications, 30000);

// Vérifier au chargement
document.addEventListener('DOMContentLoaded', checkNotifications);