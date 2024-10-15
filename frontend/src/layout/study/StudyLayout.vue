<template>
  <div class="wrapper study">
    <div class="header">
      <base-button @click="goToDashboard" class="dashboard-button btn-primary" simple>
        <i class="tim-icons icon-minimal-left"></i> Trang chủ
      </base-button>
      <h1 class="title">Study Layout</h1>
      <div class="current-time">{{ currentTime }}</div>
    </div>
    
    <div class="classroom-layout">
      <div v-for="(row, rowIndex) in desks" :key="rowIndex" class="row">
        <div v-for="(seat, columnIndex) in row" :key="columnIndex"
         :class="['seat', 
                      { 'spacer': columnIndex === 2 || columnIndex === 5 }]"  
         @dragover.prevent @drop="dropStudent(rowIndex, columnIndex)" @dragstart="dragStart(seat,rowIndex,columnIndex)">
          <base-button
            v-if="seat"
            class="btn btn-info btn-simple student"
            draggable
            
          >
            {{ seat }} <!-- Assuming 'seat' is an object with 'student' having a 'name' property -->
          </base-button>
        </div>
      </div>

      <div class="teacher-desk">
        <h3>Bàn giáo viên</h3>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../../services/axios'; 
let API_URL = ""

export default {
  data() {
    return {
      currentTime: this.formatTime(new Date()),
      positions: null,
      desks: Array.from({ length: 5 }, () => Array(9).fill(null)),
      draggedStudent: null,
      draggedRow: null,
      draggedCol: null,
    };
  },
  methods: {
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
      this.$router.push('/dashboard');  
    },
    async getPositionData() {
      const roomName = "6A"; 
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
  margin-right: 100px; /* Khoảng cách giữa các cột */
}
</style>
