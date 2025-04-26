class ApiClient {
  constructor(baseUrl = 'http://localhost:8000') {
    // Remove any trailing slash
    this.baseUrl = baseUrl.replace(/\/$/, '');
  }

  // Core request helper
  async _request(endpoint, options = {}) {
    const url = `${this.baseUrl}${endpoint}`;
    const { body: optionsBody, headers: optionsHeaders, ...otherOptions } = options;

    // Build the config object
    const config = {
      ...otherOptions, // e.g. method, credentials, mode, cache...
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
        ...(optionsHeaders || {}),
      },
    };

    // Attach body if provided
    if (optionsBody !== undefined) {
      config.body = typeof optionsBody === 'string'
        ? optionsBody
        : JSON.stringify(optionsBody);
    }

    const response = await fetch(url, config);

    if (!response.ok) {
      // Try to parse JSON error details
      let errorMessage = response.statusText || `Status ${response.status}`;
      try {
        const errJson = await response.json();
        if (errJson.detail) {
          errorMessage = typeof errJson.detail === 'string'
            ? errJson.detail
            : JSON.stringify(errJson.detail);
        }
      } catch (_) {
        // ignore parse errors
      }
      throw new Error(`API request failed (${response.status}): ${errorMessage}`);
    }

    // No content
    if (response.status === 204 || response.headers.get('content-length') === '0') {
      return null;
    }

    // Successful JSON response
    return response.json();
  }

  // --- Statistics ---
  async getStatsCounts() {
    return this._request('/stats/counts/');
  }

  // --- Countries ---
  createCountry(countryData) {
    return this._request('/countries/', {
      method: 'POST',
      body: countryData,
    });
  }

  getCountries(skip = 0, limit = 100) {
    return this._request(`/countries/?skip=${skip}&limit=${limit}`);
  }

  // --- Brands ---
  createBrand(brandData) {
    return this._request('/brands/', {
      method: 'POST',
      body: brandData,
    });
  }

  getBrands(skip = 0, limit = 100) {
    return this._request(`/brands/?skip=${skip}&limit=${limit}`);
  }

  // --- Users ---
  createUser(userData) {
    // Password hashing should happen server-side!
    return this._request('/users/', {
      method: 'POST',
      body: userData,
    });
  }

  getUsers(skip = 0, limit = 100) {
    return this._request(`/users/?skip=${skip}&limit=${limit}`);
  }

  getUser(userId) {
    return this._request(`/users/${userId}`);
  }

  // --- Products ---
  createProduct(productData) {
    return this._request('/products/', {
      method: 'POST',
      body: productData,
    });
  }

  getProducts(skip = 0, limit = 10000) {
    return this._request(`/products/?skip=${skip}&limit=${limit}`);
  }

  getProduct(productId) {
    return this._request(`/products/${productId}`);
  }

  deleteProduct(productId) {
    return this._request(`/products/${productId}`, {
      method: 'DELETE',
    });
  }

  updateProduct(productId, productData) {
    return this._request(`/products/${productId}`, {
      method: 'PUT',
      body: productData,
    });
  }

  // --- Carts ---
  createCart(cartData) {
    return this._request('/carts/', {
      method: 'POST',
      body: cartData,
    });
  }

  getCarts(skip = 0, limit = 100) {
    return this._request(`/carts/?skip=${skip}&limit=${limit}`);
  }

  getCart(cartId) {
    return this._request(`/carts/${cartId}`);
  }

  // --- Cart Contents ---
  addProductToCart(cartContentData) {
    return this._request('/cart_contents/', {
      method: 'POST',
      body: cartContentData,
    });
  }

  getCartContents(skip = 0, limit = 100) {
    return this._request(`/cart_contents/?skip=${skip}&limit=${limit}`);
  }

  getContentsForCart(cartId) {
    return this._request(`/carts/${cartId}/contents/`);
  }
}

const apiClient = new ApiClient();
export default apiClient;