<template>
  <div class="wrapper study">
    <div class="navbar">
      <div>
        <base-button @click="goToDashboard" class="dashboard-button btn-success" simple>
          <i class="tim-icons icon-minimal-left"></i> Trang chủ
        </base-button>
      </div>
      <div class="title">
        <h1 class="font-weight-bold">DẠY HỌC</h1>
      </div>
      <div>
        <base-button @click="toggleEvaluate" class="dashboard-button btn-info" simple>
          <i class="tim-icons icon-notes"></i> Đánh giá
        </base-button>
      </div>
      <div class="current-time" style=" width: 180px">{{ currentTime }}</div>
    </div>
    
    <div class="classroom-layout mt-3">
      <div v-for="(row, rowIndex) in desks" :key="rowIndex" class="row">
        <div v-for="(seat, columnIndex) in row" :key="columnIndex"
         :class="['seat', 
                      { 'spacer': columnIndex === 1 || columnIndex === 3 || columnIndex === 5 || columnIndex === 7}]"  
         @dragover.prevent @drop="dropStudent(rowIndex, columnIndex)" @dragstart="dragStart(seat,rowIndex,columnIndex)">
          <base-button
            v-if="seat"
            @click="scoringAndEnroll(seat)"
            class="btn btn-simple student"
            draggable
            :class="{'btn-success': getAttendanceStatus(seat.user) === 1, 'btn-danger': (getAttendanceStatus(seat.user) === 3) || (!getAttendanceStatus(seat.user)) , 'btn-warning': getAttendanceStatus(seat.user) === 2,}"
            
          >
            {{ shortenName(seat.full_name) }} <!-- Assuming 'seat' is an object with 'student' having a 'name' property -->
          </base-button>
        </div>
      </div>

      <div class="class-info">
        <table class="table table-bordered class-info-table">
          <thead>
            <tr>
              <th>Lớp</th>
              <th>Tiết</th>
              <th>Môn</th>
              <th>Sỹ số</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{this.lessonData.room}}</td>
              <td>{{this.lessonData.period}}</td>
              <td>{{this.lessonData.subject}}</td>
              <td> {{ this.attendances ? this.countUsersWithStatus12(attendances)+"/" : "" }}<strong>{{this.positions.length }}</strong></td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="teacher-desk">
        <h3>Bàn giáo viên</h3>
      </div>

      <!-- Scoring Modal -->
        <modal :show.sync="scoreModal"
       body-classes="p-0"
       modal-classes="modal-dialog-centered modal-lg">
    <card type="secondary"
          header-classes="bg-white pb-5"
          body-classes="px-lg-5 py-lg-5"
          class="border-0 mb-0">
        <template>
            <div class="text-muted mb-3">
                <h4 class="text-success">Chấm điểm và Điểm danh</h4>
            </div>
        </template>
        <template>
            <div class="row">
                <!-- Card bên trái: Chấm điểm -->
                <div class="col-md-8">
                    <card type="secondary" header-classes="bg-white pb-2" class="border-0 mb-0">
                        <template>
                            <div class="text-muted mb-3">
                                <h5>Chấm điểm</h5>
                            </div>
                        </template>
                        <div class="row">
                            <div class="col-md-6">
                                <base-input disabled label="Id học sinh" v-model="studentDetail.id"></base-input>
                            </div>
                            <div class="col-md-6">
                                <base-input disabled label="Họ và tên" v-model="studentDetail.full_name"></base-input>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <base-input disabled label="Môn" v-model="studentDetail.subject"></base-input>
                            </div>
                            <div class="col-md-6">
                                <base-input disabled label="Học kỳ" v-model="studentDetail.semester"></base-input>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-12">
                                <base-input label="Điểm" v-model="studentDetail.grade"></base-input>
                            </div>
                        </div>
                        <div class="d-flex mt-4">
                            <base-button @click="givenScore" type="secondary" fill>Xác nhận</base-button>
                        </div>
                    </card>
                </div>

                <!-- Card bên phải: Trạng thái điểm danh -->
                <div class="col-md-4">
                  <card type="secondary" header-classes="bg-white pb-2" class="border-0 mb-0">
                      <template>
                          <div class="text-muted mb-3">
                              <h5>Trạng thái điểm danh</h5>
                          </div>
                      </template>
                      <div class="container text-center"> <!-- Thêm class text-center -->
                          <div class="row justify-content-center"> <!-- Căn giữa với justify-content-center -->
                              <div class="col-xs-12">
                                  <div class="switch">
                                      <input id="switch-present" name="attendance" type="radio" value="1" v-model="newStatus" class="switch-input" @change="updateStatus" />
                                      <label for="switch-present" class="switch-label switch-label-y"><i class="tim-icons icon-check-2"></i></label>
                                      
                                      <input id="switch-late" name="attendance" type="radio" value="2" v-model="newStatus" class="switch-input" @change="updateStatus"/>
                                      <label for="switch-late" class="switch-label switch-label-i"><i class="tim-icons icon-simple-delete"></i></label>
                                      
                                      <input id="switch-absent" name="attendance" type="radio" value="3" v-model="newStatus" class="switch-input" @change="updateStatus"/>
                                      <label for="switch-absent" class="switch-label switch-label-n"><i class="tim-icons icon-simple-remove"></i></label>
                                      
                                      <span class="switch-selector"></span>
                                  </div>
                              </div>
                          </div>
                      </div>
                      <div class="text-muted mt-2">
                          <span v-if="newStatus == 1" class="text-success">Có mặt</span>
                          <span v-if="newStatus == 2" class="text-warning">Đi muộn</span>
                          <span v-if="newStatus == 3" class="text-danger">Vắng mặt</span>
                      </div>
                  </card>
              </div>
            </div>
        </template>
    </card>
</modal>




        <!-- Evaluating Modal -->
        <modal :show.sync="evaluateModal"
                body-classes="p-0"
               modal-classes="modal-dialog-centered modal-md">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0">
                <template>
                    <div class="text-muted mb-3">
                        <h4 class="text-success">Đánh giá tiết học</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12" v-if="lessonDetail">
                              <div class="row">
                                    <div class="col-md-3 pr-md-1">
                                        <base-input label="Bài số" v-model="lessonDetail.lessonNumber" placeholder="Bài số">
                                        </base-input>
                                    </div>
                                    <div class="col-md-9 pr-md-1">
                                        <base-input label="Tên bài học" v-model="lessonDetail.nameLesson" placeholder="Tên bài học">
                                        </base-input>
                                    </div>
                              </div>
                              <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Điểm đánh giá (Số tự nhiên 0 -> 10)" v-model="lessonDetail.evaluate" placeholder="Điểm đánh giá">
                                        </base-input>
                                    </div>
                              </div>
                              <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Nhận xét">
                                          <textarea class="form-control" rows="3" v-model="lessonDetail.comment"></textarea>
                                        </base-input>
                                    </div>
                              </div>
                              <base-button @click="evaluating" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>
    </div>
  </div>
</template>

<script>
import axios from '../../services/axios'; 
import Modal from '../../components/Modal.vue';

let API_URL = ""

export default {
  components: { Modal },
  mounted() {
    this.startLongPolling();
  },
  data() {
    return {
      attendances: null,
      currentStatus: null,
      newStatus: null,
      attendanceStatus: 1,

      isActive: false,
      attendance: null,
      scoreModal : false,
      evaluateModal: false,

      polling: false,

      lessonData: null,
      rooms: null,

      lessonDetail: {
        semester: null,
        day: null,
        room: null,
        period_number: null,
        lessonNumber: null,
        nameLesson: null,
        teacher: null,
        comment: null,
        evaluate: null

      },

      studentDetail: {
        id: null,
        full_name: null,
        subject: null,
        semester: null,
        score_type: null,
        grade: null,
      },

      currentTime: this.formatTime(new Date()),
      positions: null,
      desks: Array.from({ length: 5 }, () => Array(8).fill(null)),
      draggedStudent: null,
      draggedRow: null,
      draggedCol: null,
    };
  },
  methods: {
    countUsersWithStatus12(attendances) {
        // Lọc các đối tượng có status là 1 hoặc 2
        const filteredUsers = attendances.filter(item => item.status === 1 || item.status === 2);
        
        // Đếm số lượng các user có status = 1 hoặc 2
        return filteredUsers.length;
    },
    
    demo(){
      return true;
    },
    getAttendanceStatus(studentId) {
      // Lọc danh sách attendance dựa trên studentId
      if(!this.attendance) return 0;
      const studentAttendance = this.attendance.filter(
        (att) => att.user === studentId
      );

      // Nếu không có dữ liệu, trả về trạng thái vắng mặt = 3
      if (studentAttendance.length === 0) {
        return 0;
      }

      // Kiểm tra trạng thái cuối cùng của sinh viên
      const lastStatus = studentAttendance[studentAttendance.length - 1].status;
      return lastStatus
    },
    async startLongPolling() {
  let lastAttendance = [];
  this.polling = true;

  // Sử dụng setInterval với khoảng thời gian 500ms
  this.pollingInterval = setInterval(async () => {
    if (!this.polling) {
      clearInterval(this.pollingInterval);
      return;
    }

    try {
      const token = localStorage.getItem("access_token");
      const response = await axios.get(`${API_URL}/attendance/attendance/?lesson=${this.lessonData.id}`, {
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      this.attendances = response.data;
      const newAttendance = response.data || [];

      if (JSON.stringify(newAttendance) !== JSON.stringify(lastAttendance)) {
        const differences = this.getDifferences(lastAttendance, newAttendance);
        if (differences.length > 0) {
          this.attendance = newAttendance;
          console.log('New attendance data:', this.attendance);

          if (differences.length !== newAttendance.length) {
            differences.forEach(difference => {
              if (difference.status === 1 && difference.lesson == this.lessonData.id) {
                // this.$notify({
                //   type: "success",
                //   icon: 'tim-icons icon-badge',
                //   title: "Điểm danh thành công",
                //   message: `Học sinh ${difference.user}`,
                //   timeout: 1000,
                //   verticalAlign: "bottom",
                //   horizontalAlign: "left",
                // });
              }
            });
          }
          lastAttendance = newAttendance;
        }
      }

    } catch (error) {
      console.error('Error fetching attendance data:', error);
    }
  }, 500); // Polling mỗi 0.5 giây
},

    // Hàm để lấy ra các phần tử khác nhau
    getDifferences(oldData, newData) {
      const differences = [];

      // Chuyển đổi dữ liệu cũ thành một đối tượng để dễ dàng so sánh
      const oldDataMap = new Map(oldData.map(item => [item.id, item]));

      // So sánh từng phần tử trong dữ liệu mới với dữ liệu cũ
      newData.forEach(newItem => {
        const oldItem = oldDataMap.get(newItem.id);
        if (!oldItem || JSON.stringify(oldItem) !== JSON.stringify(newItem)) {
          differences.push(newItem);
        }
      });

      return differences;
    },
    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    shortenName(fullName) {
      const nameParts = fullName.trim().split(' '); // Tách tên thành các phần
      if (nameParts.length == 3) return nameParts.slice(1).join(' '); // Nếu chỉ có một phần, trả về tên gốc
      if (nameParts.length == 4) return nameParts.slice(2).join(' '); // Lấy các phần sau họ và ghép lại
      return fullName
    },
    scoringAndEnroll(index){
      this.studentDetail.id = index.user
      this.studentDetail.full_name = index.full_name
      this.studentDetail.subject = this.lessonData.subject
      this.studentDetail.semester = this.lessonData.semester

      this.currentStatus = this.getAttendanceStatus(index.user);
      this.newStatus = this.currentStatus;
      console.log("current and new"+this.currentStatus)

      this.scoreModal = true
    },
    updateStatus(){
      console.log("current"+this.currentStatus)
      console.log("new"+this.newStatus)
      if(this.currentStatus == this.newStatus) return 
      else {
        //update status
        let data = {
          "lesson_id": this.lessonData.id,
          "student_id": this.studentDetail.id,
          "new_status": this.newStatus
        }
        const token = localStorage.getItem("access_token");
        
        console.log(data)

        axios
        .post(API_URL+"/attendance/attendance/update/", data,  {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then(() => {
          this.currentStatus = this.newStatus 
          this.$notify({
                type: "success",
                icon: 'tim-icons icon-bell-55',
                message: "Đổi trạng thái học sinh " + this.studentDetail.full_name+ " thành công",
                timeout: 1000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        })
        .catch((error) => {
          console.error("Error post grade data :", error);
          if(this.currentStatus == 0){
            this.createStatus()
            return
          }

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Đổi trạng thái thất bại. Vui lòng thử lại sau",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
      }
    },
    createStatus(){
      let data = {
          "student_id": this.studentDetail.id,  
          "device_id": "as7dchu8d"
        }
        console.log(data)
        const token = localStorage.getItem("access_token");
        
        console.log(data)

        axios
        .post(API_URL+"/attendance/attendance/", data,  {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.currentStatus = response.data.status
          this.newStatus = this.currentStatus
          this.$notify({
                type: "success",
                icon: 'tim-icons icon-bell-55',
                message: "Thêm trạng thái điểm danh thành công",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        })
        .catch((error) => {
          console.error("Error post grade data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Thêm trạng thái điểm danh thất bại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    givenScore(){
      if(!this.studentDetail.grade){
        this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Vui lòng nhập điểm cho học sinh",
                timeout: 1000,
                verticalAlign: "top",
                horizontalAlign: "right",
        });
        return
      }

      const data = {
        "student": this.studentDetail.id,
        "subject": this.studentDetail.subject,
        "semester": this.studentDetail.semester,
        "score_type": "TX",
        "grade": this.studentDetail.grade
      }

      console.log(data)
      const token = localStorage.getItem("access_token");

        axios
        .post(API_URL+"/adminpanel/grades/", data,  {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then(() => {
          this.scoreModal = false
          this.studentDetail.grade = null
          this.$notify({
                type: "success",
                icon: 'tim-icons icon-bell-55',
                message: "Chấm điểm cho học sinh " + this.studentDetail.full_name+ " thành công",
                timeout: 1000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        })
        .catch((error) => {
          console.error("Error post grade data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Chấm điêm thất bại. Vui lòng thử lại sau",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleEvaluate(){
      this.evaluateModal = true;
    },
    evaluating(){
      if(!this.lessonDetail.evaluate) {
        this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Vui lòng cho điểm đánh giá tiết học",
                timeout: 1000,
                verticalAlign: "top",
                horizontalAlign: "right",
        });
        return
      }
      if(!this.lessonDetail.comment) {
        this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Vui lòng cho nhận xét tiết học",
                timeout: 1000,
                verticalAlign: "top",
                horizontalAlign: "right",
        });
        return
      }

      const data = {
        "comment": this.lessonDetail.comment,
        "evaluate": this.lessonDetail.evaluate,        
        "lesson_number": this.lessonDetail.lessonNumber,
        "name_lesson": this.lessonDetail.nameLesson
      }
      console.log(data)
      
      const token = localStorage.getItem("access_token");

        axios
        .patch(API_URL+`/adminpanel/lessons/${this.lessonData.id}/update/`, data,  {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then(() => {
          this.$notify({
                type: "success",
                icon: 'tim-icons icon-bell-55',
                message: "Đánh giá tiết học thành công",
                timeout: 1000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
              this.evaluateModal = false
        })
        .catch((error) => {
          console.error("Error:", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Đánh giá tiết học thất bại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    async initializeData() {
      try {
        await this.getApiUrl();
        await this.getPositionData();
        this.startLongPolling()
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
    dragStart(student, row, col) {
      this.draggedStudent = student; 
      this.draggedRow = row;
      this.draggedCol = col;
      console.log("start Drag"+student)
    },
    dropStudent(rowIndex, columnIndex) {
      if (this.draggedStudent) {
        const targetStudent = this.desks[rowIndex][columnIndex];
        if(!targetStudent) {
          this.desks[rowIndex][columnIndex] = this.draggedStudent; // Đặt học sinh kéo tới vị trí mới
          this.desks[this.draggedRow][this.draggedCol] = null; // vị trí trước đó là null
          //Cập nhật vị trí mới cho học sinh
          this.updatePosition(this.draggedStudent.user, rowIndex, columnIndex);
        }
        else {
          this.desks[rowIndex][columnIndex] = this.draggedStudent;
          this.desks[this.draggedRow][this.draggedCol] = targetStudent;
          this.swapPosition(this.draggedStudent, targetStudent);
        }
      }
    },
    updatePosition(studentId, row, col){
      const token = localStorage.getItem("access_token");
      const data = {
        "row": row+1,
        "column": col+1
      }
        axios
        .patch(API_URL+"/rooms/seating-positions/"+ studentId +"/", data, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.$notify({
                type: "success",
                icon: 'tim-icons icon-bell-55',
                message: "Đổi vị trí học sinh "+ response.data.student_details.full_name + " thành công",
                timeout: 1500,
                verticalAlign: "bottom",
                horizontalAlign: "left",
              });
        })
        .catch((error) => {
          console.error("Error get lesson data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Đổi vị trí không thành công. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    swapPosition(student1, student2){
      const token = localStorage.getItem("access_token");
      const data = {
        "user_id_1": student1.user,
        "user_id_2": student2.user
      }
        axios
        .post(API_URL+"/rooms/seating-positions/swap_seats/", data, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then(() => {
          this.$notify({
                type: "success",
                icon: 'tim-icons icon-bell-55',
                message: "Đổi vị trí học sinh "+student1.full_name+" và "+student2.full_name + " thành công",
                timeout: 1500,
                verticalAlign: "bottom",
                horizontalAlign: "left",
              });
        })
        .catch((error) => {
          console.error("Error get lesson data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Đổi vị trí không thành công. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    formatPositionData(positions) {
      positions.forEach(position => {
        const columnIndex = position.column - 1; 
        const rowIndex = position.row - 1; 
        this.$set(this.desks[rowIndex], columnIndex, position.student_details); 
      });
      return this.desks;
    },
    formatTime(date) {
      return date.toLocaleTimeString();
    },
    goToDashboard() {
      this.polling = false
      this.$router.push('/profile');  
    },
    async getPositionData() {
      this.lessonData = JSON.parse(localStorage.getItem("lesson_data"));
      console.log(this.lessonData)
      this.lessonDetail.lessonNumber = this.lessonData.lesson_number
      this.lessonDetail.nameLesson = this.lessonData.name_lesson
      this.lessonDetail.evaluate = this.lessonData.evaluate
      this.lessonDetail.comment = this.lessonData.comment
      const roomName = this.lessonData.room
      const token = localStorage.getItem("access_token");
      try {
        // const response = await axios.get(`${API_URL}/rooms/${roomName}/allseatings/`, {
        const response = await axios.get(`${API_URL}/rooms/seating-positions/?room=${roomName}`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        this.positions = response.data;
        if (response.data.length === 0) {
          this.$notify({
            type: "warning",
            icon: 'tim-icons icon-bell-55',
            message: "Không tồn tại danh sách chỗ ngồi của lớp",
            timeout: 3000,
            verticalAlign: "bottom",
            horizontalAlign: "right",
          });
        } else {
          this.desks = this.formatPositionData(this.positions);
        }
      } catch (error) {
        console.error("Error getting seating data:", error);
      }
    },
  },
  created() {
    setInterval(() => {
      this.currentTime = this.formatTime(new Date());
    }, 1000);
    this.initializeData(); 
  }
};
</script>

<style >
.study {
  text-align: center;
  position: relative;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 20px;
}

.dashboard-button {
  margin-right: auto;
}

.title {
  flex-grow: 1;
}

.current-time {
  margin-left: auto;
  font-size: 30px;
}

.classroom-layout {
  display: flex;
  flex-direction: column;
  justify-content: space-evenly;
  align-items: center;
}

.row {
  display: flex;
  flex-direction: row;
  margin-bottom: 10px;
}

.seat {
  border: 1px solid #DAA520;
  width: 130px;
  height: 70px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.student {
  padding: 10px;
  background-color: #f0f0f0;
  cursor: pointer;
  border-radius: 5px;
  text-align: center;
}

.teacher-desk {
  border: 2px solid #ff6347;
  padding: 20px;
  position: absolute;
  border-radius: 5px;
  bottom: 50px;
  right: 160px;
}
.spacer {
  margin-right: 50px; /* Khoảng cách giữa các cột */
}

.container {
  margin-top: 20px;
  width: 100%;
}

.switch {
    position: relative;
    height: 32px;
    width: 210px;
    margin: 20px auto;
    background: #d7d7d789;
    border-radius: 32px;
}

.switch-label {
    font-weight: bold;
    position: relative;
    z-index: 2;
    float: left;
    width: 70px; /* Thay đổi giá trị này để mở rộng chiều rộng của label */
    line-height: 32px; /* Giữ cho icon được căn giữa trong switch */
    font-size: 24px; /* Tăng kích thước chữ nếu cần */
    color: #676a6c;
    text-align: center;
    cursor: pointer;
}

.switch-input {
  display: none;
}

.switch-input:checked + .switch-label {
  color: #fff;
  transition: color 0.15s ease-out, text-shadow 0.15s ease-out;
}

.switch-input:checked + .switch-label-y ~ .switch-selector {
  transform: translateX(0%);
  background-color: #1ab394; /* Màu xanh cho 'Có mặt' */
}

.switch-input:checked + .switch-label-i ~ .switch-selector {
  transform: translateX(100%);
  background-color: #f8ac59; /* Màu vàng cho 'Đi muộn' */
}

.switch-input:checked + .switch-label-n ~ .switch-selector {
  transform: translateX(200%);
  background-color: #ed5565; /* Màu đỏ cho 'Vắng mặt' */
}

.switch-selector {
  position: absolute;
  z-index: 1;
  top: 0;
  left: 0;
  width: 33.33%;
  height: 32px;
  border-radius: 32px;
  background-color: #1ab394;
  transition: all 0.3s cubic-bezier(0.18, 0.89, 0.32, 1.28);
}
.switch-label {
    white-space: nowrap; /* Ngăn không cho chữ xuống dòng */
}

.switch-label i {
    font-size: 12px; /* Điều chỉnh kích thước icon */
    line-height: 32px; /* Giữ cho icon được căn giữa trong switch */
    transition: font-size 0.3s; /* Hiệu ứng chuyển đổi khi thay đổi kích thước */
}

/* Tùy chọn cho trạng thái checked */
.switch-input:checked + .switch-label i {
    font-size: 28px; /* Kích thước lớn hơn khi được chọn */
}

.class-info {
  position: absolute;
  bottom: 35px; /* Adjust vertical position */
  left: 120px;   /* Adjust horizontal position */
}
.class-info-table {
  width: 240px; /* Điều chỉnh kích thước */
  background-color: #f9f9f9;
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); /* Hiệu ứng đổ bóng */
}

.class-info-table th {
  background-color: #007bff; /* Màu nền phần header */
  color: white;
  font-weight: bold;
  padding: 10px; /* Tạo khoảng cách trong ô */
  text-align: center;
  position: relative;
}

.class-info-table th:not(:last-child)::after {
  content: "";
  position: absolute;
  top: 0;
  right: 0;
  height: 100%;
  width: 2px;
  background-color: #f2f2f21f; /* Màu sắc đường ngăn cách */
}

.class-info-table td {
  padding: 8px;
  text-align: center;
  color: #333;
}

.class-info-table tr:nth-child(even) {
  background-color: #f2f2f2; /* Màu nền so le */
}
</style>
