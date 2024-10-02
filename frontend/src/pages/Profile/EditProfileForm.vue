<!-- eslint-disable vue/no-mutating-props -->
<template>
<div class="row">
  <div class="col-12">
  <card>
    <!-- CẬP NHẬT THÔNG TIN NGƯỜI DÙNG -->
    <h4 slot="header" class="title">Thông tin tài khoản</h4>
     <div class="row">
      <div class="col-md-6 pr-md-1">
        <base-input
          label="ID"
          v-model="model.user_id"
          placeholder="ID"
          disabled
        >
        </base-input>
      </div>
      <div class="col-md-6 pl-md-1">
        <base-input
          label="Họ và tên"
          v-model="model.full_name"
          placeholder="Họ và tên"
          disabled
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 pr-md-1">
        <base-input :class="{'has-danger': hasEmailError()}"
          label="Email"
          v-model="model.email"
          placeholder="example@gmail.com"
          type="email"
        >
        </base-input>
      </div>
      <div class="col-md-6 pl-md-1">
        <base-input
          label="Số điện thoại"
          v-model="model.phone_number"
          placeholder="SĐT"
        >
        </base-input>
      </div>
    </div>

    <div class="row">
      <div class="col-md-6 pr-md-1">
        <base-input label="Giới tính">
                <select v-model="model.sex" class="form-control">
                  <option>Nam</option>
                  <option>Nữ</option>
                  <option>Khác</option>
                </select>
          </base-input>
      </div>
      <div class="col-md-6 pl-md-1">
        <base-input
          label="Quốc tịch"
          v-model="model.nation"
          placeholder="Quốc tịch"
        >
        </base-input>
      </div>
    </div>

    <!-- <div class="row">
      <div class="col-md-5 pr-md-1">
        <base-input
          label="Company (disabled)"
          placeholder="Company"
          v-model="model.company"
          disabled
        >
        </base-input>
      </div>
      <div class="col-md-3 px-md-1">
        <base-input
          label="Username"
          placeholder="Username"
          v-model="model.username"
        >
        </base-input>
      </div>
      <div class="col-md-4 pl-md-1">
        <base-input
          label="Email address"
          type="email"
          placeholder="mike@email.com"
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-6 pr-md-1">
        <base-input
          label="First Name"
          v-model="model.firstName"
          placeholder="First Name"
        >
        </base-input>
      </div>
      <div class="col-md-6 pl-md-1">
        <base-input
          label="Last Name"
          v-model="model.lastName"
          placeholder="Last Name"
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-12">
        <base-input
          label="Address"
          v-model="model.address"
          placeholder="Home Address"
        >
        </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-4 pr-md-1">
        <base-input label="City" v-model="model.city" placeholder="City">
        </base-input>
      </div>
      <div class="col-md-4 px-md-1">
        <base-input
          label="Country"
          v-model="model.country"
          placeholder="Country"
        >
        </base-input>
      </div>
      <div class="col-md-4 pl-md-1">
        <base-input label="Postal Code" placeholder="ZIP Code"> </base-input>
      </div>
    </div>
    <div class="row">
      <div class="col-md-8">
        <base-input>
          <label>About Me</label>
          <textarea
            rows="4"
            cols="80"
            class="form-control"
            placeholder="Here can be your description"
            v-model="model.about"
          >
          </textarea>
        </base-input>
      </div>
    </div> -->
    <base-button @click="updateUser" type="primary" fill :disabled="this.hasEmailError()" >Lưu</base-button>
  </card>
</div>

<div class="col-12">
  <card>
    <!-- CẬP NHẬT THÔNG TIN NGƯỜI DÙNG -->
    <h4 slot="header" class="title">Đổi mật khẩu</h4>
    <div class="row">
      <div class="col-md-6 pr-md-1">
        <base-input
          label="Mật khẩu cũ"
          v-model="old_password"
          placeholder="Mật khẩu cũ"
        >
        </base-input>
      </div>
      <div class="col-md-6 pl-md-1">
        <base-input
          label="Mật khẩu mới"
          v-model="new_password"
          placeholder="Mật khẩu mới"
        >
        </base-input>
      </div>
    </div>

    <base-button @click="changePassword" type="success" fill  >Lưu</base-button>
  </card>
</div>

</div>

</template>
<script>
import axios from '../../services/axios'; 
// const API_URL = 'https://classroom50.online';
const API_URL = 'http://127.0.0.1:8000';

export default {
  data(){
    return {
      old_password: null,
      new_password: null,
    }
  },
  props: {
    model: {
      type: Object,
      default: () => {
        return {};
      },
    },
  },
  methods: {
    hasEmailError() {
    // Kiểm tra email với regex cơ bản để kiểm tra tính hợp lệ của email
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return !emailPattern.test(this.model.email);  // Nếu email không hợp lệ, trả về true
  },
    updateUser() {
      if(this.hasEmailError()){
        this.$notify({
          type: 'warning',
          message: "Email chưa chính xác",
          timeout: 3000,
          verticalAlign: 'top',
          horizontalAlign: 'right',
        });
        return;
      }

      const token = localStorage.getItem('access_token');
      const updateData = {
          full_name: this.model.full_name,
          sex: this.model.phone_number,
          nation: this.model.day_of_birth,
          email: this.model.email,
          phone_number: this.model.phone_number,
          day_of_birth: this.model.day_of_birth,
          active_status: "Active"
    };

      axios.patch(API_URL+'/accounts/update/', updateData, {
        headers: {
          'Authorization': `Bearer ${token}`, // Đính kèm token vào headers
          'Content-Type': 'application/json',
        }
      })
      .then(() => {
        this.$notify({
          type: 'success',
          message: "Cập nhật thông tin người dùng thành công",
          timeout: 3000,
          verticalAlign: 'top',
          horizontalAlign: 'right',
        });
      })
      .catch(error => {
        console.error("Error updating user data:", error);
        this.$notify({
          type: 'warning',
          message: "Cập nhật thông tin người dùng thất bại",
          timeout: 3000,
          verticalAlign: 'top',
          horizontalAlign: 'right',
        });
      });
    },
    changePassword() {
      if(!this.old_password){
        this.$notify({
            type: 'warning',
            message: "Vui lòng nhập mật khẩu cũ",
            timeout: 3000,
            verticalAlign: 'top',
            horizontalAlign: 'right',
          });
          return;
      }
      if(!this.new_password){
        this.$notify({
            type: 'warning',
            message: "Vui lòng nhập mật khẩu mới",
            timeout: 3000,
            verticalAlign: 'top',
            horizontalAlign: 'right',
          });
          return;
      }

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
          type: 'success',
          message: response.data.detail,
          timeout: 3000,
          verticalAlign: 'top',
          horizontalAlign: 'right',
        });

        this.old_password = null;
        this.new_password = null;
      })
      .catch(error => {
        console.error("Error change password user :", error);
        
        if (error.response && error.response.data){
          this.$notify({
              type: 'danger',
              message: error.response.data.old_password || error.response.data.new_password || 'Có lỗi xảy ra khi đổi mật khẩu.',
              timeout: 3000,
              verticalAlign: 'top',
              horizontalAlign: 'right',
            });
        }else {
          this.$notify({
            type: 'danger',
            message: "Đổi mật khẩu không thành công. Vui lòng thử lại !",
            timeout: 3000,
            verticalAlign: 'top',
            horizontalAlign: 'right',
          });
        }
        
      });
    },
  }
};
</script>
<style></style>
