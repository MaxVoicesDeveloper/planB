document.querySelector('.to-open-send').addEventListener('click', function(){
    document.querySelector('.send').classList.toggle('open');
});

document.querySelector('.closesend').addEventListener('click', function(){
    document.querySelector('.send').classList.toggle('open');
});

document.querySelector('.closesendbut').addEventListener('click', function(){
    document.querySelector('.send').classList.toggle('open');
});

function openEditForm(login, name, email) {
    // Заполнение полей формы редактирования
    document.getElementById('edit-login').value = login;
    document.getElementById('edit-name').value = name;
    document.getElementById('edit-email').value = email;
    // Показ формы редактирования
    document.getElementById('edit-form').style.display = 'block';
}
