document.querySelector('.reg').addEventListener('click', function(){
    document.querySelector('.rega').classList.toggle('open');
});

document.querySelector('.areg').addEventListener('click', function(){
    document.querySelector('.rega').classList.toggle('open');
    document.querySelector('.loga').classList.remove('open');
});

document.querySelector('.to-close').addEventListener('click', function(){
    document.querySelector('.rega').classList.toggle('open');
});

document.querySelector('.lets').addEventListener('click', function(){
    document.querySelector('.rega').classList.toggle('open');
});

document.querySelector('.log').addEventListener('click', function(){
    document.querySelector('.loga').classList.toggle('open');
});

document.querySelector('.alog').addEventListener('click', function(){
    document.querySelector('.loga').classList.toggle('open');
    document.querySelector('.rega').classList.remove('open');
});

document.querySelector('.closelog').addEventListener('click', function(){
    document.querySelector('.loga').classList.toggle('open');
});

