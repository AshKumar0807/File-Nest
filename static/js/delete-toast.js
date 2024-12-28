
let currentFolderId = null;
let deleteForm = null;
let isDeleting = false;

//show_toast
function showDeleteToast(folderId, form) {
    if (isDeleting) return;
    currentFolderId = folderId;
    deleteForm = form;
    const deleteToast = document.getElementById('deleteToast');
    deleteToast.classList.remove('translate-x-full');
    deleteToast.classList.add('translate-x-0');
}

//close_toast
function closeToast() {
    const deleteToast = document.getElementById('deleteToast');
    deleteToast.classList.remove('translate-x-0');
    deleteToast.classList.add('translate-x-full');
    currentFolderId = null;
    deleteForm = null;
}

//show_status_toast
function showStatusToast(message, isError = false) {
    const toast = document.createElement('div');
    toast.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg transform transition-all duration-300 z-50 ${isError ? 'bg-red-500' : 'bg-green-500'
        } text-white`;
    toast.textContent = message;
    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.transform = 'translateX(0)';
    }, 100);

    setTimeout(() => {
        toast.style.transform = 'translateX(100%)';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

//delete_confirmation
async function handleDelete() {
    if (!deleteForm || isDeleting) return;
    isDeleting = true;

    try {
        const response = await fetch(deleteForm.action, {
            method: 'POST',
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            },
            credentials: 'same-origin'
        });

        const data = await response.json();

        if (response.ok) {
            showStatusToast(data.message || 'Folder deleted successfully');
            const folderElement = deleteForm.closest('.folder-item');
            if (folderElement) {
                folderElement.remove();
            } else {
                window.location.reload();
            }
        } else {
            showStatusToast(data.error || 'Failed to delete folder', true);
        }
    } catch (error) {
        showStatusToast('An error occurred while deleting the folder', true);
    } finally {
        isDeleting = false;
        closeToast();
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const confirmDeleteBtn = document.getElementById('confirmDelete');
    if (confirmDeleteBtn) {
        confirmDeleteBtn.addEventListener('click', handleDelete);
    }

    document.querySelectorAll('.delete-folder-form').forEach(form => {
        form.querySelector('button[type="submit"]').addEventListener('click', (e) => {
            e.preventDefault();
            const folderId = form.action.split('/').pop();
            showDeleteToast(folderId, form);
        });
    });
});

//close_toast_on_escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        closeToast();
    }
});