function form_fetch(reset_offset = false) {

    if (reset_offset) {stt_offset.value = 0;}
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

function edit_button(id,event){

    
    alert("Edit function is not implemented yet. id: " + id);
    event.stopPropagation();

}

function delete_button(id,event){

    
    alert("Delete function is not implemented yet. id: " + id);
    event.stopPropagation();

}

function row_click(id,event){
    
    alert("Row click function is not implemented yet. ID: " + id);
    event.stopPropagation();
}