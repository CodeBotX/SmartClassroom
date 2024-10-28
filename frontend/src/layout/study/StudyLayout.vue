<template>
  

  <!-- <div class="wrapper study" style="background-color: ">
      <div class="navbar">
          <div>
            <base-button @click="goToDashboard" class="dashboard-button btn-success" simple>
              <i class="tim-icons icon-minimal-left"></i> Trang chủ
            </base-button>
          </div>
          <div class="title">
            <h1 class="font-weight-bold">Dạy học</h1>
          </div>

          <div class="current-time" style=" width: 180px">{{ currentTime }}</div>
      </div>
    
      <div class="classroom-layout mt-3"></div>
   -->
  
  
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
            @click="scoring(seat)"
            class="btn btn-simple student"
            draggable
            :class="{'btn-success': getAttendanceStatus(seat) === 1, 'btn-danger': getAttendanceStatus(seat) === 2}"
            
          >
            {{ seat }} <!-- Assuming 'seat' is an object with 'student' having a 'name' property -->
          </base-button>
        </div>
      </div>

      <div class="teacher-desk">
        <h3>Bàn giáo viên</h3>
      </div>

      <!-- Scoring Modal -->
        <modal :show.sync="scoreModal"
                body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0">
                <template>
                    <div class="text-muted mb-3">
                        <h4 class="text-success">Chấm điểm</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12" v-if="studentDetail">
                              <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input disabled label="Id học sinh" v-model="studentDetail.id"></base-input>
                                    </div>
                                    <div class="col-md-6 pr-md-1" >
                                        <base-input disabled label="Họ và tên" v-model="studentDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1" >
                                        <base-input disabled label="Môn" v-model="studentDetail.subject"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input disabled label="Học kỳ" v-model="studentDetail.semester"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pl-md-1">
                                        <base-input label="Điểm" v-model="studentDetail.grade"></base-input>
                                    </div>
                                </div>
                                <base-button @click="givenScore" type="secondary" fill>Xác nhận</base-button>
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
      isActive: false,
      attendance: null,
      scoreModal : false,
      evaluateModal: false,

      polling: false,

      lessonData: null,

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
    demo(){
      return true;
    },
    getAttendanceStatus(studentId) {
      // Lọc danh sách attendance dựa trên studentId
      const studentAttendance = this.attendance.filter(
        (att) => att.user === studentId
      );

      // Nếu không có dữ liệu, trả về trạng thái vắng mặt = 2
      if (studentAttendance.length === 0) {
        return 2;
      }

      // Kiểm tra trạng thái cuối cùng của sinh viên
      const lastStatus = studentAttendance[studentAttendance.length - 1].status;
      return lastStatus
    },
    async startLongPolling() {
      let lastAttendance = []; 
      this.polling = true;

      while (this.polling) {
        try {
          const token = localStorage.getItem("access_token");
          const response = await axios.get(`${API_URL}/attendance/attendance/`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          });

          // Đảm bảo response.data không phải là null
          const newAttendance = response.data || []; // Nếu response.data là null thì sử dụng mảng rỗng

          // So sánh dữ liệu mới với dữ liệu trước đó
          if (JSON.stringify(newAttendance) !== JSON.stringify(lastAttendance)) {
            // Tìm ra các phần tử khác nhau
            const differences = this.getDifferences(lastAttendance, newAttendance);
            if (differences.length > 0) {
              this.attendance = newAttendance;
              console.log('New attendance data:', this.attendance);

              if(differences.length !== newAttendance.length){
                // Thông báo nếu có thay đổi trạng thái
                differences.forEach(difference => {
                  if (difference.status === 1) {
                    this.$notify({
                        type: "success",
                        icon: 'tim-icons icon-badge',
                        title: "Điểm danh thành công",
                        message: `Học sinh ${difference.user}`,
                        timeout: 1000,
                        verticalAlign: "bottom",
                        horizontalAlign: "left",
                    });
                  }
                });
              }

              // Cập nhật dữ liệu trước đó
              lastAttendance = newAttendance;
            }
          }

          // Tiếp tục polling
        } catch (error) {
          console.error('Error fetching attendance data:', error);
          await this.delay(5000); // Tạm dừng nếu có lỗi
        }
      }
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
    scoring(index){
      this.studentDetail.id = index
      this.studentDetail.subject = this.lessonData.subject
      this.studentDetail.semester = this.lessonData.semester

      this.scoreModal = true
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
                message: "Chấm điểm cho học sinh " + this.studentDetail.id+ " thành công",
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
          this.updatePosition(this.draggedStudent, rowIndex, columnIndex);
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
                message: "Đổi vị trí học sinh "+ response.data.student + " thành công",
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
        "user_id_1": student1,
        "user_id_2": student2
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
                message: "Đổi vị trí học sinh "+student1+" và "+student2 + " thành công",
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
        this.$set(this.desks[rowIndex], columnIndex, position.student); 
      });
      return this.desks;
    },
    formatTime(date) {
      return date.toLocaleTimeString();
    },
    goToDashboard() {
      this.polling = false
      this.$router.push('/dashboard');  
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

<style>
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
</style>
