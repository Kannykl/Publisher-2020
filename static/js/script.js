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
        </td>\
        <td>\
            <a href="/publisher/publication_info/{{id}}">{{title}}</a>\
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
        <td>\
        <a class="btn-secondary btn-sm mt-1 mb-1" href="/publisher/update_publication/{{id}}">\
        <img src="/static/publisher/images/update_picture.jpg" width="20" height="20">\
        </a>\
        </td>\
        <td>\
        <a class="btn-secondary btn-sm mt-1 mb-1" href="/publisher/delete_publication/{{id}}">\
        <img src="/static/publisher/images/delete_picture.png" width="20" height="20">\
        </a>\
        </td>\
    </tr>\
{{/publications}}'
