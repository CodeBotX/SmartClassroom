<template>
  <!-- <div class="row"> -->
    <div  v-if="isHomeroomTeacher" class="row">
      <!-- Hiển thị quản lý lớp học nếu là giáo viên chủ nhiệm -->
      <div class="row ml-2">
        <div class="col-md-6">
          <h3 class="font-weight-bold">Quản lý lớp học</h3>
        </div>
        <div class="col-md-6">
          <div
            class="btn-group btn-group-toggle float-right"
            data-toggle="buttons"
          >
            <label
              v-for="(option, index) in adminstrationOption"
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
      </div>
      
      <div v-if="bigLineChart.activeIndex === 0" class="col-12">
        <seating-management v-if="room" :room="room"></seating-management>
      </div>
      <div v-if="bigLineChart.activeIndex === 1" class="col-12">
        <room-detail v-if="room" :room="room"></room-detail>
      </div>
      <div v-if="bigLineChart.activeIndex === 2" class="col-12">
        <weekly-report v-if="room" :room="room"></weekly-report>
      </div>
    </div>

    <!-- Hiển thị thông báo nếu không phải là giáo viên chủ nhiệm -->
    <div v-else class="col-12 text-center">
      <p>Đây là trang dành cho giáo viên chủ nhiệm.</p>
      <p>
        Các giáo viên chủ nhiệm hiện tại:
        <span v-for="teacher in homeroomTeachers" :key="teacher.id">{{ teacher }} | </span>
      </p>
    </div>
  <!-- </div> -->
</template>

<script>
import UserSetting from './Administration/UserSetting.vue'
import SeatingManagement from './HomeroomTeacher/SeatingManagement.vue';
import axios from "../services/axios";
import config from "@/config";
import TimeTable from './EducationProgram/TimeTable.vue';
import TeacherDivision from './EducationProgram/TeacherDivision.vue';
import WeeklyReport from './HomeroomTeacher/WeeklyReport.vue';
import RoomDetail from './HomeroomTeacher/RoomDetail.vue';

let API_URL = "";
 


export default {
    mounted() {
      this.initializeData();
    },
  components: { 
    UserSetting,
    TimeTable,
    TeacherDivision,
    SeatingManagement,
    WeeklyReport,
    RoomDetail
  },
  computed: {
    adminstrationOption() {
      return this.$t("dashboard.homeroomTeacher");
    },
  },
  data() {
    return {
    rooms: null,
    room: null,
    isHomeroomTeacher: false,
    homeroomTeachers: [], // Danh sách các giáo viên chủ nhiệm
      bigLineChart: {
        activeIndex: 0,
        index: "Quản trị",
        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: [],
      },
    }
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
    },
    async initializeData() {
        try {
          await this.getApiUrl();
          await this.getRoomData();
          await this.getUserData();
          await this.checkHomeroomTeacher();
         
        } catch (error) {
          console.error('Error initializing data:', error);
        }
    },
    checkHomeroomTeacher() {
      // Kiểm tra xem this.rooms có dữ liệu trước khi sử dụng map
      if (this.rooms && this.rooms.length > 0) {
        // Lấy danh sách giáo viên chủ nhiệm từ các phòng
        this.homeroomTeachers = this.rooms.map(item => item.homeroom_teacher);
        console.log(this.homeroomTeachers);

        // Duyệt qua danh sách rooms để kiểm tra xem user_id có phải là homeroom_teacher không
        for (const room of this.rooms) {
          if (room.homeroom_teacher && String(room.homeroom_teacher) === String(this.userData.user_id)) {
            this.isHomeroomTeacher = true;
            this.room = room; // Lưu phòng phù hợp vào this.room
            console.log(this.room)
            break; // Thoát khỏi vòng lặp sau khi tìm thấy phòng phù hợp
          }
        }
        // Nếu không tìm thấy, đảm bảo isHomeroomTeacher là false
        if (!this.isHomeroomTeacher) {
          console.warn("User không phải là giáo viên chủ nhiệm của bất kỳ lớp nào.");
          this.room = null;
        }
      } else {
        console.warn("Không có dữ liệu phòng học.");
        this.homeroomTeachers = [];
        this.isHomeroomTeacher = false;
        this.room = null;
      }
    },
    getUserData(){
        this.userData = JSON.parse(localStorage.getItem('user_data'));
    },
    getApiUrl() {
    return new Promise((resolve) => {
        API_URL = this.$t("dashboard.apiURL");
        resolve();
        });
    },
    getRoomData(){
        const token = localStorage.getItem("access_token");

  return axios
    .get(API_URL + "/rooms/roomset/", {
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
    .then((response) => {
      this.rooms = response.data;
      console.log(this.rooms);
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
  }

}
</script>

<style>

</style>