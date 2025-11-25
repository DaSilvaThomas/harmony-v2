// Gestion du quiz avec timer optionnel
document.addEventListener('DOMContentLoaded', function() {
    // Animation des boutons de réponse
    const answerButtons = document.querySelectorAll('button[name="answer"]');
    
    answerButtons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(8px)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
});