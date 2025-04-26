<script>
  import { createEventDispatcher, onMount } from 'svelte'; // Import onMount
  import apiClient from './lib/apiClient';

  // initialProducts prop is still useful for potentially faster initial display
  // but the component will fetch its own full list.
  export let initialProducts = [];
  export let brands = [];

  let products = []; // Initialize as empty, will be filled by fetch
  let isLoading = true; // Start in loading state
  let error = '';
  let showAddForm = false;
  let searchTerm = '';

  // Form state for adding a new product
  let newProduct = {
    produrl: '', perfume: '', gender: 'unisex', rating_value: null, rating_count: null,
    create_year: null, top_note: '', middle_note: '', base_note: '', price: null,
    brand_id: null, quantity: 0
  };

  const dispatch = createEventDispatcher();

  // --- Function to fetch all products within this component ---
  async function loadAllProducts() {
    isLoading = true;
    error = '';
    console.log("ProductManager: Fetching all products...");
    try {
      // Use a large limit to fetch effectively all products
      const allProducts = await apiClient.getProducts(0, 2000);
      products = allProducts || []; // Update the local products array
      console.log(`ProductManager: Fetched ${products.length} products.`);
    } catch (err) {
      console.error('ProductManager: Error loading products:', err);
      error = `Failed to load products: ${err.message}`;
      products = []; // Clear products on error
    } finally {
      isLoading = false;
    }
  }

  // --- Fetch products when the component mounts ---
  onMount(() => {
    loadAllProducts();
  });

  function closeManager() {
    dispatch('close');
  }

  async function deleteProduct(productId) {
    if (!confirm('Are you sure you want to delete this product?')) {
      return;
    }
    // Indicate loading specific to this action if desired
    isLoading = true; // Or use a different loading flag for row-specific actions
    error = '';
    try {
      await apiClient.deleteProduct(productId);
      // Update local state directly
      products = products.filter(p => p.product_id !== productId);
      // No need to dispatch 'updated' if AdminDashboard doesn't need to refetch everything now
      // dispatch('updated'); // Keep if AdminDashboard needs to refresh stats or other data
    } catch (err) {
      console.error('Error deleting product:', err);
      error = `Failed to delete product: ${err.message}`;
    } finally {
      isLoading = false;
    }
  }

  async function handleAddProduct() {
    isLoading = true; // Loading for the form submission
    error = '';
    try {
        if (!newProduct.perfume || !newProduct.brand_id || newProduct.price == null || !newProduct.produrl) {
            throw new Error("Perfume name, brand, price, and URL are required.");
        }
        const payload = {
            ...newProduct,
            top_note: newProduct.top_note || null,
            middle_note: newProduct.middle_note || null,
            base_note: newProduct.base_note || null,
            rating_value: newProduct.rating_value ?? null,
            rating_count: newProduct.rating_count ?? null,
            create_year: newProduct.create_year ?? null,
            price: newProduct.price ?? null, // Already handled by required check
            quantity: newProduct.quantity ?? 0,
            brand_id: newProduct.brand_id ?? null // Already handled by required check
        };
        const addedProduct = await apiClient.createProduct(payload);
        // Update local state directly
        products = [...products, addedProduct];
        showAddForm = false;
        resetNewProductForm();
        // No need to dispatch 'updated' if AdminDashboard doesn't need to refetch everything now
        // dispatch('updated'); // Keep if AdminDashboard needs to refresh stats or other data
    } catch (err) {
        console.error('Error adding product:', err);
        error = `Failed to add product: ${err.message}`;
    } finally {
        isLoading = false;
    }
  }

  function resetNewProductForm() {
     newProduct = {
        produrl: '', perfume: '', gender: 'unisex', rating_value: null, rating_count: null,
        create_year: null, top_note: '', middle_note: '', base_note: '', price: null,
        brand_id: brands.length > 0 ? brands[0].brand_id : null, // Default to first brand
        quantity: 0
     };
  }

  // Initialize form default brand_id when brands are available
  $: if (brands.length > 0 && newProduct.brand_id === null) {
      newProduct.brand_id = brands[0].brand_id;
  }

  // Reactive statement to filter products based on searchTerm
  $: filteredProducts = products.filter(product => {
    const term = searchTerm.toLowerCase();
    const productName = (product.perfume || '').toLowerCase();
    const brand = brands.find(b => b.brand_id === product.brand_id);
    const brandName = (brand?.brand || '').toLowerCase();

    return productName.includes(term) || brandName.includes(term);
  });

</script>

<div>
  <div class="d-flex justify-content-between align-items-center mb-3">
    <h3>Manage Products</h3>
    <button class="btn btn-secondary" on:click={closeManager}>Back to Dashboard</button>
  </div>

  {#if error}
    <div class="alert alert-danger">{error}</div>
  {/if}

  <!-- Main loading indicator for initial fetch -->
  {#if isLoading && !products.length}
    <div class="text-center my-5">
      <div class="spinner-border" role="status" style="width: 3rem; height: 3rem;">
        <span class="visually-hidden">Loading Products...</span>
      </div>
      <p class="mt-2">Loading all products...</p>
    </div>
  {/if}

  <!-- Add Product Button/Form Toggle -->
  <div class="mb-3">
    {#if !showAddForm}
      <button class="btn btn-success" on:click={() => { showAddForm = true; resetNewProductForm(); error = ''; }}>
        <i class="bi bi-plus-circle"></i> Add New Product
      </button>
    {:else}
      <!-- Add Product Form -->
      <form on:submit|preventDefault={handleAddProduct} class="card p-3">
        <h4>Add New Product</h4>
         <div class="row g-3">
           <div class="col-md-6">
             <label for="add-perfume" class="form-label">Perfume Name*</label>
             <input type="text" class="form-control" id="add-perfume" bind:value={newProduct.perfume} required>
           </div>
           <div class="col-md-6">
             <label for="add-brand" class="form-label">Brand*</label>
             <select class="form-select" id="add-brand" bind:value={newProduct.brand_id} required>
               {#if !brands.length}<option disabled>Loading brands...</option>{/if}
               {#each brands as brand (brand.brand_id)}
                 <option value={brand.brand_id}>{brand.brand}</option>
               {/each}
             </select>
           </div>
            <div class="col-md-12">
             <label for="add-produrl" class="form-label">Product URL*</label>
             <input type="url" class="form-control" id="add-produrl" bind:value={newProduct.produrl} required>
           </div>
           <div class="col-md-4">
             <label for="add-price" class="form-label">Price*</label>
             <input type="number" step="0.01" class="form-control" id="add-price" bind:value={newProduct.price} required>
           </div>
           <div class="col-md-4">
             <label for="add-quantity" class="form-label">Quantity</label>
             <input type="number" class="form-control" id="add-quantity" bind:value={newProduct.quantity}>
           </div>
           <div class="col-md-4">
             <label for="add-gender" class="form-label">Gender</label>
             <select class="form-select" id="add-gender" bind:value={newProduct.gender}>
               <option value="men">Men</option>
               <option value="women">Women</option>
               <option value="unisex">Unisex</option>
             </select>
           </div>
            <div class="col-md-4">
             <label for="add-year" class="form-label">Creation Year</label>
             <input type="number" class="form-control" id="add-year" bind:value={newProduct.create_year}>
           </div>
           <div class="col-md-4">
             <label for="add-rating-val" class="form-label">Rating Value</label>
             <input type="number" step="0.01" class="form-control" id="add-rating-val" bind:value={newProduct.rating_value}>
           </div>
           <div class="col-md-4">
             <label for="add-rating-count" class="form-label">Rating Count</label>
             <input type="number" class="form-control" id="add-rating-count" bind:value={newProduct.rating_count}>
           </div>
           <div class="col-md-4">
             <label for="add-top-note" class="form-label">Top Notes</label>
             <textarea class="form-control" id="add-top-note" rows="2" bind:value={newProduct.top_note}></textarea>
           </div>
            <div class="col-md-4">
             <label for="add-middle-note" class="form-label">Middle Notes</label>
             <textarea class="form-control" id="add-middle-note" rows="2" bind:value={newProduct.middle_note}></textarea>
           </div>
            <div class="col-md-4">
             <label for="add-base-note" class="form-label">Base Notes</label>
             <textarea class="form-control" id="add-base-note" rows="2" bind:value={newProduct.base_note}></textarea>
           </div>
         </div>
        <div class="mt-3">
          <button type="submit" class="btn btn-primary me-2" disabled={isLoading}>
            {#if isLoading}<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> {/if}Save Product
          </button>
          <button type="button" class="btn btn-secondary" on:click={() => { showAddForm = false; error = ''; }}>Cancel</button>
        </div>
      </form>
    {/if}
  </div>

  <!-- Search Bar -->
  <div class="mb-3">
    <input
      type="text"
      class="form-control"
      placeholder="Search by product name or brand..."
      bind:value={searchTerm}
    />
  </div>

  <!-- Products Table -->
  <div class="table-responsive">
    <table class="table table-striped table-hover">
      <thead>
        <tr>
          <th>ID</th>
          <th>Name</th>
          <th>Brand</th>
          <th>Price</th>
          <th>Qty</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <!-- Use filteredProducts here -->
        {#each filteredProducts as product (product.product_id)}
          <tr>
            <td>{product.product_id}</td>
            <td>{product.perfume?.replaceAll('-',' ') || 'N/A'}</td>
            <td>{brands.find(b => b.brand_id === product.brand_id)?.brand || 'Unknown'}</td>
            <td>{product.price} Ft</td>
            <td>{product.quantity}</td>
            <td>
              <button class="btn btn-sm btn-outline-primary me-1" on:click={() => alert(`Edit product ${product.product_id}`)} title="Edit" disabled={isLoading}>
                <i class="bi bi-pencil-square"></i>
              </button>
              <button
                class="btn btn-sm btn-outline-danger"
                on:click={() => deleteProduct(product.product_id)}
                title="Delete"
                disabled={isLoading}
              >
                 <!-- Removed spinner logic here for simplicity, main isLoading covers page load -->
                 <i class="bi bi-trash"></i>
              </button>
            </td>
          </tr>
        {:else}
          <tr>
            <td colspan="6" class="text-center text-muted">
              {#if isLoading}
                 <!-- This might show briefly between fetch start and table render -->
                 Loading...
              {:else if searchTerm}
                No products match your search "{searchTerm}".
              {:else if products.length === 0 && !error}
                 No products found in the database.
              {:else if !error}
                 <!-- Should not happen if products array is populated -->
                 No products to display.
              {/if}
            </td>
          </tr>
        {/each}
      </tbody>
    </table>
  </div>
</div>

<style>
    /* Optional: Add some specific styles */
    .table th, .table td {
        vertical-align: middle;
    }
    /* Add Bootstrap Icons CSS to your main HTML or import if needed */
    /* @import url("https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css"); */
</style>