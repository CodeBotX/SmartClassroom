<template>
  <div class="row">
    <div class="col-12">
      <card>
        <template slot="header">
          <h3>Quản trị tài khoản</h3>
          <div class="col-sm-12">
            <div
              class="btn-group btn-group-toggle float-right"
              data-toggle="buttons"
            >
              <label
                v-for="(option, index) in accountSettingOption"
                :key="option"
                class="btn btn-sm btn-success btn-simple"
                :class="{ active: bigLineChart.activeIndex === index }"
                :id="index"
              >
                <input
                  type="radio"
                  @click="initBigChart(index)"
                  name="options"
                  autocomplete="off"
                  :checked="bigLineChart.activeIndex === index"
                />
                {{ option }}
              </label>
            </div>
          </div>
        </template>

        <!-- ĐỔI MẬT KHẨU -->
        <div v-if="bigLineChart.activeIndex === 0">
          <h4 class="title text-success">
            Reset mật khẩu
          </h4>
          <div class="row">
            <div class="col-md-6 pr-md-1">
              <base-input
                label="ID Người dùng"
                v-model="id_user_reset"
                placeholder="ID"
              >
              </base-input>
            </div>
          </div>

          <base-button @click="resetPassword" type="success" fill
            >Xác nhận</base-button
          >
        </div>

        <!-- ĐĂNG KÝ TÀI KHOẢN -->
        <div v-if="bigLineChart.activeIndex === 1">
          <h4 class="title text-success">Đăng ký tài khoản</h4>

          <!-- Choose registration type -->
          <div class="row">
            <div class="col-md-6 pr-md-1">
              <label for="registrationType">Loại đăng ký</label>
              <select v-model="registrationType" class="form-control" id="registrationType">
                <option class="text-info" value="teacher">Giáo viên</option>
                <option class="text-info" value="student">Học sinh</option>
                <option class="text-info" value="parent">Phụ huynh</option>
              </select>
            </div>
          </div>

          <!-- Hidden File Input -->
          <input
            type="file"
            ref="fileInput"
            @change="handleFileUpload"
            style="display: none"
          />

          <!-- Button to Upload File -->
          <div class="row mt-4">
            <div class="col-md-6 pr-md-1">
              <base-button type="success" @click="triggerFileUpload" simple>
              <i class="tim-icons icon-attach-87"></i> Upload file Excel
              </base-button>
              <p v-if="selectedFile">{{ selectedFile.name }}</p>
            </div>
          </div>

          <base-button @click="registerAccounts" type="success" fill>Xác nhận</base-button>
        </div>
      </card>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";
// const API_URL = 'https://classroom50.online';
// const API_URL = "http://127.0.0.1:8000";
let API_URL = ""

import config from "@/config";
import Card from "../../components/Cards/Card.vue";
export default {
  components: { Card },
  computed: {
    getApiUrl() {
      API_URL =  this.$t("dashboard.apiURL");
    },
  },
  data() {
    return {
      id_user_reset: null,
      registrationType: "teacher", // Default registration type
      selectedFile: null, // For file upload
      bigLineChart: {
        allData: [
          [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100],
          [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120],
          [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130],
        ],
        activeIndex: 0,
        index: "Quản trị",
        chartData: {
          datasets: [{}],
          labels: [
            "JAN",
            "FEB",
            "MAR",
            "APR",
            "MAY",
            "JUN",
            "JUL",
            "AUG",
            "SEP",
            "OCT",
            "NOV",
            "DEC",
          ],
        },

        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: [],
      },
    };
  },
  computed: {
    accountSettingOption() {
      return this.$t("dashboard.accountSetting");
    },
  },
  methods: {
    initBigChart(index) {
      let chartData = {
        datasets: [
          {
            fill: true,
            borderColor: config.colors.primary,
            borderWidth: 2,
            borderDash: [],
            borderDashOffset: 0.0,
            pointBackgroundColor: config.colors.primary,
            pointBorderColor: "rgba(255,255,255,0)",
            pointHoverBackgroundColor: config.colors.primary,
            pointBorderWidth: 20,
            pointHoverRadius: 4,
            pointHoverBorderWidth: 15,
            pointRadius: 4,
            data: this.bigLineChart.allData[index],
          },
        ],
        labels: [
          "JAN",
          "FEB",
          "MAR",
          "APR",
          "MAY",
          "JUN",
          "JUL",
          "AUG",
          "SEP",
          "OCT",
          "NOV",
          "DEC",
        ],
      };

      this.bigLineChart.chartData = chartData;
      this.bigLineChart.activeIndex = index;
      if (index === 0) this.bigLineChart.index = "Reset password";
      if (index === 1) this.bigLineChart.index = "Option2";
      if (index === 2) this.bigLineChart.index = "Option3";
    },
    resetPassword() {
      const token = localStorage.getItem("access_token");
      const resetPasswordData = {
        user_id: this.id_user_reset,
      };

      axios
        .post(API_URL + "/accounts/admin-reset-password/", resetPasswordData, {
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
          this.isEditingResetPassword = false; // Tắt chế độ chỉnh sửa

          this.user_id_reset = null;
        })
        .catch((error) => {
          console.error("Error reset password user :", error);

          // this.isEditingPassword = false; // Tắt chế độ chỉnh sửa
          if (error.response && error.response.data) {
            if (error.response.status === 401) {
              this.$notify({
                type: "danger",
                icon: 'tim-icons icon-alert-circle-exc',
                message: "Bạn không có quyền thực hiện thao tác này.",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
            }
            if (error.response.status === 404) {
              this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
            }
          } else {
            this.$notify({
              type: "danger",
              icon: 'tim-icons icon-bell-55',
              message: "Reset mật khẩu không thành công. Vui lòng thử lại sau.",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          }
        });
    },
    triggerFileUpload() {
      this.$refs.fileInput.click(); // Trigger file input click event
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0]; // Get selected file
    },
    registerAccounts() {
      if (!this.selectedFile) {
        this.$notify({
          type: "warning",
          icon: 'tim-icons icon-bell-55',
          message: "Vui lòng tải lên tệp Excel",
          timeout: 3000,
          verticalAlign: "top",
          horizontalAlign: "center",
        });
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      let apiUrl = "";
      if (this.registrationType === "student") {
        apiUrl = API_URL + "/accounts/register-student/";
      } else if (this.registrationType === "teacher") {
        apiUrl = API_URL + "/accounts/register-teacher/";
      } else if (this.registrationType === "parent") {
        apiUrl = API_URL + "/accounts/register-parent/";
      }

      const token = localStorage.getItem("access_token");

      axios
        .post(apiUrl, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
          timeout: 100000,
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
        })
        .catch((error) => {
          console.error("Error registering accounts:", error);
          if (error.response) {
            if (error.response && error.response.data) {
          // Kiểm tra lỗi validate_file từ backend
          if (error.response.data.file) {
            const errorMessage = error.response.data.file[0]; // Lấy thông báo lỗi từ trường file
            this.$notify({
              type: "danger",
              icon: 'tim-icons icon-bell-55',
              message: errorMessage,
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          } else {
            const errorMessage = "Vui lòng kiểm tra lại cấu trúc file và loại đối tượng đăng ký ";
            console.error("Error registering accounts:", error);
            this.$notify({
              type: "danger",
              icon: 'tim-icons icon-bell-55',
              message: error.response.data,
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          }
        } else {
          // Thông báo lỗi nếu không nhận được phản hồi cụ thể từ backend
          this.$notify({
            type: "danger",
            icon: 'tim-icons icon-alert-circle-exc',
            message: "Lỗi không xác định. Vui lòng thử lại.",
            timeout: 3000,
            verticalAlign: "top",
            horizontalAlign: "right",
          });
        }
          } else {
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Có lỗi xảy ra. Vui lòng thử lại sau",
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

<style>
</style>