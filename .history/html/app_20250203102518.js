// URL for API
const API_URL = 'https://nffco-images.onrender.com';

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

// Load pages into the page selector (dropdown)
async function loadPageSelect() {
    const response = await fetch(`${API_URL}/pages`);
    const data = await response.json();

    const pageSelect = document.getElementById('pageId');
    pageSelect.innerHTML = ''; // Clear existing options

    // Add default "Select Page" option
    const defaultOption = document.createElement('option');
    defaultOption.textContent = "Select Page";
    pageSelect.appendChild(defaultOption);

    data.pages.forEach(page => {
        const option = document.createElement('option');
        option.value = page.id;
        option.textContent = page.name;
        pageSelect.appendChild(option);
    });
}

// Load images for all pages
async function loadAllPagesImages() {
    const response = await fetch(`${API_URL}/pages`);
    const data = await response.json();

    const imagesContainer = document.getElementById('imagesContainer');
    imagesContainer.innerHTML = ''; // Clear existing images

    // Iterate through each page and fetch its images
    for (const page of data.pages) {
        const pageResponse = await fetch(`${API_URL}/pages/${page.id}/images`);
        const pageData = await pageResponse.json();

        const pageSection = document.createElement('div');
        pageSection.classList.add('page-section'); // Add class for styling

        const pageTitle = document.createElement('h3');
        pageTitle.textContent = page.name;
        pageSection.appendChild(pageTitle);

        // Display images for this page
        pageData.images.forEach(image => {
            const img = document.createElement('img');
            img.src = `data:image/jpeg;base64,${image.file_data}`;
            img.alt = image.filename;
            pageSection.appendChild(img);
        });

        imagesContainer.appendChild(pageSection);
    }
}

// Initial loading of pages and images
loadAllPagesImages();



// Initial loading of pages and images
loadPageSelect();


document.addEventListener('DOMContentLoaded', () => {
    const pageId = 1;  // You can change this to the actual page ID you want to fetch
    const pageNameElement = document.getElementById('page-name');
    const imagesContainer = document.getElementById('images-container');

    // Fetch the page and images from the Flask API
    fetch(`http://127.0.0.1:5000/pages/${pageId}/images`)
        .then(response => response.json())
        .then(data => {
            const { page_name, images } = data;

            // Set the page name
            pageNameElement.textContent = page_name;

            // Display images
            images.forEach(image => {
                const imgElement = document.createElement('img');
                imgElement.src = `data:image/jpeg;base64,${image.file_data}`;
                imgElement.alt = image.filename;
                imgElement.classList.add('image-item');
                imagesContainer.appendChild(imgElement);
            });
        })
        .catch(error => {
            console.error('Error fetching page images:', error);
            pageNameElement.textContent = 'Failed to load page';
        });
});
