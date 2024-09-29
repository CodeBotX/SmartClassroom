<template>
  <div>
    <!-- Register -->
    <div class="register-form">
      <h2>Đăng ký tài khoản</h2>
      <form @submit.prevent="register">
        <div class="form-group">
          <label for="file">Tải lên file danh sách</label>
          <input type="file" id="file" @change="onFileChange" />
        </div>

        <div class="form-group">
          <label for="role">Chọn loại đăng ký</label>
          <select v-model="role">
            <option value="">Chọn loại</option>
            <option value="student">Học sinh</option>
            <option value="teacher">Giáo viên</option>
            <option value="parent">Phụ huynh</option>
          </select>
        </div>

        <button type="submit" class="btn btn-primary">Đăng ký</button>
      </form>

    </div>
  </div>
</template>

<script>
import axios from '../../services/axios'; 
// const API_URL = 'https://classroom50.online';
const API_URL = 'http://127.0.0.1:8000';

export default {
  data() {
    return {
      file: null, // Biến để lưu trữ tệp đã được chọn
      role: '', // Biến để lưu trữ loại đăng ký
    };
  },
  methods: {
    // Xử lý khi người dùng chọn tệp
    onFileChange(event) {
      this.file = event.target.files[0]; // Lưu tệp đã được chọn vào biến `file`
    },

    // Xử lý gửi form đăng ký
    register() {
      if (!this.file || !this.role) {
            this.$notify({
              group: 'auth',
              title: 'Thông báo',
              text: 'Vui lòng chọn tệp và loại đăng ký',
              type: 'warn',
              duration: 3000,
            });
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file); // Đính kèm tệp vào FormData

      let apiUrl = ''; // API URL sẽ thay đổi dựa trên loại đăng ký
      if (this.role === 'student') {
        apiUrl = API_URL + '/accounts/register-student/';
      } else if (this.role === 'teacher') {
        apiUrl = API_URL + '/accounts/register-teacher/';
      } else if (this.role === 'parent') {
        apiUrl = API_URL + '/accounts/register-parent/';
      }

      // Gửi yêu cầu POST đến API đăng ký
      axios
        .post(apiUrl, formData, {
          headers: {
            'Content-Type': 'multipart/form-data',
          },
        })
        .then((response) => {
          this.message = response.data.detail;
          this.$notify({
          group: 'auth',
          title: 'Hệ thống',
          text: response.data.detail,
          type: 'success',  // Kiểu thông báo: 'success', 'error', 'warn'
          duration: 3000,
        });
        })
        .catch((error) => {
          // this.message =
          //   'Có lỗi xảy ra: ' +
          //   (error.response?.data?.error || 'Đăng ký thất bại');
          // this.messageClass = 'error';
          if (error.response){
            this.$notify({
              group: 'auth',
              title: 'Thông báo',
              text: 'Lựa chọn loại tài khoản được tạo không hợp lệ ',
              type: 'warn',
              duration: 3000,
            });
          }
          else {
          this.$notify({
          group: 'auth',
          title: 'Lỗi',
          text: 'Có lỗi xảy ra. Vui lòng thử lại sau',
          type: 'error',
          duration: 3000,
        });
        }
          
        });
    },
  },
};
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

.form-group input[type='file'] {
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
