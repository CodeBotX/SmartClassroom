<template>
  <div class="row">
    <div class="col-12">
      <card>
        <template slot="header">
          <div class="row">
            <div class="col-md-5">
              <h3>Thời khóa biểu {{ roomSelected ? roomSelected.name : "" }} {{ semesterSelected ? " - "+semesterSelected.name : "" }} {{ weekSelected ? " - Tuần "+ weekData : "" }} </h3>
            </div>
            <div class="col-md-7">
              <div class="row">
                <div class="col-md-3 pr-md-1 text-center">
                  <base-input label="Học kỳ">
                    <select class="btn btn-simple btn-sm btn-success" v-model="semesterSelected" @change="getWeekData">
                      <option class="text-info" v-for="(semester, index) in semesters" :key="index" :value="semester">{{ semester.name }}</option>
                    </select>
                  </base-input>
                </div>
                <div class="col-md-3 pl-md-1 text-center">
                  <base-input label="Lớp">
                    <select class="btn btn-simple btn-sm btn-success" v-model="roomSelected">
                    <option class="text-info" v-for="(room, index) in rooms" :key="index" :value="room" >{{ room.name }}</option>
                    </select>
                  </base-input>
                </div>
                <div class="col-md-3 pr-md-1 text-center">
                  <base-input label="Tuần">
                    <select class="btn btn-simple btn-sm btn-success" v-model="weekSelected" @change="takeWeekData">
                      <option class="text-info" v-for="week in weeks" :key="week" :value="week" >{{ week }}</option>
                    </select>
                  </base-input>
                </div>
                <div class="col-md-3 pl-md-1 text-center">
                  <base-button 
                    class="btn btn-sm "
                    @click="getTimeTable"
                    fill
                  >Lọc
                  </base-button>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- Thời khóa biểu -->
        <div v-if="checkTimeTable">
          <base-table :data="timetableData" :columns="timetable_columns">
            <template slot="columns">
              <th class="text-center text-info">Tiết</th>
              <th class="text-center text-info">Thứ 2</th>
              <th class="text-center text-info">Thứ 3</th>
              <th class="text-center text-info">Thứ 4</th>
              <th class="text-center text-info">Thứ 5</th>
              <th class="text-center text-info">Thứ 6</th>
              <th class="text-center text-info">Thứ 7</th>
            </template>
            <template slot-scope="{ row }">
              <td class="text-center"> <div class="text-info">Tiết {{ row.period }}</div></td>

              <td class="text-center" v-if="row.monday">
                <base-button @click="toggleDetail(row.monday.id, 0, row.period)" class="btn-simple btn-lg text-secondary" type="default">{{ row.monday.subject}}</base-button></td>
              <td class="text-center" v-else>
                <base-button @click="toggleCreate(0, row.period)" class="btn-simple btn-lg" type="default"> <i class="tim-icons icon-simple-add"></i> </base-button></td>
              
              <td class="text-center" v-if="row.tuesday">
                <base-button @click="toggleDetail(row.tuesday.id, 1, row.period)" class="btn-simple btn-lg text-secondary" type="default">{{ row.tuesday.subject}}</base-button></td>
              <td class="text-center" v-else>
                <base-button @click="toggleCreate(1, row.period)" class="btn-simple btn-lg" type="default"> <i class="tim-icons icon-simple-add"></i> </base-button></td>

              <td class="text-center" v-if="row.wednesday">
                <base-button @click="toggleDetail(row.wednesday.id, 2, row.period)" class="btn-simple btn-lg text-secondary" type="default">{{ row.wednesday.subject}}</base-button></td>
              <td class="text-center" v-else>
                <base-button @click="toggleCreate(2, row.period)" class="btn-simple btn-lg" type="default"> <i class="tim-icons icon-simple-add"></i> </base-button></td>

              <td class="text-center" v-if="row.thursday">
                <base-button @click="toggleDetail(row.thursday.id, 3, row.period)" class="btn-simple btn-lg text-secondary" type="default">{{ row.thursday.subject}}</base-button></td>
              <td class="text-center" v-else>
                <base-button @click="toggleCreate(3, row.period)" class="btn-simple btn-lg" type="default"> <i class="tim-icons icon-simple-add"></i> </base-button></td>
              
              <td class="text-center" v-if="row.friday">
                <base-button @click="toggleDetail(row.friday.id, 4, row.period)" class="btn-simple btn-lg text-secondary" type="default">{{ row.friday.subject}}</base-button></td>
              <td class="text-center" v-else>
                <base-button @click="toggleCreate(4, row.period)" class="btn-simple btn-lg" type="default"> <i class="tim-icons icon-simple-add"></i> </base-button></td>
              
              <td class="text-center" v-if="row.saturday">
                <base-button @click="toggleDetail(row.saturday.id, 5, row.period)" class="btn-simple btn-lg text-secondary" type="default">{{ row.saturday.subject}}</base-button></td>
              <td class="text-center" v-else>
                <base-button @click="toggleCreate(5, row.period)" class="btn-simple btn-lg " type="default"> <i class="tim-icons icon-simple-add"></i> </base-button></td>
            </template>
          </base-table>
        </div>
      </card>

      <!-- Lesson Detail Modal -->
        <modal :show.sync="detailModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thông tin tiết học</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12" v-if="lessonDetail">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1" >
                                        <base-input label="Môn" >
                                          <select class="form-control" v-model="lessonDetail.subject" @change="getTeacherAssignment(lessonDetail.subject)">
                                            <option class="text-info" v-for="(subject, index) in subjects" :key="index">{{subject}}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input disabled label="Ngày" v-model="lessonDetail.day"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Giáo viên" >
                                          <select class="form-control" v-model="lessonDetail.teacher">
                                            <option class="text-info" v-for="(teacher, index) in teachers" :key="index" :value="teacher.teacher">{{ teacher.teacher}}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Đánh giá" v-model="lessonDetail.evaluate" disabled></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Nhận xét"> 
                                          <textarea class="form-control" rows="3" v-model="lessonDetail.comment" disabled></textarea>
                                        </base-input>
                                    </div>
                                </div>
                                <base-button @click="updateLesson" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>

        <!-- Lesson Create Modal -->
        <modal :show.sync="createModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thêm tiết học</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12" v-if="lessonCreate">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1" >
                                        <base-input label="Môn" >
                                          <select class="form-control" v-model="lessonCreate.subject">
                                            <option class="text-info" v-for="(subject, index) in subjects" :key="index" :value="subject">{{subject}}</option>
                                          </select>
                                        </base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input disabled label="Ngày" v-model="lessonCreate.day"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input disabled label="Tiết" v-model="lessonCreate.period"></base-input>
                                    </div>
                                </div>
                                <base-button @click="createLesson" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>
    </div>
  </div>
</template>

<script>
import Card from "../../components/Cards/Card.vue";
import BaseTable from '../../components/BaseTable.vue';
import axios from "../../services/axios";
import Modal from '../../components/Modal.vue';

let API_URL = "";

export default {
    components: { Card, BaseTable, Modal },
    mounted() {
      this.initializeData();
    },
    data() {
        return {
          checkTimeTable: false,

          teacherName: null,
          semesterSelected: null,
          roomSelected: null,
          weekSelected: null,
          semesters: null,
          rooms: null,
          lessons: null,
          weeks: [],
          currentWeek: null,
          weekData: null,

          detailModal: false,
          createModal: false,

          teacherOption: null,
          teachers: null,

          lessonDetail: null,
          lessonCreate: {
            "subject": null,
            "lesson_number": null,
            "name_lesson": null,
            "day": null,
            "semester": null,
            "room": null,
            "period": null,
            "teacher": null
          },

          subjects: ['TOAN', 'VAN', 'ANH', 'KHTN_HOA', 'KHTN_LY', 'KHTN_SINH', 'KHXH_DIA', 'KHXH_SU', 'KHXH_GDCD', 'TD', 'MT', 'AN', 'TH', 'CN', 'HDTN-HN'],

          timetableData: this.initializeTimetableData(),
          timetable_columns: [
            { title: 'Tiết', key: 'period' },
            { title: 'Thứ 2', key: 'monday' },
            { title: 'Thứ 3', key: 'tuesday' },
            { title: 'Thứ 4', key: 'wednesday' },
            { title: 'Thứ 5', key: 'thursday' },
            { title: 'Thứ 6', key: 'friday' },
            { title: 'Thứ 7', key: 'saturday' },
          ],
        };
    },
    methods: {
      getTeacherDetail(teacherId){
        const token = localStorage.getItem("access_token");

        axios
          .get(API_URL + `/accounts/teachers/?user_id=${teacherId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            console.log(response.data[0].full_name)
            this.teacherName = response.data[0].full_name
          })
          .catch((error) => {
            console.error("Error getting teacher data:", error);
            
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy chi tiết giáo viên thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
      getTeacherAssignment(subject){
        const token = localStorage.getItem("access_token");
        axios
        .get(API_URL+`/adminpanel/assignments/?room=${this.roomSelected.name}&subject=${subject}&semester=${this.semesterSelected.name}`, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.teachers = response.data
          // this.getTeacherDetail(this.teachers[0].teacher)
        })
        .catch((error) => {
          console.error("Error get lesson data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Thông tin phân công giáo viên môn "+subject+ " lớp "+this.roomSelected+ " chưa tồn tại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
      },
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
      toggleDetail(id_lesson, day, period ){
        this.detailModal = true;

        const token = localStorage.getItem("access_token");
        axios
        .get(API_URL+"/adminpanel/lessons/"+id_lesson+"/", {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.lessonDetail = response.data
          this.teachers = this.getTeacherAssignment(this.lessonDetail.subject)
        })
        .catch((error) => {
          console.error("Error get lesson data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Thông tin tiết học không tồn tại. Vui lòng thử lại sau",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });

        axios
        .get(API_URL+"/adminpanel/lessons/"+id_lesson+"/", {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.lessonDetail = response.data

        })
        .catch((error) => {
          console.error("Error get lesson data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Thông tin tiết học không tồn tại. Vui lòng thử lại sau",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
      },
      toggleCreate(day_number, period) {
        // Kiểm tra và chuyển đổi weekSelected thành số nguyên
        const week_number = parseInt(this.weekSelected === "hiện tại" ? this.currentWeek : this.weekSelected, 10);
        
        // Chuyển đổi semesterSelected.day_begin thành Date object
        const semesterStartDate = new Date(this.semesterSelected.day_begin);

        // Tính toán ngày bằng cách cộng thêm số tuần đã chọn
        let date = new Date(semesterStartDate);
        date.setDate(semesterStartDate.getDate() + (week_number - 1) * 7);

        // Tính toán ngày chính xác dựa trên ngày đầu tuần và số ngày cần cộng thêm
        let selectedDay = new Date(date);
        selectedDay.setDate(date.getDate() + day_number );

        const formattedDate = selectedDay.toISOString().split('T')[0];
        this.lessonCreate.day = formattedDate
        this.lessonCreate.period = period
        this.lessonCreate.room = this.roomSelected.name
        this.lessonCreate.semester = this.semesterSelected.name

        this.createModal = true;
      },
      createLesson(){

        const date = new Date(this.lessonCreate.day)
        console.log(this.lessonCreate.day)
        const weekday = date.getDay();    

        let data = {
          "subject": this.lessonCreate.subject,
          "weekday": weekday - 1 ,      
          "semester": this.lessonCreate.semester,
          "room": this.lessonCreate.room,
          "period": this.lessonCreate.period,
        }
        console.log(data)

        const token = localStorage.getItem("access_token");
        axios
        .post(API_URL+"/adminpanel/lessons/create_schedule/", data, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then(() => {
          this.createModal = false
          this.getTimeTable()
          this.$notify({
                type: "success",
                icon: 'tim-icons icon-bell-55',
                message: "Tạo tiết học thành công",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        })
        .catch((error) => {
          console.error("Error create lesson data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Tạo tiết học không thành công.",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });

      },
      updateLesson(){
        const token = localStorage.getItem("access_token");
        const data = {
          "subject": this.lessonDetail.subject,
          "lesson_number": this.lessonDetail.lesson_number,
          "name_lesson": this.lessonDetail.name_lesson,
          "comment": this.lessonDetail.comment,
          "evaluate": this.lessonDetail.evaluate,
          "teacher": this.lessonDetail.teacher
        }

        axios
          .patch(API_URL + "/adminpanel/lessons/"+ this.lessonDetail.id + "/", data, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.getTimeTable();
            this.lessonDetail = response.data;
            this.detailModal = false
            this.$notify({
              type: "success",
              icon: 'tim-icons icon-bell-55',
              message: "Cập nhật dữ liệu tiết học thành công",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          })
          .catch((error) => {
            console.error("Error update lesson data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Cập nhật dữ liệu tiết học thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
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
      takeWeekData(){
        if(this.weekSelected === "hiện tại") {
          this.weekData = this.currentWeek
        }
        else this.weekData = this.weekSelected
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
      getWeekData(){
        if(!this.semesterSelected) return;

        else {
          const arr = ["hiện tại"];
          let number_of_week = this.semesterSelected.number_of_weeks

          const semesterStartDate = new Date(this.semesterSelected.day_begin); // Ngày bắt đầu của học kỳ
          const currentDate = new Date();

          // Tính toán tuần hiện tại
          const diffTime = currentDate - semesterStartDate; // Chênh lệch thời gian
          this.currentWeek = Math.floor(diffTime / (1000 * 60 * 60 * 24 * 7)) + 1; // Tính số tuần

          for (let i = 1; i <= number_of_week; i++) {
            arr.push(i);
          }
          this.weeks = arr
        } 
      },
      getTimeTable() {
        if(!this.weekSelected || !this.roomSelected || !this.semesterSelected){
          this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Vui lòng chọn đầy đủ lựa chọn học kỳ, lớp, tuần.",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
          });
          return
        }

        this.timetableData = this.initializeTimetableData()

        let date = null
        if(this.weekSelected === "hiện tại") {
          date = new Date();
        }
        else {
          // Chuyển đổi weekSelected thành số nguyên
          const week_number = parseInt(this.weekSelected, 10);
          
          const semesterStartDate = new Date(this.semesterSelected.day_begin); // Ngày bắt đầu của học kỳ
          // Tính toán ngày bằng cách cộng thêm số tuần đã chọn
          date = new Date(semesterStartDate);
          date.setDate(semesterStartDate.getDate() + (week_number - 1) * 7);
        }
        const startOfWeek = this.getStartOfWeek(date);
        const endOfWeek = this.getEndOfWeek(date);
        const startDate = this.formatDate(startOfWeek);
        const endDate = this.formatDate(endOfWeek);
        const token = localStorage.getItem("access_token");

        const api = API_URL + `/adminpanel/lessons/?semester=${this.semesterSelected.name}&room=${this.roomSelected.name}&day_range_after=${startDate}&day_range_before=${endDate}`;
        axios
          .get(api, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.lessons = response.data;
            console.log(this.lessons)
            if(response.data.length === 0) {
              this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Không tồn tại thời khóa biểu của lớp " +this.roomSelected.name + " trong tuần " + this.weekData,
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
            }
            else {
              this.timetableData = this.formatTimetableData(this.lessons);
              this.checkTimeTable = true;
               this.$notify({
              type: "success",
              icon: 'tim-icons icon-bell-55',
              message: "Lọc thành công TKB lớp " +this.roomSelected.name + " tuần " + this.weekData,
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
             });
            }
          })
          .catch((error) => {
            console.error("Error getting timetable:", error);
          });
      },
      initializeTimetableData() {
        // Tạo một mảng với các tiết từ 1 đến 5
        return Array.from({ length: 5 }, (_, index) => ({
          period: index + 1,
          monday: null,
          tuesday: null,
          wednesday: null,
          thursday: null,
          friday: null,
          saturday: null,
        }));
      },
      formatTimetableData(lessons) {
        // Cập nhật bảng thời khóa biểu với các tiết học
        lessons.forEach(lesson => {
          const periodIndex = lesson.period - 1;
          const dayOfWeek = this.getDayOfWeek(lesson.day);
          if (this.timetableData[periodIndex]) {
            this.timetableData[periodIndex][this.getDayName(dayOfWeek)] = lesson; // Thêm lesson vào đúng ngày
          }
        });

        return this.timetableData;
      },
      getStartOfWeek(date) {
        const day = date.getDay();
        const diff = date.getDate() - day + (day === 0 ? -6 : 1);
        return new Date(date.setDate(diff));
      },
      getEndOfWeek(date) {
        const startOfWeek = this.getStartOfWeek(date);
        return new Date(startOfWeek.setDate(startOfWeek.getDate() + 6));
      },
      formatDate(date) {
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        return `${year}-${month}-${day}`;
      },
      getDayOfWeek(dateString) {
        const date = new Date(dateString);
        const day = date.getDay();
        return (day === 0) ? 6 : day - 1; // Chủ nhật là 6
      },
      getDayName(day) {
        switch (day) {
          case 0: return 'monday';
          case 1: return 'tuesday';
          case 2: return 'wednesday';
          case 3: return 'thursday';
          case 4: return 'friday';
          case 5: return 'saturday';
          default: return '';
        }
      }
    },
};
</script>

<style>

</style>
