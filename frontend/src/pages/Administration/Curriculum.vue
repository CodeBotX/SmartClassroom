<template>
  <div class="row">
    <div class="col-12">
      <card>
        <template slot="header">
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

        <!-- Device -->
        <!-- <div v-if="bigLineChart.activeIndex === 2">
          <base-table :data="deviceData" :columns="device_columns">
            <template slot="columns">
              <th>ID thiết bị</th>
              <th>Phòng học</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.device_id }}</td>
              <td>{{ row.room }}</td>
            </template>
          </base-table>
        </div> -->

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
          <base-button type="default" size="sm" icon @click="toggleCreate()">
                  <i class="tim-icons icon-simple-add"></i>
          </base-button>
        </div>

        <!-- Create Modal -->
        <modal :show.sync="modals.createModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
               <!-- Semester -->
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thêm học kỳ</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Học kỳ" v-model="modals.semesterCreate.name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày bắt đầu" v-model="modals.semesterCreate.day_begin" type="date"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Số tuần" v-model="modals.semesterCreate.number_of_weeks"></base-input>
                                    </div>
                                </div>
                                <base-button @click="createObject" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>

            <!-- PlannedLessson -->

            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 1">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thêm bài giảng</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-4 pr-md-1">
                                        <base-input label="Môn">
                                          <select class="form-control" v-model="modals.plannedLessonCreate.subject">
                                            <option class="text-info" v-for="(subject, index) in subjects" :key="index">{{subject}}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                    <div class="col-md-4 pl-md-1">
                                        <base-input label="Học kỳ">
                                          <select class="form-control" v-model="modals.plannedLessonCreate.semester">
                                            <option class="text-info" v-for="(semester, index) in semesters" :key="index" :value="semester.name">{{ semester.name }}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                    <div class="col-md-4 pl-md-1">
                                        <base-input label="Lớp">
                                          <select class="form-control" v-model="modals.plannedLessonCreate.room">
                                            <option class="text-info" v-for="(room, index) in rooms" :key="index" :value="room.name">{{ room.name }}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Bài số" type="number" v-model="modals.plannedLessonCreate.lesson_number"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Tên bài" v-model="modals.plannedLessonCreate.name_lesson"></base-input>
                                    </div>
                                </div>
                                <base-button @click="createObject" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>

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
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 1">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Cập nhật bài giảng</h4>
                    </div>
                </template>
                <template v-if="modals.plannedLessonDetail">
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-4 pr-md-1">
                                        <base-input label="Môn">
                                          <select class="form-control" v-model="modals.plannedLessonDetail.subject">
                                            <option class="text-info" v-for="(subject, index) in subjects" :key="index">{{subject}}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                    <div class="col-md-4 pl-md-1">
                                        <base-input label="Học kỳ">
                                          <select class="form-control" v-model="modals.plannedLessonDetail.semester">
                                            <option class="text-info" v-for="(semester, index) in semesters" :key="index" :value="semester.name">{{ semester.name }}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                    <div class="col-md-4 pl-md-1">
                                        <base-input label="Lớp">
                                          <select class="form-control" v-model="modals.plannedLessonDetail.room">
                                            <option class="text-info" v-for="(room, index) in rooms" :key="index" :value="room.name">{{ room.name }}</option>
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
            <h4 slot="header" class="modal-title" id="modal-title-default" v-if="this.bigLineChart.activeIndex === 1">Xóa nhận xóa bài giảng này </h4>
            <template slot="footer">
                <base-button type="secondary" @click="removeObject">Xác nhận</base-button>
                <base-button type="danger" class="ml-auto" @click="modals.removeModal = false">Hủy
                </base-button>
            </template>
        </modal>

        <!-- Seating Modal -->
        <modal :show.sync="modals.seatingModal"
                body-classes="p-0"
               modal-classes="modal-dialog-centered modal-md">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0">
                <template>
                    <div class="text-muted mb-3">
                        <h4 class="text-success text-">Quản lý chỗ ngồi</h4>
                    </div>
                </template>
                <template>
                      <base-table :data="seatingData" :columns="seating_columns">
                        <template slot="columns">
                          <th>Học sinh</th>
                          <th class="text-center">Hàng</th>
                          <th class="text-center">Cột</th>
                        </template>
                        <template slot-scope="{ row }">
                          <td> <div class="text-info"> {{ row.student }}</div></td>
                          <td class="text-center">{{ row.row }}</td>
                          <td class="text-center">{{ row.column }}</td>
                        </template>
                      </base-table>
                      <!-- <base-button type="default" size="sm" icon @click="toggleCreateSeating()">
                              <i class="tim-icons icon-simple-add"></i>
                      </base-button> -->
                </template>
            </card>
        </modal>

        <!-- BÀI GIẢNG -->
        <div v-if="bigLineChart.activeIndex === 1">
          <base-table :data="plannedlessonData" :columns="plannedlesson_columns">
            <template slot="columns">
              <th>ID</th>
              <th>Môn học</th>
              <th>Bài số</th>
              <th>Tên bài học</th>
              <th>Học kỳ</th>
              <th>Lớp</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.id }}</td>
              <td>{{ row.subject }}</td>
              <td>{{ row.lesson_number }}</td>
              <td>{{ row.name_lesson }}</td>
              <td>{{ row.semester }}</td>
              <td>{{ row.room }}</td>
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
          <base-button type="default" size="sm" icon @click="toggleCreate()">
                  <i class="tim-icons icon-simple-add"></i>
          </base-button>
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
        seatingModal: false,
        
        createModal: false,
        updateModal: false,
        removeModal: false,
        idRemove: null,

        semesterCreate: {
          name: null,
          day_begin: null,
          number_of_weeks: null
        },

        plannedLessonCreate: {
          semester: null,
          subject: null,
          name_lesson: null,
          lesson_number: null,
          room: null,
        },

        teacherModal: false,
        parentModal: false,
        semesterDetail: null,
        teacherDetail: null,
        plannedLessonDetail: null,
    },
    seatingData: null,
    rooms: null,
    seating_columns: ["student", "row", "column"],
    subjects: ['TOAN', 'VAN', 'ANH', 'KHTN_HOA', 'KHTN_LY', 'KHTN_SINH', 'KHXH_DIA', 'KHXH_SU', 'KHXH_GDCD', 'TD', 'MT', 'AN', 'TH', 'CN', 'HDTN-HN'],
    subjects_2: ['Toán', 'Ngữ Văn', 'Tiếng Anh', 'Hóa', 'Sinh học', 'Địa lý', 'Lịch sử', 'GDCD', 'Thể dục', 'Mỹ thuật', 'Âm nhạc', 'Tin học', 'Mỹ thuật'],
    semester_columns: ["semester", "day_begin", "number_of_weeks"],
    room_columns: ["name", "students", "homeroom_teacher"],
    plannedlesson_columns: ["id", "subject", "lesson_number", "name_lesson", "semester", "room"],
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
          await this.getRoomData();
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
      async getPositionData(index) {
        
        const token = localStorage.getItem("access_token");
        try {
          // const response = await axios.get(`${API_URL}/rooms/${roomName}/allseatings/`, {
          const response = await axios.get(`${API_URL}/rooms/seating-positions/?room=${index}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });
          if (response.data.length === 0) {
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Không tồn tại danh sách chỗ ngồi của lớp",
              timeout: 3000,
              verticalAlign: "bottom",
              horizontalAlign: "right",
            });
          } 
          else {
            this.seatingData = response.data;
          }
          
          
        } catch (error) {
          console.error("Error getting seating data:", error);
        }
      },
      getRoomData() {
        if (this.rooms) return;
        const token = localStorage.getItem("access_token");

        axios
          .get(API_URL + "/rooms/roomset/", {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.rooms = response.data;
          })
          .catch((error) => {
            console.error("Error getting room data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy danh sách lớp học thất bại",
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
        } else if (this.bigLineChart.activeIndex === 1) {
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
          } else if (this.bigLineChart.activeIndex === 1) {
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
    createObject(){
        let apiUrl = "";
        let data =null
        if(this.bigLineChart.activeIndex ===0 ){
          apiUrl = API_URL + `/adminpanel/semesters/`
          data = this.modals.semesterCreate
        } else if (this.bigLineChart.activeIndex === 1) {
          apiUrl = API_URL + "/adminpanel/planned-lessons/";
          data = this.modals.plannedLessonCreate
        }

        console.log(data)
        const token = localStorage.getItem("access_token");
        axios
        .post(apiUrl, data, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          let message = "";
          if (this.bigLineChart.activeIndex === 0) {
            message = "Thêm học kỳ thành công"
          } else if (this.bigLineChart.activeIndex === 1) {
            message = "Thêm bài giảng thành công"
          }

            this.$notify({
                type: "success",
                icon: 'tim-icons icon-check-2',
                message: message,
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });

          this.modals.createModal = false
          this.initBigChart(this.bigLineChart.activeIndex)
        })
        .catch((error) => {
          console.error("Error create data :", error);
          if(error.response.status === 400 && this.bigLineChart.activeIndex === 0){
            this.$notify({
                type: "warning",
                message: "Ngày bắt đầu của học kỳ phải là thứ hai",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
          }
          else {
            this.$notify({
                type: "warning",
                message: "Thêm dữ liệu thất bại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
          }
        });
    },
    updateObject(){
        let data = null;
        let apiUrl = "";
        // const data = this.modals.studentDetail;

        if(this.bigLineChart.activeIndex ===0 ){
          apiUrl = API_URL + `/adminpanel/semesters/${this.modals.semesterDetail.name}/`
          data = this.modals.semesterDetail
        }
         else if (this.bigLineChart.activeIndex === 1) {
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
     toggleSeatingDetail(){
      this.modals.seatingModal = true;
      this.getPositionData();
    },
    toggleCreate(){
      this.modals.createModal = true;
    },
    toggleUpdate(index){
        this.modals.updateModal = true;

        let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
        if (this.bigLineChart.activeIndex === 0) {
          apiUrl = API_URL + "/adminpanel/semesters/" + index + "/";
        }  else if (this.bigLineChart.activeIndex === 1) {
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
          }  else if (this.bigLineChart.activeIndex === 1) {
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
          else if(this.bigLineChart.activeIndex === 1) this.plannedlessonData = response.data
          else if(this.bigLineChart.activeIndex === 2) this.deviceData = response.data
          
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