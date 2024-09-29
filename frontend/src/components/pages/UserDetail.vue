<template>
  <div class="user-detail-container">
    <h1>Thông tin người dùng</h1>
    <div v-if="errorMessage">
      <p class="error-message">{{ errorMessage }}</p>
    </div>
    <div v-else-if="userData" class="user-info">
      <div class="user-status">
        <p v-if="userData.is_student" class="status student"><strong>Học sinh</strong></p>
        <p v-if="userData.is_parent" class="status parent"><strong>Phụ huynh</strong></p>
        <p v-if="userData.is_teacher" class="status teacher"><strong>Giáo viên</strong></p>
        <p v-if="userData.is_admin" class="status admin"><strong>ADMIN</strong></p>
      </div>
      <div class="info-details">
        <p><strong>ID:</strong> {{ userData.user_id }}</p>
        <p><strong>Họ và tên:</strong> {{ userData.full_name }}</p>
        <p><strong>SĐT:</strong> {{ userData.phone_number }}</p>
        <p><strong>Ngày sinh:</strong> {{ new Date(userData.day_of_birth).toLocaleDateString() }}</p>
        <p><strong>Giới tính:</strong> {{ userData.sex }}</p>
        <p><strong>Quốc gia:</strong> {{ userData.nation }}</p>
        <p><strong>Email:</strong> {{ userData.email }}</p>

        <div v-if="userData.is_student">
          <p><strong>Lớp:</strong> {{ userData.room }}</p>
          <p><strong>Tên phụ huynh:</strong> {{ userData.parent }}</p>
        </div>
      </div>

      <button class="edit-button" @click="editUserDetail">Sửa thông tin</button>
      <br>
      <button class="edit-button" @click="editUserPassword">Đổi mật khẩu</button>
      <br>
      <button v-if="userData.is_admin" class="edit-button" @click="editResetPassword">Reset Password(Only ADMIN)</button>
    </div>
    <div v-else>
      <p>Đang tải thông tin người dùng...</p>
    </div>

    <!-- Overlay cho form sửa thông tin -->
    <div v-if="isEditingDetail" class="overlay" @click="cancelEditDetail">
      <div class="edit-form" @click.stop>
        <h2>Sửa thông tin người dùng</h2>
        <form @submit.prevent="updateUser">
          <div class="form-group">
            <label for="full_name">Họ và tên:</label>
            <input type="text" v-model="userData.full_name" required />
          </div>
          <div class="form-group">
            <label for="day_of_birth">Ngày sinh:</label>
            <input type="date" v-model="userData.day_of_birth" required />
          </div>
          <div class="form-group">
            <label for="day_of_birth">Giới tính:</label>
            <input type="text" v-model="userData.sex" required />
          </div>
          <div class="form-group">
            <label for="day_of_birth">Quốc gia:</label>
            <input type="text" v-model="userData.nation" required />
          </div>
          <div class="form-group">
            <label for="day_of_birth">Email:</label>
            <input type="text" v-model="userData.email" required />
          </div>
          <div class="form-group">
            <label for="phone_number">SĐT:</label>
            <input type="text" v-model="userData.phone_number" required />
          </div>

          <div class="button-group">
            <button type="submit" class="save-button">Lưu</button>
            <button type="button" class="cancel-button" @click="cancelEditDetail">Hủy</button>
          </div>
        </form>
      </div>
    </div>

     <!-- Overlay cho form đổi mật khẩu -->
    <div v-if="isEditingPassword" class="overlay" @click="cancelEditPassword">
      <div class="edit-form" @click.stop>
        <h2>Đổi mật khẩu</h2>
        <form @submit.prevent="updatePassword">
          <div class="form-group">
            <label for="full_name">Mật khẩu cũ</label>
            <input type="password" v-model="old_password" required />
          </div>
          <div class="form-group">
            <label for="day_of_birth">Mật khẩu mới:</label>
            <input type="password" v-model="new_password" required />
          </div>

          <div class="button-group">
            <button type="submit" class="save-button">Xác nhận</button>
            <button type="button" class="cancel-button" @click="cancelEditPassword">Hủy</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Overlay cho reset mật khẩu -->
    <div v-if="isEditingResetPassword" class="overlay" @click="cancelEditResetPassword">
      <div class="edit-form" @click.stop>
        <h2>Reset Password</h2>
        <form @submit.prevent="resetPassword">
          <div class="form-group">
            <label for="full_name">User ID:</label>
            <input type="text" v-model="user_id_reset" required />
          </div>

          <div class="button-group">
            <button type="submit" class="save-button">Xác nhận</button>
            <button type="button" class="cancel-button" @click="cancelEditResetPassword">Hủy</button>
          </div>
        </form>
      </div>
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
      errorMessage: '',
      userData: null, // Chứa thông tin người dùng
      isEditingDetail: false,
      isEditingPassword: false,
      isEditingResetPassword: false,
      old_password: null,
      new_password: null,
      user_id_reset: null,
    };
  },
   mounted() {
    this.getUserData(); // Gọi API khi trang tải
  }, 
  methods: {
    getUserData() {
      const token = localStorage.getItem('access_token');
      axios.post(API_URL+'/accounts/detail/', {}, {
        headers: {
          'Authorization': `Bearer ${token}`  // Đính kèm token vào headers
        }
      })
      .then((response) => {
         // Lưu dữ liệu người dùng vào userData
        // this.userData.full_name = response.data.user.full_name;
        // this.userData.sex = response.data.user.sex;
        // this.userData.nation = response.data.user.nation;
        // this.userData.email = response.data.user.email;
        // this.userData.day_of_birth = response.data.user.day_of_birth;
        this.userData = response.data
         this.getUserData
        console.log(this.userData)
      })
      .catch(error => {
        console.error("Error fetching user data:", error);
        this.$notify({
          group: 'app',
          title: 'Lỗi',
          text: "Lấy thông tin người dùng thất bại!",
          type: 'error',
          duration: 3000,
        });
      });
    },
    editUserDetail() {
      this.isEditingDetail = true; // Bật chế độ chỉnh sửa
    },
    cancelEditDetail() {
      this.isEditingDetail = false; // Hủy chế độ chỉnh sửa
    },
    editUserPassword() {
      this.isEditingPassword = true; // Bật chế độ chỉnh sửa
    },
    cancelEditPassword() {
      this.isEditingPassword = false; // Hủy chế độ chỉnh sửa
      this.old_password = null;
      this.new_password = null;
    },
    editResetPassword() {
      this.isEditingResetPassword = true; // Bật chế độ chỉnh sửa
    },
    cancelEditResetPassword() {
      this.isEditingResetPassword = false; // Hủy chế độ chỉnh sửa
      this.user_id_reset = null;
    },
    updateUser() {
      const token = localStorage.getItem('access_token');
      const updateData = {
      user: {
          full_name: this.userData.full_name,
          sex: this.userData.phone_number,
          nation: this.userData.day_of_birth,
          email: this.userData.email,
          phone_number: this.userData.phone_number,
          day_of_birth: this.userData.day_of_birth,
      },
        active_status: "Active"
    };

      axios.patch(API_URL+'/accounts/update/', updateData, {
        headers: {
          'Authorization': `Bearer ${token}`, // Đính kèm token vào headers
          'Content-Type': 'application/json',
        }
      })
      .then(() => {
        // this.userData = response.data; // Cập nhật thông tin người dùng
        // this.isEditing = false; // Tắt chế độ chỉnh sửa
        this.getUserData
        this.isEditingDetail = false; // Tắt chế độ chỉnh sửa
      })
      .catch(error => {
        console.error("Error updating user data:", error);
        this.isEditingDetail = false; // Tắt chế độ chỉnh sửa
        this.$notify({
          group: 'app',
          title: 'Lỗi',
          text: "Cập nhật thông tin người dùng thất bại!",
          type: 'error',
          duration: 3000,
        });
      });
    },
    updatePassword() {
      const token = localStorage.getItem('access_token');
      const changePasswordData = {
      old_password: this.old_password,
      new_password: this.new_password
    };

      axios.post(API_URL+'/accounts/change-password/', changePasswordData, {
        headers: {
          'Authorization': `Bearer ${token}`, // Đính kèm token vào headers
          'Content-Type': 'application/json',
        }
      })
      .then(response => {
        this.$notify({
          group: 'auth',
          title: 'Hệ thống',
          text: response.data.detail,
          type: 'success',  // Kiểu thông báo: 'success', 'error', 'warn'
          duration: 3000,
        });
        this.isEditingPassword = false; // Tắt chế độ chỉnh sửa

        this.old_password = null;
        this.new_password = null;
      })
      .catch(error => {
        console.error("Error change password user :", error);
        
        // this.isEditingPassword = false; // Tắt chế độ chỉnh sửa
        if (error.response && error.response.data){
          this.$notify({
              group: 'auth',
              title: 'Thông báo',
              text: error.response.data.old_password || error.response.data.new_password || 'Có lỗi xảy ra khi đổi mật khẩu.',
              type: 'warn',
              duration: 3000,
            });
        }else {
          this.$notify({
            group: 'app',
            title: 'Lỗi',
            text: "Đổi mật khẩu không thành công. Vui lòng thử lại !",
            type: 'error',
            duration: 3000,
          });
        }
        
      });
    },
    resetPassword() {
      const token = localStorage.getItem('access_token');
      const resetPasswordData = {
      user_id: this.user_id_reset
    };

      axios.post(API_URL+'/accounts/admin-reset-password/', resetPasswordData, {
        headers: {
          'Authorization': `Bearer ${token}`, // Đính kèm token vào headers
          'Content-Type': 'application/json',
        }
      })
      .then(response => {
        this.$notify({
          group: 'auth',
          title: 'Hệ thống',
          text: response.data.detail,
          type: 'success',  // Kiểu thông báo: 'success', 'error', 'warn'
          duration: 3000,
        });
        this.isEditingResetPassword = false; // Tắt chế độ chỉnh sửa

        this.user_id_reset = null;
      })
      .catch(error => {
        console.error("Error reset password user :", error);
        
        // this.isEditingPassword = false; // Tắt chế độ chỉnh sửa
        if (error.response && error.response.data){
          if(error.response.status === 401){
            this.$notify({
              group: 'auth',
              title: 'Thông báo',
              text: "Bạn không có quyền thực hiện thao tác này",
              type: 'warn',
              duration: 3000,
            }); 
          }
          if(error.response.status === 404){
            this.$notify({
              group: 'auth',
              title: 'Thông báo',
              text: "Người dụng không tồn tại. Vui lòng thử lại",
              type: 'warn',
              duration: 3000,
            }); 
          }
          
        }else {
          this.$notify({
            group: 'app',
            title: 'Lỗi',
            text: "Reset mật khẩu không thành công. Vui lòng thử lại !",
            type: 'error',
            duration: 3000,
          });
        }
        
      });
    },
  }
};
</script>

<style scoped>
.user-detail-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h1 {
  text-align: center;
  margin-bottom: 20px;
}

.error-message {
  color: red;
  text-align: center;
}

.user-info {
  margin-bottom: 20px;
}

.user-status {
  text-align: center;
  margin-bottom: 15px;
}

.status {
  font-size: 1.2em;
  font-weight: bold;
}

.info-details {
  margin-bottom: 15px;
}

.edit-button {
  display: block;
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  text-align: center;
  transition: background-color 0.3s;
}

.edit-button:hover {
  background-color: #0056b3;
}

/* Overlay */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

/* Form sửa thông tin */
.edit-form {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  max-width: 400px;
  width: 100%;
}

.form-group {
  display: flex;
  align-items: center; /* Canh giữa theo chiều dọc */
  margin-bottom: 15px;
}

.form-group label {
  flex: 0 0 150px; /* Chiều rộng cố định cho label */
  margin-right: 10px; /* Khoảng cách giữa label và input */
}

.form-group input {
  flex: 1; /* Để input chiếm không gian còn lại */
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.button-group {
  display: flex;
  justify-content: space-between;
}

.save-button {
  background-color: #28a745;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.save-button:hover {
  background-color: #218838;
}

.cancel-button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.cancel-button:hover {
  background-color: #c82333;
}
</style>
