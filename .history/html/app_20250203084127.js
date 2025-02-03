// URL for API
const API_URL = 'http://127.0.0.1:5000';

// Create a new page
document.getElementById('createPageForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const pageName = document.getElementById('pageName').value;

    if (pageName) {
        const response = await fetch(`${API_URL}/pages`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: pageName }),
        });

        const data = await response.json();

        if (response.ok) {
            alert(`Page '${pageName}' created successfully!`);
            loadPageSelect(); // Reload page select dropdown
        } else {
            alert('Error creating page');
        }
    }
});

// Upload images to a page
document.getElementById('uploadImagesForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const pageId = document.getElementById('pageId').value;
    const images = document.getElementById('images').files;

    if (pageId && images.length > 0) {
        const formData = new FormData();
        formData.append('page_id', pageId);
        for (const image of images) {
            formData.append('images', image);
        }

        const response = await fetch(`${API_URL}/pages/images`, {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();

        if (response.ok) {
            alert('Images uploaded successfully!');
            loadPageImages(pageId); // Reload images for the selected page
        } else {
            alert('Error uploading images');
        }
    }
});

// Load pages into the page selector
async function loadPageSelect() {
    const response = await fetch(`${API_URL}/pages`);
    const data = await response.json();

    const pageSelect = document.getElementById('pageId');
    pageSelect.innerHTML = ''; // Clear existing options

    data.pages.forEach(page => {
        const option = document.createElement('option');
        option.value = page.id;
        option.textContent = page.name;
        pageSelect.appendChild(option);
    });
}

// Load images for a specific page
async function loadPageImages(pageId) {
    const response = await fetch(`${API_URL}/pages/${pageId}/images`);
    const data = await response.json();

    const imagesContainer = document.getElementById('imagesContainer');
    imagesContainer.innerHTML = ''; // Clear existing images

    data.images.forEach(image => {
        const img = document.createElement('img');
        img.src = `data:image/jpeg;base64,${image.file_data}`;
        imagesContainer.appendChild(img);
    });
}

// Initial loading of pages and images
loadPageSelect();
