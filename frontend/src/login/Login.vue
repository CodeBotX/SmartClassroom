<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div class="input-group">
          <label for="username">Username</label>
          <input id="username" v-model="username" type="text" placeholder="Enter your username" required />
        </div>
        <div class="input-group">
          <label for="password">Password</label>
          <input id="password" v-model="password" type="password" placeholder="Enter your password" required />
        </div>
        <button type="submit" class="login-btn">Login</button>
      </form>
      <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
    </div>
  </div>

</template>

<script>

export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',

      //register

      file: null, // Biến để lưu trữ tệp đã được chọn
      message: '', // Thông báo sau khi đăng ký
      messageClass: '', // Lớp CSS để hiển thị thông báo (success/error)
    };
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post('http://127.0.0.1:8000/accounts/login/', {
          username: this.username,
          password: this.password
        });

        // Lưu token vào localStorage
        localStorage.setItem('authToken', response.data.token);

        // Chuyển hướng đến dashboard
        this.$router.push('/');
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.errorMessage = 'Tên đăng nhập hoặc mật khẩu không chính xác';
        } else {
          this.errorMessage = 'Có lỗi xảy ra. Vui lòng thử lại sau.';
        }
      }
    },
  }
};
</script>

<style scoped>
/* Container bao quanh form */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f4f8;
}

/* Box chứa form */
.login-box {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 350px;
}

/* Heading của form */
.login-box h2 {
  text-align: center;
  margin-bottom: 1.5rem;
  color: #333;
}

/* Nhóm input gồm label và input field */
.input-group {
  margin-bottom: 1rem;
}

/* Label của input */
.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #555;
  font-size: 0.9rem;
}

/* Input field */
.input-group input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

/* Hiệu ứng khi focus vào input */
.input-group input:focus {
  border-color: #3498db;
  outline: none;
}

/* Nút đăng nhập */
.login-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

/* Hiệu ứng hover khi rê chuột vào nút đăng nhập */
.login-btn:hover {
  background-color: #2980b9;
}

</style>
