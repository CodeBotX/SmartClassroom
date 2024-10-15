<template>
  <div class="row">
    <div class="col-12">
      <card>
        <template slot="header">
          <h3>Chương trình đào tạo</h3>
          <div class="col-sm-12">
            <div
              class="btn-group btn-group-toggle float-right"
              data-toggle="buttons"
            >
              <label
                v-for="(option, index) in curriculumOption"
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

        <!-- HỌC KỲ -->
        <div v-if="bigLineChart.activeIndex === 0">
          <base-table :data="semesterData" :columns="semester_columns">
            <template slot="columns">
              <th>Học kỳ</th>
              <th>Ngày bắt đầu</th>
              <th>Số tuần học</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.semester }}</td>
              <td>{{ row.day_begin }}</td>
              <td>{{ row.number_of_weeks }}</td>
              <td class="td-actions text-right">
                <base-button type="info" size="sm" icon @click="toggleStudentDetail(row.user)">
                  <i class="tim-icons icon-single-02"></i>
                </base-button>
                <base-button type="success" size="sm" icon @click="toggleStudentUpdate(row.user)">
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon @click="toggleStudentRemove(row.user)">
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td>
            </template>
          </base-table>
        </div>
        <!-- Student Detail Modal -->
        <modal :show.sync="modals.studentDetailModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thông tin học sinh</h4>
                    </div>
                </template>
                <template v-if="modals.studentDetail">
                    <fieldset disabled>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="modals.studentDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="modals.studentDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Lớp" v-model="modals.studentDetail.room"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Giới tính" v-model="modals.studentDetail.sex"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày sinh" v-model="modals.studentDetail.day_of_birth"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Trạng thái" v-model="modals.studentDetail.active_status"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Phụ huynh" v-model="modals.studentDetail.parent"></base-input>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>  
                </template>
            </card>
        </modal>

        <!-- Student Update Modal -->
        <modal :show.sync="modals.studentUpdateModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Cập nhật học sinh</h4>
                    </div>
                </template>
                <template v-if="modals.studentDetail">
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="modals.studentDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="modals.studentDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Lớp" v-model="modals.studentDetail.room"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Giới tính" v-model="modals.studentDetail.sex"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày sinh" v-model="modals.studentDetail.day_of_birth"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Trạng thái" v-model="modals.studentDetail.active_status"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Phụ huynh" v-model="modals.studentDetail.parent"></base-input>
                                    </div>
                                </div>
                                <base-button @click="updateStudent" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>

        <!-- Student Remove Modal -->
        <modal :show.sync="modals.studentRemoveModal">
            <h4 slot="header" class="modal-title" id="modal-title-default">Xác nhận xóa học sinh này</h4>
            <template slot="footer">
                <base-button type="secondary" @click="removeStudent">Xác nhận</base-button>
                <base-button type="danger" class="ml-auto" @click="modals.studentRemoveModal = false">Hủy
                </base-button>
            </template>
        </modal>

        <!-- STUDY WEEK -->
        <div v-if="bigLineChart.activeIndex === 1">
          <base-table :data="studyweekData" :columns="studyweek_columns">
            <template slot="columns">
              <th>ID</th>
              <th>Họ và tên</th>
              <th>Giới tính</th>
              <th>Ngày sinh</th>
              <th>Môn dạy</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.user }}</td>
              <td>{{ row.full_name }}</td>
              <td>{{ row.sex }}</td>
              <td>{{ row.day_of_birth }}</td>
              <td>{{ row.subjects }}</td>
              <td class="td-actions text-right">
                <base-button type="info" size="sm" icon>
                  <i class="tim-icons icon-single-02"></i>
                </base-button>
                <base-button type="success" size="sm" icon>
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon>
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td>
            </template>
          </base-table>
        </div>

        <!-- BÀI GIẢNG -->
        <div v-if="bigLineChart.activeIndex === 2">
          <base-table :data="plannedlessonData" :columns="plannedlesson_columns">
            <template slot="columns">
              <th>ID</th>
              <th>Môn học</th>
              <th>Bài số</th>
              <th>Tên bài học</th>
              <th>Học kỳ</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.id }}</td>
              <td>{{ row.subject }}</td>
              <td>{{ row.lesson_number }}</td>
              <td>{{ row.name_lesson }}</td>
              <td>{{ row.semester }}</td>
              <td class="td-actions text-right">
                <base-button type="info" size="sm" icon>
                  <i class="tim-icons icon-single-02"></i>
                </base-button>
                <base-button type="success" size="sm" icon>
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon>
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td>
            </template>
          </base-table>
        </div>

        <!-- ADMIN -->
        <div v-if="bigLineChart.activeIndex === 3">
          <base-table :data="adminData" :columns="admin_columns">
            <template slot="columns">
              <th>ID</th>
              <th>Họ và tên</th>
              <th>Giới tính</th>
              <th>Ngày sinh</th>
              <th>Chức vụ</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.user }}</td>
              <td>{{ row.full_name }}</td>
              <td>{{ row.sex }}</td>
              <td>{{ row.day_of_birth }}</td>
              <td>{{ row.description }}</td>
              <td class="td-actions text-right">
                <base-button type="info" size="sm" icon>
                  <i class="tim-icons icon-single-02"></i>
                </base-button>
                <base-button type="success" size="sm" icon>
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon>
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td>
            </template>
          </base-table>
        </div>

      </card>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";
let API_URL = ""

import config from "@/config";
import Card from "../../components/Cards/Card.vue";
import BaseTable from '../../components/BaseTable.vue';
import Modal from '../../components/Modal.vue';
import BaseInput from '../../components/Inputs/BaseInput.vue';


export default {
  components: { Card, BaseTable, Modal, BaseInput },
  computed: {
    getApiUrl() {
      API_URL =  this.$t("dashboard.apiURL");
    },
  },
  data() {
    return {
    modals: {
        studentDetailModal: false,
        studentUpdateModal: false,
        studentRemoveModal: false,
        idStudentRemove: null,

        teacherModal: false,
        parentModal: false,
        studentDetail: null,
        teacherDetail: null,
        parentDetail: null,
    },
    semester_columns: ["semester", "day_begin", "number_of_weeks"],
    studyweek_columns: ["user", "full_name", "sex", "day_of_birth", "subjects", "actions"],
    plannedlesson_columns: ["id", "subject", "lesson_number", "name_lesson", "semester"],
    lesson_columns: ["user", "full_name", "sex", "day_of_birth", "description"],
      semesterData: null,
      studyweekData: null,
      plannedlessonData: null,
      lessonData: null,
      gradeData: null,
      bigLineChart: {
        allData: [
          [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100],
          [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120],
          [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130],
        ],
        activeIndex: null,
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
    curriculumOption() {
      return this.$t("dashboard.curriculum");
    },
  },
  methods: {
    removeStudent(){
        const token = localStorage.getItem("access_token");
        axios
        .delete(API_URL+"/accounts/students/"+this.modals.idStudentRemove+"/", {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
            this.$notify({
                type: "success",
                message: "Xóa học sinh thành công",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
          this.modals.studentRemoveModal = false
          this.initBigChart(0)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    updateStudent(){
        const dataUser = this.modals.studentDetail;

        const token = localStorage.getItem("access_token");
        axios
        .patch(API_URL+"/accounts/students/"+this.modals.studentDetail.user+"/", dataUser, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
            this.$notify({
                type: "success",
                message: "Cập nhật thông tin học sinh thành công",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });

          this.modals.studentDetail = response.data

          this.initBigChart(0)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleStudentDetail(index){
        this.modals.studentDetailModal = true;

        const token = localStorage.getItem("access_token");
        axios
        .get(API_URL+"/accounts/students/"+index+"/", {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.modals.studentDetail = response.data
          console.log(this.modals.studentDetail)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleStudentUpdate(index){
        this.modals.studentUpdateModal = true;

        const token = localStorage.getItem("access_token");
        axios
        .get(API_URL+"/accounts/students/"+index+"/", {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.modals.studentDetail = response.data
          console.log(this.modals.studentDetail)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleStudentRemove(index){
        this.modals.studentRemoveModal = true;
        this.modals.idStudentRemove = index;
    },
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
    
      let apiUrl = ""; 
      if (this.bigLineChart.activeIndex === 0) {
        apiUrl = API_URL + "/adminpanel/semesters/";
      } else if (this.bigLineChart.activeIndex === 1) {
        apiUrl = API_URL + "/adminpanel/studyweeks/";
      } else if (this.bigLineChart.activeIndex === 2) {
        apiUrl = API_URL + "/adminpanel/planned-lessons/";
      } else if (this.bigLineChart.activeIndex === 3) {
        apiUrl = API_URL + "/adminpanel/lessons/";
      } else if (this.bigLineChart.activeIndex === 4) {
        apiUrl = API_URL + "/adminpanel/grades/";
      }

      //Get data
      const token = localStorage.getItem("access_token");
      axios
        .get(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          if(this.bigLineChart.activeIndex === 0) this.semesterData = response.data
          else if(this.bigLineChart.activeIndex === 1) this.studyweekData = response.data
          else if(this.bigLineChart.activeIndex === 2) this.plannedlessonData = response.data
          else if(this.bigLineChart.activeIndex === 3) this.lessonData = response.data
          else if(this.bigLineChart.activeIndex === 4) this.gradeData = response.data
          
        })
        .catch((error) => {
          console.error("Error get data :", error);

          this.$notify({
                type: "warning",
                message: "Lấy dữ liệu thất bại. Vui lòng thử lại sau",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
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
                group: "auth",
                title: "Thông báo",
                text: "Bạn không có quyền thực hiện thao tác này",
                type: "warn",
                duration: 3000,
              });
            }
            if (error.response.status === 404) {
              this.$notify({
                type: "warning",
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
            }
          } else {
            this.$notify({
              type: "danger",
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
          message: "Vui lòng tải lên tệp Excel",
          timeout: 3000,
          verticalAlign: "top",
          horizontalAlign: "center",
        });
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
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
        })
        .then((response) => {
          this.$notify({
            type: "success",
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
                  message: errorMessage,
                  timeout: 3000,
                  verticalAlign: "top",
                  horizontalAlign: "right",
                });
              } else {
                const errorMessage =
                  "Vui lòng kiểm tra lại cấu trúc file và loại đối tượng đăng ký ";
                this.$notify({
                  type: "danger",
                  message: errorMessage,
                  timeout: 3000,
                  verticalAlign: "top",
                  horizontalAlign: "right",
                });
              }
            } else {
              // Thông báo lỗi nếu không nhận được phản hồi cụ thể từ backend
              this.$notify({
                type: "danger",
                message: "Lỗi không xác định. Vui lòng thử lại.",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
            }
          } else {
            this.$notify({
              type: "warning",
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