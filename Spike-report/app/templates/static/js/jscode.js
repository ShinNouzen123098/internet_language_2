// 1. Получаем текст из элемента h2
const headerText = document.querySelector('h2').textContent;
console.log('Текст заголовка:', headerText);

// 2. Создаем новый элемент p и добавляем его после h2
const newParagraph = document.createElement('p');
newParagraph.textContent = headerText;
newParagraph.style.fontSize = '24px';
newParagraph.style.color = '#666';
document.querySelector('h2').after(newParagraph);

// 3. Создаем форму с input и button
const form = document.createElement('form');
form.style.marginTop = '20px';
form.style.padding = '20px';
form.style.backgroundColor = '#f8f9fa';

const input = document.createElement('input');
input.type = 'text';
input.placeholder = 'Введите имя латинскими буквами';
input.style.padding = '10px';
input.style.marginRight = '10px';
input.style.border = '1px solid #ddd';
input.style.borderRadius = '4px';
input.style.width = '200px';

const button = document.createElement('button');
button.textContent = 'Проверить';
button.style.padding = '10px 20px';
button.style.backgroundColor = '#e74c3c';
button.style.color = 'white';
button.style.border = 'none';
button.style.borderRadius = '4px';
button.style.cursor = 'pointer';

form.appendChild(input);
form.appendChild(button);
document.querySelector('.contact-form').appendChild(form);

// 4. Добавляем обработчик события для кнопки
button.addEventListener('click', function(e) {
    e.preventDefault();
    const name = input.value;
    const latinRegex = /^[a-zA-Z]+$/;
    
    if (latinRegex.test(name)) {
        alert('Имя введено верно!');
    } else {
        alert('Имя должно содержать только латинские буквы!');
    }
});

// 5. Создаем кнопку для скрытия/показа формы
const toggleButton = document.createElement('button');
toggleButton.textContent = 'Скрыть/Показать форму';
toggleButton.style.marginTop = '20px';
toggleButton.style.padding = '10px 20px';
toggleButton.style.backgroundColor = '#2c3e50';
toggleButton.style.color = 'white';
toggleButton.style.border = 'none';
toggleButton.style.borderRadius = '4px';
toggleButton.style.cursor = 'pointer';

document.querySelector('.contact-form').appendChild(toggleButton);

//Скрытие/показ 
let isFormVisible = true;
toggleButton.addEventListener('click', function() {
    if (isFormVisible) {
        form.style.display = 'none';
    } else {
        form.style.display = 'block';
    }
    isFormVisible = !isFormVisible;
});


