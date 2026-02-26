document.addEventListener('DOMContentLoaded', function () {
    window.confirmDelete = function(userName) {
        console.log('Удаляем юзера...', userName)
        return flash(`Вы уверены, что хотите удалить пользователя ${userName}?`)
    }
})

