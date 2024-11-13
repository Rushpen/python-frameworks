function toggleEditForm(todoId) {
    const form = document.getElementById(`edit-form-${todoId}`);
    if (form.style.display === 'none' || form.style.display === '') {
        form.style.display = 'block';
    } else {
        form.style.display = 'none';
    }
}