function form_fetch(){
    f_orm = document.getElementById("form_query");
    formData = new FormData(f_orm);
    const csrfToken = formData.get('csrfmiddlewaretoken');
    const url = f_orm.action;   
    

    fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status == 'success') {
            document.getElementById("dv_data").innerHTML = data.table;
        } else {
            alert(data.message);
        }
    })




}