document.querySelector('.to-close-setting').addEventListener('click', function(){
    document.querySelector('.setting').classList.toggle('open');
});

document.querySelector('.to-open-setting').addEventListener('click', function(){
    document.querySelector('.setting').classList.toggle('open');
});


document.querySelector('.to-close-add-org').addEventListener('click', function(){
    document.querySelector('.add-org').classList.toggle('open-org');
});

document.querySelector('.to-open-add-org').addEventListener('click', function(){
    document.querySelector('.add-org').classList.toggle('open-org');
});

document.getElementById('profilePictureInput').onchange = function(event) {
    var reader = new FileReader();
    reader.onload = function() {
        var output = document.getElementById('preview-image');
        output.src = reader.result;
        output.style.display = 'block';
    };
    reader.readAsDataURL(event.target.files[0]);
};