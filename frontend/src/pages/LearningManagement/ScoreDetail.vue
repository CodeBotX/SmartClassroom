<template>
  <div class="row">
    <div class="col-12">
      <card>
        <template slot="header">
          <div class="row">
            <div class="col-md-5">
              <h3>Bảng điểm {{ roomSelected ? " Lớp "+ roomSelected.room : "" }} </h3>
            </div>
            <div class="col-md-7">
              <div class="row">
                <div class="col-md-3 pr-md-1 text-center">
                  <base-input label="Học kỳ">
                    <select class="btn btn-simple btn-sm btn-success" v-model="semesterSelected">
                      <option class="text-info" v-for="(semester, index) in semesters" :key="index" :value="semester">{{ semester.name }}</option>
                    </select>
                  </base-input>
                </div>
                <div class="col-md-3 pl-md-1 text-center">
                  <base-input label="Lớp">
                    <select class="btn btn-simple btn-sm btn-success" v-model="roomSelected" @change="getStudents(roomSelected.room)">
                    <option class="text-info" v-for="(room, index) in roomOption" :key="index" :value="room" >{{ room.room }}</option>
                    </select>
                  </base-input>
                </div>
                <div class="col-md-3 pr-md-1 text-center">
                  <base-input label="Loại điểm">
                    <select class="btn btn-simple btn-sm btn-success" v-model="scoreTypeSelected">
                      <option class="text-info" v-for="scoreType in scoreTypes" :key="scoreType" :value="scoreType" >{{ scoreType }}</option>
                    </select>
                  </base-input>
                </div>
                <div class="col-md-3 pl-md-1 text-center">
                  <base-button 
                    class="btn btn-sm "
                    @click="getScoreData"
                    fill
                  >Lọc
                  </base-button>
                </div>
              </div>
            </div>
          </div>
        </template>

        <!-- Bảng điểm -->
        <div>
          <base-table :data="scoreData" :columns="score_columns">
            <template slot="columns">
              <th>Học sinh</th>
              <th>Điểm</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.student.full_name }}</td>
              <td>{{ row.grade.join( ", ") }}</td>
              <td class="td-actions text-right">
                <base-button v-if="(currentScoreType !== 'TX') && row.grade.length === 0" type="info" class="btn-simple" size="md" icon @click="toggleDetailScore(row)">
                  <i class="tim-icons icon-pencil"></i>
                </base-button>
                <!-- <base-button v-if="(scoreTypeSelected !== 'TX') && row.grade.length !== 0" type="info" class="btn-simple" size="md" icon @click="toggleUpdateScore(row)">
                  <i class="tim-icons icon-refresh-02"></i>
                </base-button> -->
              </td>
            </template>
          </base-table>
        </div>
        
      </card>
      <!-- score detail Modal -->
        <modal :show.sync="scoreDetailModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0"
                  v-if="scoreDetail">
                  
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Nhập điểm {{this.scoreTypeSelected}} học sinh {{ scoreDetail.student.full_name }}</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                  <div class="col-md-12 pr-md-1 text-center">          
                                        <base-input type="number" label="Điểm" v-model="createScore"></base-input>
                                  </div>
                                </div>

                                <base-button @click="createGrade" type="secondary" fill>Luu</base-button>
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
import BarChart from "@/components/Charts/BarChart";
let API_URL = "";

export default {
    components: { Card, BaseTable, Modal, BarChart },
    mounted() {
      this.initializeData();
    },
    computed: {
      formattedGrade: {
        get() {
          return this.scoreDetail.grade.join(", "); // Chuyển mảng thành chuỗi khi hiển thị
        },
        set(value) {
          // Chuyển chuỗi thành mảng và lọc ra các phần tử hợp lệ là số
          this.scoreDetail.grade = value
            .split(",")
            .map(item => item.trim()) // Loại bỏ khoảng trắng thừa
            .map(item => Number(item)) // Chuyển sang số
            .filter(item => !isNaN(item)); // Chỉ giữ lại số hợp lệ
        },
      }
    },
    data() {
        return {
          currentScoreType: null,

          createScore: null,
          scoreDetailModal: false,
          scoreDetail: null,
          score_columns: ["student", "grade"],
          roomSelected: null,
          semesterSelected: null,
          scoreTypeSelected: null,

          students: null,

          scoreData: null,
          userData: null,
          roomOption: null,
          semesters: null,
          scoreTypes: ["TX", "GK", "CK"],
          subject: null,
          
        };
    },
    methods: {
      async initializeData() {
        try {
          await this.getApiUrl();
          await this.getSemesterData();
          await this.getUserData();
          await this.getRoomOption();
        } catch (error) {
          console.error('Error initializing data:', error);
        }
      },
      getStudents(roomName){
        const token = localStorage.getItem("access_token");
        
          axios
          .get(API_URL+`/rooms/roomset/${roomName}/students/`, {
            headers: {
              Authorization: `Bearer ${token}`, // Đính kèm token vào headers
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
              this.students = response.data
          })
          .catch((error) => {
            console.error("Error get lesson data :", error);

            this.$notify({
                  type: "warning",
                  icon: 'tim-icons icon-bell-55',
                  message: "Lấy chi tiết danh sách học sinh thất bại",
                  timeout: 3000,
                  verticalAlign: "top",
                  horizontalAlign: "right",
                });
          });
      },
      getUserData(){
        this.userData = JSON.parse(localStorage.getItem('user_data'));
        this.subject = this.userData.subject
      },
      getApiUrl() {
        return new Promise((resolve) => {
          API_URL = this.$t("dashboard.apiURL");
          resolve();
        });
      },
      getRoomOption(){
        const token = localStorage.getItem("access_token");

        axios
          // .get(API_URL + "/adminpanel/assignments/"+this.userData.user_id+"/", { //lấy lớp của giáo viên đang dạy
          // .get(API_URL + "/rooms/roomset/", {  //lấy tất cả các lớp
          .get(API_URL + `/adminpanel/assignments/?user_id=${this.userData.user_id}`, {
          
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            
            this.roomOption = response.data;
            console.log(this.roomOption)
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
      initializeScoreData() {
        return Array.from({ length: this.students.length }, (_, index) => ({
          student: this.students[index],
          grade: [],
        }));
      },
      formatScoreData(data) {
          const groupedScores = {};

          // Khởi tạo với tất cả các môn để đảm bảo mỗi môn đều có một dòng trong bảng
          this.initializeScoreData().forEach(item => {
            groupedScores[item.student.user] = {
              student: item.student,
              grade: [],
            };
          });

          // Cập nhật dữ liệu điểm thực tế từ API
          data.forEach(item => {
            if (groupedScores[item.student]) {      
                groupedScores[item.student].grade = item.grade;
            }
          });
          console.log(groupedScores)

          // Chuyển đổi đối tượng groupedScores thành mảng để dễ hiển thị trong bảng
          return Object.values(groupedScores);
      },
//       getScoreData(){
//         const data = [
//     {
//         "subject": "TOAN",
//         "score_type": "TX",
//         "grade": [
//             8.0
//         ],
//         "student": "3581635860",
//         "semester": 20241
//     },
//     {
//         "subject": "TOAN",
//         "score_type": "TX",
//         "grade": [
//             7.0
//         ],
//         "student": "3581635904",
//         "semester": 20241
//     }
// ]
//           this.scoreData = this.formatScoreData(data);
//       },
      getSubject(subjectName){
        switch(subjectName){
          case "Toán": return "TOAN";
          case "Ngữ Văn": return "VAN"
          case "Tiếng Anh": return "ANH"
          case "Hoá": return "KHTN_HOA"
          case "Vật lý": return "KHTN_LY"
          case "Sinh học": return "KHTN_SINH"
          case "Địa lý": return "KHXH_DIA"
          case "Lịch sử": return "KHXH_SU"
          case "GDCD": return "KHXH_GDCD"
          case "Thể dục": return "TD"
          case "Mỹ thuật": return "MT"
          case "Âm nhạc": return "AN"
          case "Tin học": return "TH"
          case "Công nghệ": return "CN"
          case "Hoạt động trại nghiệm, hướng nghiệp": return "HDTN-HN"
        }
      },
      getScoreData(){
        const subject = this.getSubject(this.userData.subjects)
        this.currentScoreType = this.scoreTypeSelected;
        
        const token = localStorage.getItem("access_token");
        this.scoreData = this.initializeScoreData()

        axios
          .get(API_URL + `/adminpanel/grades?semester_name=${this.semesterSelected.name}&score_type=${this.scoreTypeSelected}&subject=${subject}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            // Xử lý dữ liệu để sắp xếp theo từng môn
            this.$notify({
              type: "success",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy bảng điểm thành công",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
            this.scoreData = this.formatScoreData(response.data);
          })
          .catch((error) => {
            console.error("Error getting score data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy danh sách điểm thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
      createGrade() {
        //update diem
        const token = localStorage.getItem("access_token");
        const data = {
        "student": this.scoreDetail.student.user,
        "subject": this.getSubject(this.userData.subjects),
        "semester": this.semesterSelected.name,
        // "semester":20241,
        "score_type": this.scoreTypeSelected,
        "grade": parseFloat(this.createScore)
    }

      console.log(data)
        axios
          .post(API_URL + `/adminpanel/grades/`,data, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            // Xử lý dữ liệu để sắp xếp theo từng môn
            this.$notify({
              type: "success",
              icon: 'tim-icons icon-bell-55',
              message: "Nhập điểm thành công",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
            this.scoreDetailModal = false
            this.getScoreData()
          })
          .catch((error) => {
            console.error("Error getting score data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Nhập điểm thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
      toggleDetailScore(index){
        this.scoreDetail = index
        this.scoreDetailModal = true;
      }
    },
    
};
</script>

<style>

</style>
