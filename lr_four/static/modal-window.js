class ModalManager {
    constructor() {
        this.messageModal = new bootstrap.Modal(document.getElementById('messageModal'));
        this.confirmCallback = null
    }

    showMessage(msg, type='info') {
        const modalHeader = document.getElementById('modalHeader')
        const modalBody = document.getElementById('modalMessage')

        modalBody.textContent = msg
        modalHeader.className = 'modal-header'
        switch(type) {
            case 'success':
                modalHeader.classList.add('bg-success', 'text-white')
                document.getElementById('messageModalLabel').textContent = 'Успех!';
                break
            case 'danger':
            case 'error':
                modalHeader.classList.add('bg-danger', 'text-white')
                document.getElementById('messageModalLabel').textContent = 'Ошибка!';
                break
            case 'warning':
                modalHeader.classList.add('bg-warning', 'text-black')
                document.getElementById('messageModalLabel').textContent = 'Нет доступа!'
                break
            case 'confirm':
                modalHeader.classList.add('bg-danger', 'text-white')
                document.getElementById('messageModalLabel').textContent = 'Подтверждение';
                const btn_confirm = document.createElement('button')
                btn_confirm.type = 'button'
                btn_confirm.classList.add('btn', 'btn-success')
                btn_confirm.textContent = 'Да'
                btn_confirm.onclick = () => {
                    if (this.confirmCallback()) {
                        this.confirmCallback()
                    }
                    this.messageModal.hide()
                };

                document.getElementById('btn_close_confirm').textContent = 'Нет'
                document.getElementById('modalFooter').prepend(btn_confirm)
                break
            
            default:
                modalHeader.classList.add('bg-primary', 'text-white')
                document.getElementById('messageModalLabel').textContent = 'Информация';
        }

        this.messageModal.show()
    }

    showFlashMessage() {
        const flashData = document.getElementById('flash-data')
        if (flashData) {
            try {
                const messages = JSON.parse(flashData.dataset.messages || '[]')
                if (messages.length > 0) {
                    const [category, message] = messages[messages.length - 1]
                    this.showMessage(message, category)
                }
            }
            catch (e) {
                console.error('Flash error', e)
            }
        }
    }

    confirm(msg, callback) {
        this.confirmCallback = callback
        this.showMessage(msg, 'confirm')

    }
}

document.addEventListener('DOMContentLoaded', function() {
    window.ModalManager = new ModalManager()
    window.ModalManager.showFlashMessage()
})