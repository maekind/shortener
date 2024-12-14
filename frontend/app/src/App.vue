<template>
  <div class="container">
    <h1>URL Shortener</h1>
    <input
      v-model="url"
      class="textbox"
      type="text"
      placeholder="Enter your URL here"
    />
    <div class="buttons">
      <button class="shorten-btn" @click="shortenUrl">Shorten URL</button>
      <button
        v-if="shortUrl"
        class="email-btn"
        @click="sendEmail"
      >
        Send by Email
      </button>
      <p v-if="sent" class="notification">Email feature not implemented yet!</p>
    </div>
    <div v-if="shortUrl" class="result">
      <p>
        Shortened URL: 
        <a :href="shortUrl" target="_blank">{{ shortUrl }}</a>&nbsp;
        <i class="fa-regular fa-copy" @click="copyToClipboard"></i>
      </p>
      <p v-if="copied" class="notification">Copied to clipboard!</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      url: "",
      shortUrl: "",
      copied: false,
      sent: false,
      backend_host: "http://localhost:8000",
      api_url: "/api/v1",
    };
  },
  methods: {
    async shortenUrl() {
      try {
        const endpoint = `${this.backend_host}${this.api_url}/shorten?url=${encodeURIComponent(this.url)}`;
        const response = await fetch(endpoint, {
          method: "GET",
          headers: { "Content-Type": "application/json" },
        });

        if (!response.ok) {
          throw new Error("Failed to shorten the URL");
        }

        const data = await response.json();
        this.shortUrl = data.short_url;
      } catch (error) {
        alert("There was an error shortening the URL");
      }
    },
    // Utility method to reset a property after a delay
    showNotification(propertyName, delay = 2000) {
      this[propertyName] = true;
      setTimeout(() => {
        this[propertyName] = false;
      }, delay);
    },
    sendEmail() {
      this.showNotification("sent");
    },
    copyToClipboard() {
      navigator.clipboard.writeText(this.shortUrl).then(() => {
        this.showNotification("copied");
      });
    },
    async handleRedirect() {
      // Extract the short_id from the URL path
      const shortId = window.location.pathname.substring(1);
      if (shortId) {
        window.location.href = `${this.backend_host}${this.api_url}/redirect?short_id=${shortId}`;
      }
    },
  },
  mounted() {
    this.handleRedirect();
  },
};
</script>

<style scoped>
@import url("https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap");

.container {
  font-family: "Roboto", sans-serif;
  max-width: 400px;
  margin: 100px auto;
  text-align: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 12px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

h1 {
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

.textbox {
  width: 100%;
  padding: 10px;
  margin-bottom: 20px;
  border: 1px solid #ccc;
  border-radius: 25px;
  font-size: 16px;
  box-sizing: border-box;
}

.textbox:focus {
  border-color: #007bff;
  outline: none;
}

.buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

button {
  width: 80%;
  padding: 10px;
  border: none;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.shorten-btn {
  background-color: #007bff;
  color: white;
}

.shorten-btn:hover {
  background-color: #0056b3;
}

.email-btn {
  background-color: #28a745;
  color: white;
}

.email-btn:hover {
  background-color: #1e7e34;
}

.result {
  margin-top: 20px;
}

.result a {
  color: #007bff;
  text-decoration: none;
}

.result a:hover {
  text-decoration: underline;
}

.copy-icon {
  cursor: pointer;
  margin-left: 10px;
  font-size: 16px;
  color: #555;
  transition: color 0.3s ease;
}

.copy-icon:hover {
  color: #007bff;
}

.notification {
  color: green;
  font-size: 14px;
  margin-top: 5px;
}
</style>