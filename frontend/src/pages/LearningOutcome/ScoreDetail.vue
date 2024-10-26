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
              <th>Thường xuyên</th>
              <th>Giữa kỳ</th>
              <th>Cuối kỳ</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.subject }}</td>
              <td>{{ row.TX ? row.TX : '-' }}</td> <!-- Hiển thị '-' nếu không có điểm -->
              <td>{{ row.GK ? row.GK : '-' }}</td>
              <td>{{ row.CK ? row.CK : '-' }}</td>
              <td class="td-actions text-right">
                <base-button type="info" class="btn-simple" size="md" icon @click="editScore(row)">
                  <i class="tim-icons icon-pencil"></i>
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
          scoreData: [], // Dữ liệu điểm đã được định dạng
          score_columns: ['Môn', 'Thường xuyên', 'Giữa kỳ', 'Cuối kỳ', 'Actions'], // Cột của bảng

          roomSelected: null,
          semesterSelected: null,
          scoreTypeSelected: null,

          scoreData: null,
          userData: null,
          roomOption: null,
          semesters: null,
          scoreTypes: ["TX", "GK", "CK"],
          subject: null,
          

          scoreRow: {
            Toan: {
              Tx: null,
              Gk: null,
              Ck: null,
            },
            Van: {
              Tx: null,
              Gk: null,
              Ck: null
            }
          }
        };
    },
    methods: {
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
      getScoreData(){
        const token = localStorage.getItem("access_token");

        axios
          .get(API_URL + `/adminpanel/grades?user_id=${this.userData.user_id}&semester_name=${this.semesterSelected.name}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            // Xử lý dữ liệu để sắp xếp theo từng môn
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
      formatScoreData(data) {
        // Khởi tạo một đối tượng để nhóm điểm theo môn
        const groupedScores = {};

        data.forEach(item => {
            if (!groupedScores[item.subject]) {
                groupedScores[item.subject] = {
                    subject: item.subject,
                    TX: null,  // Điểm thường xuyên
                    GK: null,  // Điểm giữa kỳ
                    CK: null   // Điểm cuối kỳ
                };
            }

            // Sắp xếp điểm vào đúng loại điểm (TX, GK, CK)
            groupedScores[item.subject][item.score_type] = item.grade;
        });

        // Chuyển đổi đối tượng thành mảng để dễ hiển thị trong bảng
        return Object.values(groupedScores);
      },
    },
};
</script>

<style>

</style>
