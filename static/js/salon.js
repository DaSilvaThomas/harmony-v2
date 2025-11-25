// Gestion de l'auto-scroll des messages
document.addEventListener('DOMContentLoaded', function() {
    const messagesContainer = document.getElementById('messages-container');
    
    if (messagesContainer) {
        // Scroll vers le bas au chargement
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Scroll vers le bas après chaque mise à jour HTMX
        messagesContainer.addEventListener('htmx:afterSwap', function() {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        });
    }
});

// Gestion du formulaire de message
document.addEventListener('htmx:afterRequest', function(event) {
    if (event.detail.elt.tagName === 'FORM') {
        // Réinitialiser le formulaire après envoi
        event.detail.elt.reset();
    }
});