<template>
    <div>
      <form @submit.prevent="login">
        <div>
          <label>Username:</label>
          <input v-model="username" type="text">
        </div>
        <div>
          <label>Password:</label>
          <input v-model="password" type="password">
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        username: '',
        password: ''
      }
    },
    methods: {
      async login() {
        try {
          let response = await axios.post('/auth/login', {
            username: this.username,
            password: this.password
          });
          localStorage.setItem('token', response.data.token);
          this.$router.push('/');
        } catch (error) {
          console.error(error);
        }
      }
    }
  }
  </script>

/** 
axios.interceptors.request.use(config => {
    let token = localStorage.getItem('token');
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  });
*/

  
  