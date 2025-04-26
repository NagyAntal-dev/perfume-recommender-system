<script>
  import { onMount } from 'svelte';
  import apiClient from './lib/apiClient';
  import ProductManager from './ProductManager.svelte';

  let users = [];
  let products = [];
  let carts = [];
  let countries = [];
  let brands = [];
  let stats = null;
  let isLoading = true;
  let isLoadingStats = true;
  let errorMessage = '';
  let showProductManager = false;

  async function fetchData(forceRefresh = false) {
    if (!products.length || forceRefresh) {
        isLoading = true;
    }
    isLoadingStats = true;
    errorMessage = '';
    try {

      const [usersData, productsData, cartsData, countriesData, brandsData, statsData] = await Promise.all([
        apiClient.getUsers(0, 10),
        apiClient.getProducts(0, 10),
        apiClient.getCarts(0, 10),
        apiClient.getCountries(0, 10),
        apiClient.getBrands(0, 10),
        apiClient.getStatsCounts()
      ]);
      users = usersData || [];
      products = productsData || [];
      carts = cartsData || [];
      countries = countriesData || [];
      brands = brandsData || [];
      stats = statsData;
      console.log('Fetched Admin Data:', { users, products, carts, countries, brands, stats });
    } catch (error) {
      console.error('Error fetching admin data:', error);
      errorMessage = `Failed to fetch data: ${error.message}. Is the backend API running at ${apiClient.baseUrl}?`;
      stats = null;
    } finally {
      isLoading = false;
      isLoadingStats = false;
    }
  }

  function toggleProductManager() {
    showProductManager = !showProductManager;
    if (showProductManager && products.length < (stats?.products || 1000)) {

         fetchAllProductsForManager();
    }
  }


  async function fetchAllProductsForManager() {
      console.log("Fetching all products for manager...");

      try {
          const allProducts = await apiClient.getProducts(0, 5000);
          products = allProducts || [];
      } catch(err) {
          console.error("Failed to fetch all products for manager", err);

      }
  }



  function handleProductsUpdated() {
    fetchData(true);
  }


  onMount(() => fetchData(true));

</script>

<div class="container mt-4">
  {#if isLoading && !products.length} <!-- Show main loader only on initial load -->
    <div class="d-flex justify-content-center">
      <div class="spinner-border" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>
  {:else if errorMessage}
    <div class="alert alert-danger" role="alert">
      Error: {errorMessage}
    </div>
  {:else}
    {#if showProductManager}
      <!-- Show Product Manager Component -->
       <ProductManager
         initialProducts={products}
         brands={brands}
         on:close={toggleProductManager}
         on:updated={handleProductsUpdated}
       />
    {:else}
      <!-- Show Default Dashboard View -->
      <div class="row g-3">

        <!-- Statistics Section -->
        <div class="col-12 mb-4">
          <h4>Database Statistics</h4>
          {#if isLoadingStats}
            <div class="text-center">
              <div class="spinner-border spinner-border-sm" role="status">
                <span class="visually-hidden">Loading Stats...</span>
              </div>
            </div>
          {:else if stats}
            <div class="row g-3">
              <div class="col-sm-6 col-md-4 col-lg-3">
                <div class="card text-center">
                  <div class="card-body">
                    <h5 class="card-title">{stats.users}</h5>
                    <p class="card-text">Total Users</p>
                  </div>
                </div>
              </div>
              <div class="col-sm-6 col-md-4 col-lg-3">
                <div class="card text-center">
                  <div class="card-body">
                    <h5 class="card-title">{stats.products}</h5>
                    <p class="card-text">Total Products</p>
                  </div>
                </div>
              </div>
              <div class="col-sm-6 col-md-4 col-lg-3">
                <div class="card text-center">
                  <div class="card-body">
                    <h5 class="card-title">{stats.brands}</h5>
                    <p class="card-text">Total Brands</p>
                  </div>
                </div>
              </div>
               <div class="col-sm-6 col-md-4 col-lg-3">
                <div class="card text-center">
                  <div class="card-body">
                    <h5 class="card-title">{stats.carts}</h5>
                    <p class="card-text">Total Carts</p>
                  </div>
                </div>
              </div>
            </div>
          {:else}
            <p class="text-muted">Could not load statistics.</p>
          {/if}
          <hr class="my-4">
        </div>


        <!-- Users Section -->
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">Recent Users ({users.length})</div>
            <div class="card-body" style="max-height: 300px; overflow-y: auto;">
              {#if users.length > 0}
                <ul class="list-group list-group-flush">
                  {#each users as user (user.user_id)}
                    <li class="list-group-item">{user.username} ({user.full_name}) - {user.mail}</li>
                  {/each}
                </ul>
              {:else}
                <p class="text-muted">No users found.</p>
              {/if}
            </div>
             <div class="card-footer text-end">
               <button class="btn btn-sm btn-outline-secondary" on:click={() => alert('Manage Users clicked!')}>Manage Users</button>
             </div>
          </div>
        </div>

        <!-- Products Section -->
        <div class="col-md-6">
          <div class="card">
            <div class="card-header">Recent Products ({products.length})</div>
             <div class="card-body" style="max-height: 300px; overflow-y: auto;">
              {#if products.length > 0}
                <ul class="list-group list-group-flush">
                  {#each products as product (product.product_id)} <!-- Show only first 10 fetched -->
                    <li class="list-group-item">{product.perfume?.replaceAll('-',' ') || 'N/A'} - Price: {product.price}</li>
                  {/each}
                </ul>
              {:else}
                <p class="text-muted">No products found.</p>
              {/if}
            </div>
             <div class="card-footer text-end">
               <button class="btn btn-sm btn-outline-secondary" on:click={toggleProductManager}>Manage Products</button>
             </div>
          </div>
        </div>

        <!-- Carts Section -->
         <div class="col-md-6">
          <div class="card">
            <div class="card-header">Recent Carts ({carts.length})</div>
            <div class="card-body" style="max-height: 300px; overflow-y: auto;">
              {#if carts.length > 0}
                <ul class="list-group list-group-flush">
                  {#each carts as cart (cart.cart_id)}
                    <li class="list-group-item">Cart ID: {cart.cart_id} - User ID: {cart.user_id}</li>
                  {/each}
                </ul>
              {:else}
                <p class="text-muted">No carts found.</p>
              {/if}
            </div>
             <div class="card-footer text-end">
               <button class="btn btn-sm btn-outline-secondary" on:click={() => alert('View Carts clicked!')}>View Carts</button>
             </div>
          </div>
        </div>

         <!-- Countries & Brands Section -->
         <div class="col-md-6">
           <div class="card">
             <div class="card-header">Reference Data Preview</div>
             <div class="card-body" style="max-height: 300px; overflow-y: auto;">
               <h5>Countries ({countries.length})</h5>
               {#if countries.length > 0}
                 <ul class="list-group list-group-flush mb-3">
                   {#each countries as country (country.country_id)} <!-- Show only first 5 fetched -->
                     <li class="list-group-item">{country.country}</li>
                   {/each}
                 </ul>
               {:else}
                 <p class="text-muted">No countries found.</p>
               {/if}

               <h5>Brands ({brands.length})</h5>
                {#if brands.length > 0}
                 <ul class="list-group list-group-flush">
                   {#each brands as brand (brand.brand_id)} <!-- Show only first 5 fetched -->
                     <li class="list-group-item">{brand.brand}</li>
                   {/each}
                 </ul>
               {:else}
                 <p class="text-muted">No brands found.</p>
               {/if}
             </div>
              <div class="card-footer text-end">
               <button class="btn btn-sm btn-outline-secondary" on:click={() => alert('Manage Reference Data clicked!')}>Manage Data</button>
             </div>
           </div>
         </div>

      </div> <!-- End row g-3 -->
    {/if} <!-- End {#if showProductManager} -->
  {/if} <!-- End {#if isLoading} -->
</div> <!-- End container -->