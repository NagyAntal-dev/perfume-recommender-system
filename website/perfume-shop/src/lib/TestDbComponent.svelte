<script>
  import { onMount } from 'svelte';
  import dataService from './dataService'; // Import the singleton instance

  let products = [];
  let users = [];
  let errorMessage = '';
  let isLoading = true;

  onMount(async () => {
    try {
      isLoading = true;
      errorMessage = '';
      console.log('Attempting to fetch data...');

      // Test fetching products
      products = await dataService.getAllProducts();
      console.log('Fetched Products:', products);

      // Test fetching users (optional, add more tests as needed)
      // users = await dataService.getAllUsers(); // Assuming you add a getAllUsers method
      // console.log('Fetched Users:', users);

      // Example: Test fetching a specific user (if one exists with ID 1)
      // const user = await dataService.getUserById(1);
      // console.log('Fetched User 1:', user);

      // Example: Test creating a user (use with caution, might insert duplicates)
      /*
      const newUser = await dataService.createUser({
          username: `testuser_${Date.now()}`,
          full_name: 'Test User',
          sex: 'Other',
          mail: `test_${Date.now()}@example.com`,
          birthdate: '2000-01-01',
          country: 'Testland',
          city: 'Testville',
          street_address: '123 Test St',
          password_hash: 'hashed_password_example' // Replace with actual hash if needed
      });
      console.log('Created User:', newUser);
      */


    } catch (error) {
      console.error('Error testing DataService:', error);
      errorMessage = `Failed to connect or fetch data: ${error.message}`;
      // Attempt to connect explicitly if fetching failed (optional debug step)
      try {
        await dataService.db.connect(); // Access the db instance directly for connect test
        console.log('Manual connection successful after error.');
      } catch (connectError) {
        console.error('Manual connection also failed:', connectError);
        errorMessage += ` | Manual connection failed: ${connectError.message}`;
      }
    } finally {
      isLoading = false;
    }
  });

</script>

<div>
  <h2>DataService Test</h2>

  {#if isLoading}
    <p>Loading data...</p>
  {:else if errorMessage}
    <p style="color: red;">Error: {errorMessage}</p>
    <p>Check the browser console and ensure your Node.js server/environment where this code runs can reach the PostgreSQL container at localhost:5432.</p>
     <p>Make sure the database container is running (`docker-compose up -d postgres`) and that the `pg` library is installed (`npm install pg`).</p>
  {:else}
    <h3>Products ({products.length})</h3>
    {#if products.length > 0}
      <ul>
        {#each products as product (product.product_id)}
          <li>
            {product.perfume} by {product.brand} ({product.country}) - Price: {product.price} - Qty: {product.quantity}
          </li>
        {/each}
      </ul>
    {:else}
      <p>No products found in the database.</p>
    {/if}

    <!-- Add sections to display other fetched data like users if needed -->
    <!--
    <h3>Users ({users.length})</h3>
    {#if users.length > 0}
      <ul>
        {#each users as user (user.user_id)}
          <li>{user.username} ({user.full_name})</li>
        {/each}
      </ul>
    {:else}
      <p>No users found.</p>
    {/if}
    -->
  {/if}
</div>

<style>
  ul {
    list-style: none;
    padding: 0;
  }
  li {
    margin-bottom: 5px;
    padding: 5px;
    border: 1px solid #eee;
  }
</style>