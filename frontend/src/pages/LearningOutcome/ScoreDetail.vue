<template>
  <div class="row">
    <div class="col-12">
      <card>
        <template slot="header">
          <div class="row">
            <div class="col-md-5">
              <h3>Bảng điểm</h3>
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
                <!-- <div class="col-md-3 pr-md-1 text-center">
                  <base-input label="Loại điểm">
                    <select class="btn btn-simple btn-sm btn-success" v-model="scoreTypeSelected">
                      <option class="text-info" v-for="scoreType in scoreTypes" :key="scoreType" :value="scoreType" >{{ scoreType }}</option>
                    </select>
                  </base-input>
                </div> -->
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
              <th>Môn</th>
              <th class="text-center">Thường xuyên</th>
              <th class="text-center">Giữa kỳ</th>
              <th class="text-center">Cuối kỳ</th>
            </template>
            <template slot-scope="{ row }">
              <td> <div class="text-info"> {{ row.subject }}</div></td>

              <td class="text-center">{{ row.tx.join(" | ") }}</td>
              <td class="text-center">{{ row.gk.join(" ") }}</td>
              <td class="text-center">{{ row.ck.join(" ") }}</td>
            </template>
          </base-table>
        </div>
        
      </card>

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
    data() {
        return {
          scoreData: this.initializeScoreData(), // Dữ liệu điểm đã được định dạng
          score_columns: ['Môn', 'Thường xuyên', 'Giữa kỳ', 'Cuối kỳ'], // Cột của bảng

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
      initializeScoreData() {
        const subjects= ['TOAN', 'VAN', 'ANH', 'KHTN_HOA', 'KHTN_LY', 'KHTN_SINH', 'KHXH_DIA', 'KHXH_SU', 'KHXH_GDCD', 'TD', 'MT', 'AN', 'TH', 'CN', 'HDTN-HN'];
        return Array.from({ length: 15 }, (_, index) => ({
          subject: subjects[index],
          tx: [],
          gk: [],
          ck: [],
        }));
      },
      async initializeData() {
        try {
          await this.getApiUrl();
          await this.getSemesterData();
          await this.getUserData();
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
      // getScoreData(){
      //   const data = [
      //         {
      //             "subject": "VAN",
      //             "score_type": "TX",
      //             "grade": [
      //                 6.0,
      //                 6.0,
      //                 5.5,
      //                 5.5,
      //                 6.5,
      //                 6.5
      //             ],
      //             "student": "0181635895",
      //             "semester": 20242
      //         },
      //         {
      //             "subject": "TOAN",
      //             "score_type": "TX",
      //             "grade": [
      //                 10.0,
      //                 8.0,
      //                 9.0,
      //                 9.0
      //             ],
      //             "student": "0181635895",
      //             "semester": 20242
      //         },
      //         {
      //             "subject": "TOAN",
      //             "score_type": "GK",
      //             "grade": [
      //                 8.0
      //             ],
      //             "student": "0181635895",
      //             "semester": 20242
      //         },
      //         {
      //             "subject": "TOAN",
      //             "score_type": "CK",
      //             "grade": [
      //                 8.0
      //             ],
      //             "student": "0181635895",
      //             "semester": 20242
      //         }
      //     ]
      //     this.scoreData = this.formatScoreData(data);
      // },
      getScoreData(){
        const token = localStorage.getItem("access_token");
        this.scoreData = this.initializeScoreData()

        axios
        // .get(API_URL + `/grades?student=${this.userData.user_id}&semester_name=${this.semesterSelected.name}`, {
          .get(API_URL + `/adminpanel/grades?student=${this.userData.user_id}&semester_name=${this.semesterSelected.name}`, {
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
      // formatScoreData(data) {
      //   const groupedScores = {};

      //   data.forEach(item => {
      //     // Kiểm tra xem môn học này đã tồn tại trong groupedScores chưa
      //     if (!groupedScores[item.subject]) {
      //       groupedScores[item.subject] = {
      //         subject: item.subject,
      //         tx: [],  // Điểm thường xuyên
      //         gk: [],  // Điểm giữa kỳ
      //         ck: []   // Điểm cuối kỳ
      //       };
      //     }

      //     // Sắp xếp điểm vào đúng loại điểm (TX, GK, CK)
      //     if (item.score_type === "TX") {
      //       groupedScores[item.subject].tx = item.grade;
      //     } else if (item.score_type === "GK") {
      //       groupedScores[item.subject].gk = item.grade;
      //     } else if (item.score_type === "CK") {
      //       groupedScores[item.subject].ck = item.grade;
      //     }
      //   });

      //   // Chuyển đổi đối tượng thành mảng để dễ hiển thị trong bảng
      //   return Object.values(groupedScores);
      // },
      formatScoreData(data) {
          const groupedScores = {};

          // Khởi tạo với tất cả các môn để đảm bảo mỗi môn đều có một dòng trong bảng
          this.initializeScoreData().forEach(subjectEntry => {
            groupedScores[subjectEntry.subject] = {
              subject: subjectEntry.subject,
              tx: [],
              gk: [],
              ck: []
            };
          });

          // Cập nhật dữ liệu điểm thực tế từ API
          data.forEach(item => {
            if (groupedScores[item.subject]) {
              // Thêm điểm vào đúng loại (TX, GK, CK)
              if (item.score_type === "TX") {
                groupedScores[item.subject].tx = item.grade;
              } else if (item.score_type === "GK") {
                groupedScores[item.subject].gk = item.grade;
              } else if (item.score_type === "CK") {
                groupedScores[item.subject].ck = item.grade;
              }
            }
          });

          // Chuyển đổi đối tượng groupedScores thành mảng để dễ hiển thị trong bảng
          return Object.values(groupedScores);
      },

    },
};
</script>

<style>

</style>
