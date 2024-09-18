<template>
  <div>
    <!-- Register -->
    
    <div class="register-form">
    <h2>Đăng ký tài khoản</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="file">Tải lên file danh sách</label>
        <input type="file" id="file" @change="onFileChange" required>x
      </div>
      <button type="submit" class="btn btn-primary">Đăng ký</button>
    </form>
    
    <div v-if="message" :class="messageClass">{{ message }}</div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null, // Biến để lưu trữ tệp đã được chọn
      message: '', // Thông báo sau khi đăng ký
      messageClass: '', // Lớp CSS để hiển thị thông báo (success/error)
    };
  },
  methods: {
    // Xử lý khi người dùng chọn tệp
    onFileChange(event) {
      this.file = event.target.files[0]; // Lưu tệp đã được chọn vào biến `file`
    },
    
    // Xử lý gửi form đăng ký
    register() {
      if (!this.file) {
        this.message = 'Vui lòng chọn tệp trước khi đăng ký.';
        this.messageClass = 'error';
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file); // Đính kèm tệp vào FormData

      // Gửi yêu cầu POST đến API đăng ký
      axios.post('http://127.0.0.1:8000/accounts/register/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        this.message = response.data.detail;
        this.messageClass = 'success';
      })
      .catch(error => {
        this.message = 'Có lỗi xảy ra: ' + (error.response?.data?.error || 'Đăng ký thất bại');
        this.messageClass = 'error';
      });
    }
  }
}
</script>

<style>
  /* REGISTER */

.register-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    background-color: #f9f9f9;
  }

  .form-group {
    margin-bottom: 15px;
  }

  .form-group label {
    display: block;
    margin-bottom: 5px;
    font-weight: bold;
  }

  .form-group input[type="file"] {
    width: 100%;
  }

  .btn {
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }

  .btn:hover {
    background-color: #0056b3;
  }

  .success {
    color: green;
    margin-top: 10px;
  }

  .error {
    color: red;
    margin-top: 10px;
  }
</style>