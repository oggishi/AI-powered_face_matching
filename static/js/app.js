// API Base URL
const API_BASE = '/api';

// Loading Modal Management - DISABLED
function showLoading() {
    // Disabled - no loading modal
}

function hideLoading() {
    // Disabled - no loading modal
}

// Show Alert
function showAlert(message, type = 'success', targetId = null) {
    const alertClass = type === 'success' ? 'message-success' : 'message-error';
    const iconClass = type === 'success' ? 'bi-check-circle-fill' : 'bi-exclamation-triangle-fill';
    
    const alertHTML = `
        <div class="${alertClass} fade-in">
            <i class="bi ${iconClass}"></i> ${message}
        </div>
    `;
    
    if (targetId) {
        document.getElementById(targetId).innerHTML = alertHTML;
    }
}

// Load Statistics
async function loadStats() {
    try {
        const response = await fetch(`${API_BASE}/stats`);
        const data = await response.json();
        
        if (data.success) {
            document.getElementById('totalFaces').textContent = data.stats.total_faces;
            document.getElementById('totalSearches').textContent = data.stats.total_searches;
        }
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Image Preview Handler
function setupImagePreview(inputId, previewId) {
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    
    input.addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                preview.src = e.target.result;
                preview.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });
}

// Detect Face Form
document.getElementById('detectForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('detectImage');
    const file = fileInput.files[0];
    
    if (!file) {
        showAlert('Please select an image', 'error', 'detectResult');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/detect-face`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayDetectionResult(data);
        } else {
            showAlert(data.detail || 'Error detecting faces', 'error', 'detectResult');
        }
    } catch (error) {
        console.error('Error detecting faces:', error);
        showAlert('Error: ' + error.message, 'error', 'detectResult');
    } finally {
        hideLoading();
    }
});

// Display Detection Result
function displayDetectionResult(data) {
    const resultDiv = document.getElementById('detectResult');
    
    let html = `
        <div class="detection-info fade-in">
            <h4><i class="bi bi-people-fill"></i> ${data.num_faces}</h4>
            <p class="mb-0">${data.message}</p>
        </div>
    `;
    
    if (data.num_faces > 0 && data.detected_image) {
        html += `
            <div class="text-center">
                <img src="/${data.detected_image}" class="img-preview fade-in" alt="Detected faces">
                <p class="mt-2 text-muted">
                    <i class="bi bi-info-circle"></i> 
                    Faces detected: ${data.num_faces}
                </p>
            </div>
        `;
    } else {
        html += `
            <div class="empty-state">
                <i class="bi bi-emoji-frown"></i>
                <p>No faces detected in the image</p>
            </div>
        `;
    }
    
    resultDiv.innerHTML = html;
}

// Add Face Form
document.getElementById('addForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('addImage');
    const name = document.getElementById('personName').value;
    const description = document.getElementById('personDescription').value;
    
    if (!fileInput.files[0]) {
        showAlert('Please select an image', 'error', 'addResult');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('name', name);
    if (description) {
        formData.append('description', description);
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/add-face`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            showAlert(data.message, 'success', 'addResult');
            // Reset form
            document.getElementById('addForm').reset();
            document.getElementById('addPreview').style.display = 'none';
            // Reload stats
            loadStats();
        } else {
            showAlert(data.detail || 'Error adding face', 'error', 'addResult');
        }
    } catch (error) {
        console.error('Error adding face:', error);
        showAlert('Error: ' + error.message, 'error', 'addResult');
    } finally {
        hideLoading();
    }
});

// Search Face Form
document.getElementById('searchForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('searchImage');
    const topK = document.getElementById('topK').value;
    
    if (!fileInput.files[0]) {
        showAlert('Please select an image', 'error', 'searchResults');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    formData.append('top_k', topK);
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/search-face`, {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            displaySearchResults(data);
            loadStats();
        } else {
            showAlert(data.detail || 'Error searching face', 'error', 'searchResults');
        }
    } catch (error) {
        console.error('Error searching face:', error);
        showAlert('Error: ' + error.message, 'error', 'searchResults');
    } finally {
        hideLoading();
    }
});

// Display Search Results
function displaySearchResults(data) {
    const resultsDiv = document.getElementById('searchResults');
    
    if (data.num_results === 0) {
        resultsDiv.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-search"></i>
                <p>No matching faces found in database</p>
            </div>
        `;
        return;
    }
    
    let html = `
        <div class="mb-3">
            <strong><i class="bi bi-info-circle"></i> Found ${data.num_results} matching face(s)</strong>
        </div>
    `;
    
    data.results.forEach((result, index) => {
        const matchClass = result.is_match ? 'match-true' : 'match-false';
        const matchText = result.is_match ? 'Match' : 'No Match';
        const confidence = result.confidence;
        
        html += `
            <div class="result-card fade-in">
                <div class="row align-items-center">
                    <div class="col-md-3 text-center">
                        <img src="/${result.face.image_path}" class="result-image" alt="${result.face.name}">
                    </div>
                    <div class="col-md-9">
                        <h5 class="mb-2">
                            ${result.face.name}
                            <span class="match-badge ${matchClass}">${matchText}</span>
                        </h5>
                        <p class="text-muted mb-2">${result.face.description || 'No description'}</p>
                        
                        <div class="mb-2">
                            <strong>Confidence:</strong>
                            <div class="confidence-bar mt-1">
                                <div class="confidence-fill" style="width: ${confidence}%">
                                    ${confidence.toFixed(2)}%
                                </div>
                            </div>
                        </div>
                        
                        <small class="text-muted">
                            <i class="bi bi-ruler"></i> Distance: ${result.distance.toFixed(4)}
                        </small>
                    </div>
                </div>
            </div>
        `;
    });
    
    resultsDiv.innerHTML = html;
}

// Load All Faces
async function loadFaces() {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/faces`);
        const data = await response.json();
        
        if (response.ok && data.success) {
            displayFaces(data.faces);
        } else {
            showAlert('Error loading faces', 'error', 'facesList');
        }
    } catch (error) {
        console.error('Error loading faces:', error);
        showAlert('Error: ' + error.message, 'error', 'facesList');
    } finally {
        // Always hide loading, no matter what
        hideLoading();
    }
}

// Display Faces
function displayFaces(faces) {
    const facesDiv = document.getElementById('facesList');
    
    if (faces.length === 0) {
        facesDiv.innerHTML = `
            <div class="empty-state">
                <i class="bi bi-database-x"></i>
                <p>No faces in database yet</p>
                <button class="btn btn-primary" onclick="document.getElementById('add-tab').click()">
                    <i class="bi bi-plus-circle"></i> Add First Face
                </button>
            </div>
        `;
        return;
    }
    
    let html = `<div class="mb-3"><strong><i class="bi bi-people"></i> Total: ${faces.length} face(s)</strong></div>`;
    
    faces.forEach(face => {
        const createdDate = new Date(face.created_at).toLocaleString('vi-VN');
        
        html += `
            <div class="face-card fade-in">
                <img src="/${face.image_path}" class="face-card-img" alt="${face.name}">
                <div class="face-card-info">
                    <h6 class="mb-1">${face.name}</h6>
                    <p class="text-muted mb-1 small">${face.description || 'No description'}</p>
                    <small class="text-muted">
                        <i class="bi bi-calendar"></i> ${createdDate}
                    </small>
                </div>
                <div class="face-card-actions">
                    <button class="btn btn-sm btn-danger" onclick="deleteFace(${face.id}, '${face.name}')">
                        <i class="bi bi-trash"></i> Delete
                    </button>
                </div>
            </div>
        `;
    });
    
    facesDiv.innerHTML = html;
}

// Delete Face
async function deleteFace(faceId, faceName) {
    if (!confirm(`Are you sure you want to delete ${faceName}?`)) {
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/faces/${faceId}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (response.ok && data.success) {
            loadFaces();
            loadStats();
        } else {
            alert('Error deleting face: ' + (data.detail || 'Unknown error'));
        }
    } catch (error) {
        console.error('Error deleting face:', error);
        alert('Error: ' + error.message);
    } finally {
        hideLoading();
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Setup image previews
    setupImagePreview('detectImage', 'detectPreview');
    setupImagePreview('addImage', 'addPreview');
    setupImagePreview('searchImage', 'searchPreview');
    
    // Load initial stats
    loadStats();
    
    // Load faces when manage tab is shown
    document.getElementById('manage-tab').addEventListener('click', loadFaces);
    
    // Stats button
    document.getElementById('statsBtn').addEventListener('click', function(e) {
        e.preventDefault();
        loadStats();
    });
});
