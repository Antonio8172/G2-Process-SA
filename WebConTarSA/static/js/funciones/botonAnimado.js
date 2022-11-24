var addProduct1 = document.getElementById('add-product-1'),
    btnCopy1 = document.getElementById('btn-copy-1'),
    btnCerrar1 = document.getElementById('btn-cerrar-1');

btnCopy1.addEventListener('click', function(){
    addProduct1.classList.add('open');
});

btnCerrar1.addEventListener('click', function(){
    addProduct1.classList.remove('open');
});

var addProduct2 = document.getElementById('add-product-2'),
    btnCopy2 = document.getElementById('btn-copy-2'),
    btnCerrar2 = document.getElementById('btn-cerrar-2');

btnCopy2.addEventListener('click', function(){
    addProduct2.classList.add('open');
});

btnCerrar2.addEventListener('click', function(){
    addProduct2.classList.remove('open');
});