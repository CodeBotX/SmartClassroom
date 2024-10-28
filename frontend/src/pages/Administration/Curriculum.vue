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
              <td>{{ row.name }}</td>
              <td>{{ row.day_begin }}</td>
              <td>{{ row.number_of_weeks }}</td>
              <td class="td-actions text-right">
                <base-button type="success" size="sm" icon @click="toggleUpdate(row.name)">
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon @click="toggleRemove(row.name)">
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td>
            </template>
          </base-table>
        </div>

        <!-- Lớp học -->
        <div v-if="bigLineChart.activeIndex === 1">
          <base-table :data="roomData" :columns="room_columns">
            <template slot="columns">
              <th>Lớp học</th>
              <th>Sĩ số lớp</th>
              <th>Giáo viên chủ nhiệm</th>
              <!-- <th class="text-right">Actions</th> -->
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.name }}</td>
              <td>{{ row.students.length }}</td>
              <td>{{ row.homeroom_teacher }}</td>
              <!-- <td class="td-actions text-right">
                <base-button type="success" size="sm" icon @click="toggleUpdate(row.name)">
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon @click="toggleRemove(row.name)">
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td> -->
            </template>
          </base-table>
        </div>

        <!-- Update Modal -->
        <modal :show.sync="modals.updateModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
               <!-- Semester -->
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Cập nhật học kỳ</h4>
                    </div>
                </template>
                <template v-if="modals.semesterDetail">
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Học kỳ" v-model="modals.semesterDetail.name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày bắt đầu" v-model="modals.semesterDetail.day_begin" type="date"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Số tuần" v-model="modals.semesterDetail.number_of_weeks"></base-input>
                                    </div>
                                </div>
                                <base-button @click="updateObject" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>

            <!-- PlannedLessson -->

            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 2">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Cập nhật bài giảng</h4>
                    </div>
                </template>
                <template v-if="modals.plannedLessonDetail">
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Môn">
                                          <select class="form-control" v-model="modals.plannedLessonDetail.subject">
                                            <option class="text-info" v-for="(subject, index) in subjects" :key="index">{{subject}}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Học kỳ">
                                          <select class="form-control" v-model="modals.plannedLessonDetail.semester">
                                            <option class="text-info" v-for="(semester, index) in semesters" :key="index" :value="semester.name">{{ semester.name }}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Bài số" v-model="modals.plannedLessonDetail.lesson_number"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Tên bài" v-model="modals.plannedLessonDetail.name_lesson"></base-input>
                                    </div>
                                </div>
                                <base-button @click="updateObject" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>

        <!-- Remove Modal -->
        <modal :show.sync="modals.removeModal">
            <h4 slot="header" class="modal-title" id="modal-title-default" v-if="this.bigLineChart.activeIndex === 0">Xóa nhận xóa học kỳ này </h4>
            <h4 slot="header" class="modal-title" id="modal-title-default" v-if="this.bigLineChart.activeIndex === 2">Xóa nhận xóa bài giảng này </h4>
            <template slot="footer">
                <base-button type="secondary" @click="removeObject">Xác nhận</base-button>
                <base-button type="danger" class="ml-auto" @click="modals.removeModal = false">Hủy
                </base-button>
            </template>
        </modal>

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
                <base-button type="success" size="sm" icon @click="toggleUpdate(row.id)">
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon @click="toggleRemove(row.id)">
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
  mounted() {
      this.initializeData();
  },
  data() {
    return {
    modals: {
        updateModal: false,
        removeModal: false,
        idRemove: null,

        teacherModal: false,
        parentModal: false,
        semesterDetail: null,
        teacherDetail: null,
        plannedLessonDetail: null,
    },
    subjects: ['TOAN', 'VAN', 'ANH', 'HOA', 'LY', 'SINH', 'DIA', 'SU', 'GDCD', 'TD', 'MT', 'AN', 'TH', 'CN', 'HDTN-HN'],
    semester_columns: ["semester", "day_begin", "number_of_weeks"],
    room_columns: ["name", "students", "homeroom_teacher"],
    plannedlesson_columns: ["id", "subject", "lesson_number", "name_lesson", "semester"],
    lesson_columns: ["user", "full_name", "sex", "day_of_birth", "description"],
      semesterData: null,
      roomData: null,
      plannedlessonData: null,
      lessonData: null,
      deviceData: null,
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
    async initializeData() {
        try {
          await this.getApiUrl();
          await this.getSemesterData();
        } catch (error) {
          console.error('Error initializing data:', error);
        }
      },
      getApiUrl() {
        return new Promise((resolve) => {
          API_URL = this.$t("dashboard.apiURL");
          resolve();
        });
      },
      getSemesterData() {
        if (this.semesters) return;
        const token = localStorage.getItem("access_token");

        axios
          .get(API_URL + "/adminpanel/semesters/", {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.semesters = response.data;
          })
          .catch((error) => {
            console.error("Error getting semester data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy dữ liệu học kỳ thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
    removeObject(){
        const token = localStorage.getItem("access_token");

        let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
        if (this.bigLineChart.activeIndex === 0) {
          apiUrl = API_URL + "/adminpanel/semesters/" + this.modals.idRemove + "/";
        } else if (this.bigLineChart.activeIndex === 2) {
          apiUrl = API_URL + "/adminpanel/planned-lessons/" + this.modals.idRemove + "/";
        }

        axios
        .delete(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          let message = "";

          if (this.bigLineChart.activeIndex === 0) {
            message = "Xóa học kỳ thành công"
          } else if (this.bigLineChart.activeIndex === 2) {
            message = "Xóa bài giảng thành công"
          }
            this.$notify({
                type: "success",
                icon: 'tim-icons icon-check-2',
                message: message,
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
          this.modals.removeModal = false
          this.initBigChart(this.bigLineChart.activeIndex)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                message: "Xóa dữ liệu thất bại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    updateObject(){
        let data = null;
        let apiUrl = "";
        // const data = this.modals.studentDetail;

        if(this.bigLineChart.activeIndex ===0 ){
          apiUrl = API_URL + `/adminpanel/semesters/${this.modals.semesterDetail.name}/`
          data = this.modals.semesterDetail
        } else if (this.bigLineChart.activeIndex === 1) {
          apiUrl = API_URL + "/accounts/teachers/" + this.modals.teacherDetail.user + "/";
          data = this.modals.teacherDetail
        } else if (this.bigLineChart.activeIndex === 2) {
          apiUrl = API_URL + "/adminpanel/planned-lessons/" + this.modals.plannedLessonDetail.id + "/";
          data = this.modals.plannedLessonDetail
        }
        const token = localStorage.getItem("access_token");
        axios
        .patch(apiUrl, data, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          let message = "";
          if (this.bigLineChart.activeIndex === 0) {
            this.modals.semesterDetail = response.data
            message = "Cập nhật thông tin học kỳ thành công"
          } else if (this.bigLineChart.activeIndex === 1) {
            this.modals.teacherDetail = response.data
            message = "Cập nhật thông tin giáo viên thành công"
          } else if (this.bigLineChart.activeIndex === 2) {
            this.modals.plannedLessonDetail = response.data
            message = "Cập nhật thông tin bài giảng thành công"
          }

            this.$notify({
                type: "success",
                icon: 'tim-icons icon-check-2',
                message: message,
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });

          this.modals.updateModal = false
          this.initBigChart(this.bigLineChart.activeIndex)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                message: "Dữ liệu không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleUpdate(index){
        this.modals.updateModal = true;

        let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
        if (this.bigLineChart.activeIndex === 0) {
          apiUrl = API_URL + "/adminpanel/semesters/" + index + "/";
        } else if (this.bigLineChart.activeIndex === 1) {
          apiUrl = API_URL + "/accounts/teachers/" + index + "/";
        } else if (this.bigLineChart.activeIndex === 2) {
          apiUrl = API_URL + "/adminpanel/planned-lessons/" + index + "/";
        }

        const token = localStorage.getItem("access_token");
        axios
        .get(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {

          if (this.bigLineChart.activeIndex === 0) {
            this.modals.semesterDetail = response.data
          } else if (this.bigLineChart.activeIndex === 1) {
            this.modals.teacherDetail = response.data
          } else if (this.bigLineChart.activeIndex === 2) {
            this.modals.plannedLessonDetail = response.data
          }
        })
        .catch((error) => {
          console.error("Error get data :", error);

          this.$notify({
                type: "warning",
                message: "Dữ liệu không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleRemove(index){
        this.modals.removeModal = true;
        this.modals.idRemove = index;
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
        apiUrl = API_URL + "/rooms/roomset/";
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
          else if(this.bigLineChart.activeIndex === 1) this.roomData = response.data
          else if(this.bigLineChart.activeIndex === 2) this.plannedlessonData = response.data
          else if(this.bigLineChart.activeIndex === 3) this.deviceData = response.data
          
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
  },
};
</script>

<style>
</style>