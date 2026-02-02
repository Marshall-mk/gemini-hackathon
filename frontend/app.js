const API_URL = 'http://localhost:8000/api';

// DOM Elements
const videoUrlInput = document.getElementById('videoUrl');
const modelSelect = document.getElementById('modelSelect');
const extractBtn = document.getElementById('extractBtn');
const loadingSpinner = document.getElementById('loadingSpinner');
const errorMessage = document.getElementById('errorMessage');
const recipeDisplay = document.getElementById('recipeDisplay');
const recipeGallery = document.getElementById('recipeGallery');
const recipeModal = document.getElementById('recipeModal');
const modalContent = document.getElementById('modalContent');
const closeModal = document.querySelector('.close-modal');

// Event Listeners
extractBtn.addEventListener('click', extractRecipe);
videoUrlInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') extractRecipe();
});
closeModal.addEventListener('click', () => {
    recipeModal.classList.add('hidden');
    recipeModal.style.display = 'none';
});
window.addEventListener('click', (e) => {
    if (e.target === recipeModal) {
        recipeModal.classList.add('hidden');
        recipeModal.style.display = 'none';
    }
});

// Initialize
loadRecipes();

// Functions
async function extractRecipe() {
    const videoUrl = videoUrlInput.value.trim();

    if (!videoUrl) {
        showError('Please enter a video URL');
        return;
    }

    // Validate URL
    if (!videoUrl.includes('instagram.com') && !videoUrl.includes('tiktok.com')) {
        showError('Please enter a valid Instagram or TikTok URL');
        return;
    }

    hideError();
    showLoading(true);
    recipeDisplay.classList.add('hidden');

    // Get selected model
    const selectedModel = modelSelect.value;

    try {
        const response = await fetch(`${API_URL}/recipes/extract`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                video_url: videoUrl,
                model: selectedModel
            })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to extract recipe');
        }

        const data = await response.json();

        if (data.success) {
            displayRecipe(data.recipe);
            videoUrlInput.value = '';
            loadRecipes(); // Refresh gallery
        } else {
            showError(data.message || 'Failed to extract recipe');
        }
    } catch (error) {
        console.error('Error:', error);
        showError(error.message || 'An error occurred while extracting the recipe');
    } finally {
        showLoading(false);
    }
}

function displayRecipe(recipe) {
    const thumbnailUrl = recipe.thumbnail_path ? `http://localhost:8000/${recipe.thumbnail_path}` : '';
    const videoUrl = recipe.video_path ? `http://localhost:8000/${recipe.video_path}` : '';

    let html = `
        <div class="recipe-header">
            <h2 class="recipe-title">${recipe.title || 'Untitled Recipe'}</h2>
            ${videoUrl ? `
                <video controls class="recipe-video">
                    <source src="${videoUrl}" type="video/mp4">
                    Your browser does not support the video tag.
                </video>
            ` : thumbnailUrl ? `<img src="${thumbnailUrl}" alt="${recipe.title}" class="recipe-thumbnail">` : ''}
            ${recipe.description ? `<p class="recipe-description">${recipe.description}</p>` : ''}
        </div>
    `;

    // Nutrition Info
    if (recipe.nutrition) {
        html += `
            <div class="nutrition-section">
                <h3 class="section-title"><i class="fas fa-heart"></i> Nutrition Information</h3>
                <div class="nutrition-grid">
                    ${recipe.nutrition.servings ? `
                        <div class="nutrition-item">
                            <div class="nutrition-label">Servings</div>
                            <div class="nutrition-value">${recipe.nutrition.servings}</div>
                        </div>
                    ` : ''}
                    ${recipe.nutrition.calories ? `
                        <div class="nutrition-item">
                            <div class="nutrition-label">Calories</div>
                            <div class="nutrition-value">${Math.round(recipe.nutrition.calories)}</div>
                        </div>
                    ` : ''}
                    ${recipe.nutrition.protein ? `
                        <div class="nutrition-item">
                            <div class="nutrition-label">Protein</div>
                            <div class="nutrition-value">${recipe.nutrition.protein.toFixed(1)}g</div>
                        </div>
                    ` : ''}
                    ${recipe.nutrition.carbs ? `
                        <div class="nutrition-item">
                            <div class="nutrition-label">Carbs</div>
                            <div class="nutrition-value">${recipe.nutrition.carbs.toFixed(1)}g</div>
                        </div>
                    ` : ''}
                    ${recipe.nutrition.fats ? `
                        <div class="nutrition-item">
                            <div class="nutrition-label">Fats</div>
                            <div class="nutrition-value">${recipe.nutrition.fats.toFixed(1)}g</div>
                        </div>
                    ` : ''}
                    ${recipe.nutrition.fiber ? `
                        <div class="nutrition-item">
                            <div class="nutrition-label">Fiber</div>
                            <div class="nutrition-value">${recipe.nutrition.fiber.toFixed(1)}g</div>
                        </div>
                    ` : ''}
                </div>
            </div>
        `;
    }

    // Ingredients
    if (recipe.ingredients && recipe.ingredients.length > 0) {
        html += `
            <div class="ingredients-section">
                <h3 class="section-title"><i class="fas fa-shopping-basket"></i> Ingredients</h3>
                <ul class="ingredient-list">
                    ${recipe.ingredients.map(ing => `
                        <li class="ingredient-item">
                            <i class="fas fa-check-circle ingredient-icon"></i>
                            <div class="ingredient-details">
                                <div class="ingredient-name">${ing.name}</div>
                                ${ing.quantity || ing.unit ? `
                                    <div class="ingredient-quantity">${ing.quantity || ''} ${ing.unit || ''}</div>
                                ` : ''}
                            </div>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
    }

    // Cooking Steps
    if (recipe.steps && recipe.steps.length > 0) {
        html += `
            <div class="steps-section">
                <h3 class="section-title"><i class="fas fa-list-ol"></i> Cooking Instructions</h3>
                <div class="step-list">
                    ${recipe.steps.map(step => `
                        <div class="step-item">
                            <div class="step-header">
                                <div class="step-number">${step.step_number}</div>
                                ${step.duration ? `<div class="step-duration"><i class="fas fa-clock"></i> ${step.duration}</div>` : ''}
                            </div>
                            <div class="step-instruction">${step.instruction}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
    }

    // Actions
    html += `
        <div class="recipe-actions">
            <button class="action-btn btn-success" onclick="viewGroceryList(${recipe.id})">
                <i class="fas fa-shopping-cart"></i> Grocery List
            </button>
            <button class="action-btn btn-primary" onclick="exportJSON(${recipe.id})">
                <i class="fas fa-file-code"></i> Export JSON
            </button>
            <button class="action-btn btn-info" onclick="exportPDF(${recipe.id})">
                <i class="fas fa-file-pdf"></i> Export PDF
            </button>
        </div>
    `;

    recipeDisplay.innerHTML = html;
    recipeDisplay.classList.remove('hidden');
    recipeDisplay.scrollIntoView({ behavior: 'smooth' });
}

async function loadRecipes() {
    try {
        const response = await fetch(`${API_URL}/recipes`);
        const recipes = await response.json();

        if (recipes.length === 0) {
            recipeGallery.innerHTML = '<p style="color: white; text-align: center; grid-column: 1/-1;">No recipes yet. Extract your first recipe!</p>';
            return;
        }

        recipeGallery.innerHTML = recipes.map(recipe => {
            const thumbnailUrl = recipe.thumbnail_path ? `http://localhost:8000/${recipe.thumbnail_path}` : 'https://via.placeholder.com/300x200?text=No+Image';
            const date = new Date(recipe.created_at).toLocaleDateString();

            return `
                <div class="recipe-card" onclick="viewRecipeDetail(${recipe.id})">
                    <img src="${thumbnailUrl}" alt="${recipe.title}" class="recipe-card-image">
                    <div class="recipe-card-content">
                        <span class="recipe-card-platform">
                            <i class="fab fa-${recipe.platform}"></i> ${recipe.platform}
                        </span>
                        <h3 class="recipe-card-title">${recipe.title || 'Untitled Recipe'}</h3>
                        <p class="recipe-card-description">${recipe.description || 'No description available'}</p>
                        <div class="recipe-card-footer">
                            <span class="recipe-card-date">${date}</span>
                            <div class="recipe-card-actions">
                                <button class="icon-btn" onclick="event.stopPropagation(); viewGroceryList(${recipe.id})" title="Grocery List">
                                    <i class="fas fa-shopping-cart"></i>
                                </button>
                                <button class="icon-btn" onclick="event.stopPropagation(); exportPDF(${recipe.id})" title="Export PDF">
                                    <i class="fas fa-file-pdf"></i>
                                </button>
                                <button class="icon-btn" onclick="event.stopPropagation(); deleteRecipe(${recipe.id})" title="Delete">
                                    <i class="fas fa-trash"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading recipes:', error);
        recipeGallery.innerHTML = '<p style="color: white; text-align: center; grid-column: 1/-1;">Error loading recipes</p>';
    }
}

async function viewRecipeDetail(recipeId) {
    try {
        const response = await fetch(`${API_URL}/recipes/${recipeId}`);
        const recipe = await response.json();

        let modalHtml = '';
        displayRecipe(recipe);

        // Also show in modal for detail view
        modalContent.innerHTML = recipeDisplay.innerHTML;
        recipeModal.classList.remove('hidden');
        recipeModal.style.display = 'block';
    } catch (error) {
        console.error('Error loading recipe detail:', error);
        showError('Failed to load recipe details');
    }
}

async function viewGroceryList(recipeId) {
    try {
        const response = await fetch(`${API_URL}/recipes/${recipeId}/grocery-list`);
        const data = await response.json();

        let html = `
            <h2 class="section-title"><i class="fas fa-shopping-cart"></i> Grocery List</h2>
            <h3>${data.recipe_title}</h3>
            <div style="margin: 20px 0;">
                <h4>Shopping Links:</h4>
                <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px;">
                    <a href="${data.shopping_list.bulk_shopping_links.instacart}" target="_blank" class="action-btn btn-success">
                        <i class="fas fa-shopping-bag"></i> Instacart
                    </a>
                    <a href="${data.shopping_list.bulk_shopping_links.walmart}" target="_blank" class="action-btn btn-primary">
                        <i class="fas fa-store"></i> Walmart
                    </a>
                    <a href="${data.shopping_list.bulk_shopping_links.amazon}" target="_blank" class="action-btn btn-info">
                        <i class="fab fa-amazon"></i> Amazon
                    </a>
                </div>
            </div>
            <div class="ingredients-section">
                <h4>Items (${data.shopping_list.total_items}):</h4>
                <ul class="ingredient-list">
                    ${data.shopping_list.items.map(item => `
                        <li class="ingredient-item">
                            <i class="fas fa-check-circle ingredient-icon"></i>
                            <div class="ingredient-details">
                                <div class="ingredient-name">${item.ingredient}</div>
                                <div class="ingredient-quantity">${item.quantity}</div>
                                <div style="margin-top: 8px; display: flex; gap: 8px; flex-wrap: wrap;">
                                    ${item.stores.map(store => `
                                        <a href="${store.search_url}" target="_blank" style="font-size: 12px; color: #667eea; text-decoration: none;">
                                            ${store.store_name}
                                        </a>
                                    `).join(' | ')}
                                </div>
                            </div>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;

        modalContent.innerHTML = html;
        recipeModal.classList.remove('hidden');
        recipeModal.style.display = 'block';
    } catch (error) {
        console.error('Error loading grocery list:', error);
        showError('Failed to load grocery list');
    }
}

async function exportJSON(recipeId) {
    try {
        window.open(`${API_URL}/recipes/${recipeId}/export/json`, '_blank');
    } catch (error) {
        console.error('Error exporting JSON:', error);
        showError('Failed to export JSON');
    }
}

async function exportPDF(recipeId) {
    try {
        window.open(`${API_URL}/recipes/${recipeId}/export/pdf`, '_blank');
    } catch (error) {
        console.error('Error exporting PDF:', error);
        showError('Failed to export PDF');
    }
}

async function deleteRecipe(recipeId) {
    if (!confirm('Are you sure you want to delete this recipe?')) {
        return;
    }

    try {
        const response = await fetch(`${API_URL}/recipes/${recipeId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            loadRecipes();
            recipeDisplay.classList.add('hidden');
        } else {
            showError('Failed to delete recipe');
        }
    } catch (error) {
        console.error('Error deleting recipe:', error);
        showError('Failed to delete recipe');
    }
}

function showLoading(show) {
    if (show) {
        loadingSpinner.classList.remove('hidden');
    } else {
        loadingSpinner.classList.add('hidden');
    }
}

function showError(message) {
    errorMessage.textContent = message;
    errorMessage.classList.remove('hidden');
    setTimeout(() => {
        hideError();
    }, 5000);
}

function hideError() {
    errorMessage.classList.add('hidden');
}
