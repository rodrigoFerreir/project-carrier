
document.getElementById("upload-button").onclick(() => {
    console.log("Clicou no botão de upload");
})

document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('file-input');
    const fileName = document.getElementById('file-name');

    fileInput.addEventListener('click', function () {
        if (fileInput.files.length > 0) {
            fileName.textContent = fileInput.files[0].name;
        } else {
            fileName.textContent = 'Nenhum arquivo selecionado';
        }
    });
});