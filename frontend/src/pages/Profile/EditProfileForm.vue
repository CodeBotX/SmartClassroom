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

        <div class="row" v-if="model.role === 'teachers' || model.role === 'admins'">
          <div class="col-md-12 pr-md-1">
            <base-input
              label="Chức vụ"
              v-model="model.contract_types"
              placeholder="Chức vụ"
              disabled
            >
            </base-input>
          </div>
        </div>

        <div class="row" v-if="model.role === 'teachers' || model.role === 'admins'">
          <div class="col-md-6 pr-md-1">
            <base-input
              label="Học vấn"
              v-model="model.expertise_levels"
              placeholder="Học vấn"
              disabled
            >
            </base-input>
          </div>
          <div class="col-md-6 pl-md-1">
            <base-input
              label="Môn dạy"
              v-model="model.subjects"
              placeholder=""
              disabled
            >
            </base-input>
          </div>
        </div>

        <div class="row">
          <div class="col-md-6 pr-md-1">
            <base-input
              :class="{ 'has-danger': hasEmailError() }"
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
          <div class="col-md-4 pr-md-1">
            <base-input label="Giới tính">
              <select v-model="model.sex" class="form-control">
                <option>Nam</option>
                <option>Nữ</option>
                <option>Khác</option>
              </select>
            </base-input>
          </div>
          <div class="col-md-4 pl-md-1">
            <base-input
              label="Dân tộc"
              v-model="model.nation"
              placeholder="Dân tộc"
            >
            </base-input>
          </div>
          <div class="col-md-4 pl-md-1">
            <base-input
              label="Ngày sinh"
              v-model="model.day_of_birth"
              placeholder="Ngày sinh"
              type="date"
            >
            </base-input>
          </div>
        </div>

        <base-button
          @click="updateUser"
          type="success"
          fill
          :disabled="this.hasEmailError()"
          >Lưu</base-button
        >
      </card>
    </div>

    <div class="col-12">
      <card>
        <!-- ĐỔI MẬT KHẨU -->
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

        <base-button @click="changePassword" type="success" fill
          >Lưu</base-button
        >
      </card>
    </div>
  </div>
</template>
<script>
import axios from "../../services/axios";
let API_URL = ""

export default {
  data() {
    return {
      old_password: null,
      new_password: null,
    };
  },
  computed: {
    getApiUrl() {
      API_URL =  this.$t("dashboard.apiURL");
    },
  },
  mounted() {},
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
      return !emailPattern.test(this.model.email); // Nếu email không hợp lệ, trả về true
    },
    updateUser() {
      if (this.hasEmailError()) {
        this.$notify({
          type: "warning",
          icon: 'tim-icons icon-bell-55',
          message: "Email chưa chính xác",
          timeout: 3000,
          verticalAlign: "top",
          horizontalAlign: "right",
        });
        return;
      }

      const token = localStorage.getItem("access_token");

      let updateDataUser = null;
      if (this.model.old_email === this.model.email) {
        if (this.model.old_phone_number !== this.model.phone_number) { 
          updateDataUser = {
            phone_number: this.model.phone_number,
          };
          this.model.old_phone_number = this.model.phone_number
        }
      } else if (this.model.old_phone_number !== this.model.phone_number) {
        updateDataUser = {
          email: this.model.email,
          phone_number: this.model.phone_number,
        };
        this.model.old_phone_number = this.model.phone_number
        this.model.old_email = this.model.email
      } else {
        updateDataUser = {
          email: this.model.email,
        };
        this.model.old_email = this.model.email
      }
      // updateDataUser = {
      //     email: this.model.email,
      //     phone_number: this.model.phone_number,
      // };
      const updateDataRole = {
        sex: this.model.sex,
        nation: this.model.nation,
        email: this.model.email,
        phone_number: this.model.phone_number,
        day_of_birth: this.model.day_of_birth,
      };

      const requests = [];

      if (updateDataUser !== null) {
        requests.push(
          axios.patch(
            API_URL + "/accounts/users/" + this.model.user_id + "/",
            updateDataUser,
            {
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            }
          )
        );
      }

      // Always add the second API call
      requests.push(
        axios.patch(
          API_URL +
            "/accounts/" +
            this.model.role +
            "/" +
            this.model.user_id +
            "/",
          updateDataRole,
          {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          }
        )
      );

      Promise.all(requests)
        .then(() => {
          this.$notify({
            type: "success",
            icon: 'tim-icons icon-check-2',
            message: "Cập nhật thông tin người dùng thành công",
            timeout: 3000,
            verticalAlign: "top",
            horizontalAlign: "right",
          });
          console.log(this.model);
        })
        .catch((error) => {
          console.error("Error updating user data:", error.response.data);
          if (error.response.data.email) {
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Email đã tồn tại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          }
          if (error.response.data.phone_number) {
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Số điện thoại đã tồn tại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          }
          // else {
          //   this.$notify({
          //   type: 'danger',
          //   message: "Có lỗi xảy ra. Vui lòng thử lại sau",
          //   timeout: 3000,
          //   verticalAlign: 'top',
          //   horizontalAlign: 'right',
          // });
          // }
        });
    },
    changePassword() {
      if (!this.old_password) {
        this.$notify({
          type: "warning",
          icon: 'tim-icons icon-bell-55',
          message: "Vui lòng nhập mật khẩu cũ",
          timeout: 3000,
          verticalAlign: "top",
          horizontalAlign: "right",
        });
        return;
      }
      if (!this.new_password) {
        this.$notify({
          type: "warning",
          icon: 'tim-icons icon-bell-55',
          message: "Vui lòng nhập mật khẩu mới",
          timeout: 3000,
          verticalAlign: "top",
          horizontalAlign: "right",
        });
        return;
      }

      const token = localStorage.getItem("access_token");
      const changePasswordData = {
        old_password: this.old_password,
        new_password: this.new_password,
      };

      axios
        .post(API_URL + "/accounts/change-password/", changePasswordData, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.$notify({
            type: "success",
            icon: 'tim-icons icon-check-2',
            message: response.data.detail,
            timeout: 3000,
            verticalAlign: "top",
            horizontalAlign: "right",
          });

          this.old_password = null;
          this.new_password = null;
        })
        .catch((error) => {
          console.error("Error change password user :", error);

          if (error.response && error.response.data) {
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message:
                error.response.data.old_password[0] ||
                error.response.data.new_password[0] ||
                "Có lỗi xảy ra khi đổi mật khẩu.",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          } else {
            this.$notify({
              type: "danger",
              icon: 'tim-icons icon-bell-55',
              message: "Đổi mật khẩu không thành công. Vui lòng thử lại !",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          }
        });
    },
  },
};
</script>
<style></style>
