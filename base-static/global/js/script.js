document.addEventListener('DOMContentLoaded', () => {
    
    forms = document.querySelectorAll('.delete-form')
    forms.forEach(form => {
        form.addEventListener('submit', e => {
            e.preventDefault()
            const confirma = confirm('Deseja realmente excluir a receita?')
            if(confirma){
                form.submit()
            }
        })
    });

})