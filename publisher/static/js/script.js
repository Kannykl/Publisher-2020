function ajaxSend(url, params) {
    // Отправляем запрос
    fetch(`${url}?${params}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
    })
        .then(response => response.json())
        .then(json => ren(json))
        .catch(error => console.error(error))
}

const forms = document.querySelector('form[name=search]');

forms.addEventListener('submit', function (e) {
    // Получаем данные из формы
    e.preventDefault();
    let url = this.action;
    let params = new URLSearchParams(new FormData(this)).toString();
    ajaxSend(url, params);
});

function ren(data) {
    // Рендер шаблона
    let  template = Hogan.compile(html);
    let output = template.render(data);
    const table = document.querySelector('tbody')
    table.innerHTML = output;
}

var html = '\
{{#publications}}\
    <tr>\
        <td>\
            {{#authors}}\
                {{authors__military_rank}}\
            {{/authors}}\
        </td>\
        <td>\
            {{authors}}\
        </td>\
        <td>\
            {{authors__work_position}}\
        </td>\
        <td>\
            {{title}}\
        </td>\
        <td>\
            {{edition}}\
        </td>\
        <td>\
            {{published_year}}\
        </td>\
        <td>\
            {{type_of_publication}}\
        </td>\
        <td>\
            {{range}}\
        </td>\
        <td>\
            {{uk_number}}\
        </td>\
    </tr>\
{{/publications}}'
