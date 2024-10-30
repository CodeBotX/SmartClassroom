<template>
  <div class="row">
    <div class="col-12">
      <card>
        <template slot="header">
          <div class="row">
            <div class="col-md-5">
              <h3>Bảng điểm {{ roomSelected ? " Lớp "+ roomSelected.name : "" }} </h3>
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
                    <select class="btn btn-simple btn-sm btn-success" v-model="roomSelected">
                    <option class="text-info" v-for="(room, index) in roomOption" :key="index" :value="room" >{{ room.name }}</option>
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
              <td>{{ row.student }}</td>
              <td>{{ row.grade.join( ", ") }}</td>
              <td class="td-actions text-right">
                <base-button type="info" class="btn-simple" size="md" icon @click="toggleDetailScore(row)">
                  <i class="tim-icons icon-pencil"></i>
                </base-button>
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
                        <h4 class="text-success">Thong tin diem {{this.scoreTypeSelected}} hoc sinh {{ scoreDetail.student }}</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                  <div class="col-md-12 pr-md-1 text-center">          
                                        <base-input label="Diem" v-model="formattedGrade"></base-input>
                                  </div>
                                </div>

                                <base-button @click="updateScore" type="secondary" fill>Luu</base-button>
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
          scoreDetailModal: false,
          scoreDetail: null,
          score_columns: ["student", "grade"],
          roomSelected: null,
          semesterSelected: null,
          scoreTypeSelected: null,

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
          .get(API_URL + "/rooms/roomset/", {  //lấy tất cả các lớp
          
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.roomOption = response.data;
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
        const students = [
          "181635895",
          "3581635860",
          "3581635861",
          "3581635862",
          "3581635894",
          "3581635896",
          "3581635904",
          "3681635897"
        ]
        return Array.from({ length: students.length }, (_, index) => ({
          student: students[index],
          grade: [],
        }));
      },
      // initializeScoreData() {
      //   //Lấy danh sách lớp học
      //   const token = localStorage.getItem("access_token");
      //   let students = [];

      //   axios
      //     .get(API_URL + "/rooms/roomset/"+this.roomSelected.name, {
      //       headers: {
      //         Authorization: `Bearer ${token}`,
      //         "Content-Type": "application/json",
      //       },
      //     })
      //     .then((response) => {
      //        students = response.data.students;
      //     })
      //     .catch((error) => {
      //       console.error("Error getting room data:", error);
      //       this.$notify({
      //         type: "warning",
      //         icon: 'tim-icons icon-bell-55',
      //         message: "Lấy danh sách lớp học thất bại",
      //         timeout: 3000,
      //         verticalAlign: "top",
      //         horizontalAlign: "right",
      //       });
      //     });

      //   return Array.from({ length: students.length }, (_, index) => ({
      //     student: students[index],
      //     grade: [],
      //   }));
      // },
      formatScoreData(data) {
          const groupedScores = {};

          // Khởi tạo với tất cả các môn để đảm bảo mỗi môn đều có một dòng trong bảng
          this.initializeScoreData().forEach(item => {
            groupedScores[item.student] = {
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

          // Chuyển đổi đối tượng groupedScores thành mảng để dễ hiển thị trong bảng
          return Object.values(groupedScores);
      },
      getScoreData(){
        const data = [
            {
                "subject": "TOAN",
                "score_type": "TX",
                "grade": [
                    7.0,
                    8.0,
                    5.0
                ],
                "student": "3581635862",
                "semester": 20241
            }
        ]
          this.scoreData = this.formatScoreData(data);
      },
      // getScoreData(){
      //   const token = localStorage.getItem("access_token");
      //   this.scoreData = this.initializeScoreData()

      //   axios
      //     .get(API_URL + `/adminpanel/grades?user_id=${this.userData.user_id}&semester_name=${this.semesterSelected.name}`, {
      //       headers: {
      //         Authorization: `Bearer ${token}`,
      //         "Content-Type": "application/json",
      //       },
      //     })
      //     .then((response) => {
      //       // Xử lý dữ liệu để sắp xếp theo từng môn
      //       this.$notify({
      //         type: "success",
      //         icon: 'tim-icons icon-bell-55',
      //         message: "Lấy bảng điểm thành công",
      //         timeout: 3000,
      //         verticalAlign: "top",
      //         horizontalAlign: "right",
      //       });
      //       this.scoreData = this.formatScoreData(response.data);
      //     })
      //     .catch((error) => {
      //       console.error("Error getting score data:", error);
      //       this.$notify({
      //         type: "warning",
      //         icon: 'tim-icons icon-bell-55',
      //         message: "Lấy danh sách điểm thất bại",
      //         timeout: 3000,
      //         verticalAlign: "top",
      //         horizontalAlign: "right",
      //       });
      //     });
      // },
      updateScore() {
        // Chuyển đổi các giá trị từ chuỗi thành số nguyên
        this.scoreDetail.grade = this.scoreDetail.grade.map(Number);
        console.log(this.scoreDetail.grade);
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
