<template>
  <!-- <div class="login-container">
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
  </div> -->
  <div class="login">
         <img src="../../assets/img/bg_2.jpg" alt="login image" class="login__img">
         <form action="" class="login__form" @submit.prevent="login">
            <div class="d-flex align-items-center justify-content-center mb-4 login__logo">
              <img src="../../assets/img/Class4.0.png" class="">
            </div>
            <!-- <h1 class="login__title">Login</h1> -->

            <div class="login__content">
               <div class="login__box">
                  <i class="ri-user-3-line login__icon"></i>

                  <div class="login__box-input">
                     <input type="text" required class="login__input" id="login-email" placeholder="" v-model="username">
                     <label for="login-email" class="login__label">Tên đăng nhập</label>
                  </div>
               </div>

               <div class="login__box">
                  <i class="ri-lock-2-line login__icon"></i>

                  <div class="login__box-input">
                     <input type="password" required class="login__input" id="login-pass" placeholder=" " v-model="password">
                     <label for="login-pass" class="login__label">Mật khẩu</label>
                     <i class="ri-eye-off-line login__eye" id="login-eye"></i>
                  </div>
               </div>
            </div>

            <!-- <div class="login__check">
               <div class="login__check-group">
                  <input type="checkbox" class="login__check-input" id="login-check">
                  <label for="login-check" class="login__check-label">Remember me</label>
               </div>

               <a href="#" class="login__forgot">Forgot Password?</a>
            </div> -->

            <button type="submit" class="login__button">Đăng nhập</button>

            <!-- <p class="login__register">
               Don't have an account? <a href="#">Register</a>
            </p> -->
         </form>
         <!-- Component Loading -->
        <Loading :loading="isLoading" />
      </div>

</template>

<script>
// import axios from 'axios';
import axios from '../../services/axios';
import Loading from '../../layout/loading/Loading.vue';
const API_URL = 'https://smartclassroom.click/api';
export default {
  components: {
    Loading,
  },
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
      isLoading: false,
    };
  },
  methods: {
    async login() {
      this.isLoading = true;  // Bắt đầu hiển thị loading

      try {
        const response = await axios.post(API_URL + '/accounts/login/', {
          username: this.username,
          password: this.password
        });
        
        if(response.status==200){
          this.$notify({
            type: 'success',
            icon: 'tim-icons icon-check-2',
            message: "Đăng nhập thành công",
            timeout: 3000,
            verticalAlign: 'top',
            horizontalAlign: 'center',
          });
        }
        

        localStorage.setItem('access_token', response.data.access_token);
        localStorage.setItem('refresh_token', response.data.refresh_token);

        this.$router.push('/');
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$notify({
            type: 'danger',
            icon: 'tim-icons icon-alert-circle-exc',
            message: "Tên đăng nhập hoặc mật khẩu không chính xác!",
            timeout: 3000,
            verticalAlign: 'top',
            horizontalAlign: 'center',
          });
        } else {
          this.$notify({
            type: 'danger',
            icon: 'tim-icons icon-alert-circle-exc',
            message: "Có lỗi xảy ra. Vui lòng thử lại sau",
            timeout: 3000,
            verticalAlign: 'top',
            horizontalAlign: 'right',
          });
        }
      } finally {
        this.isLoading = false;  // Kết thúc loading
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

/* Blur background khi đang loading */
.blur-background {
  filter: blur(5px);
}

/* Định dạng CSS cho trang đăng nhập */
.login {
  position: relative;
  z-index: 1;
}

input:-webkit-autofill,
  input:-webkit-autofill:focus {
    border: 1px solid transparent !important;
    -webkit-text-fill-color: #ffffff !important;
    -webkit-box-shadow: 0 0 0px 1000px transparent inset !important;
    transition: background-color 5000s ease-in-out 0s !important;
  }
</style>
