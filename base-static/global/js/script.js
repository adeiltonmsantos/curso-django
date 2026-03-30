document.addEventListener('DOMContentLoaded', () => {
    
    forms = document.querySelectorAll('.form-delete')
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