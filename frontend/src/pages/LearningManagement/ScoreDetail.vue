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
                    @click="getChartData"
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
          <base-table :data="scoreData" :columns="division_columns">
            <template slot="columns">
              <th>ID</th>
              <th>Học sinh</th>
              <th>Điểm</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.user_id }}</td>
              <td>{{ row.subject }}</td>
              <td>{{ row.rooms.join(', ') }}</td>
              <td class="td-actions text-right">
                <base-button type="info" class="btn-simple" size="md" icon @click="toggleCreateDivision(row)">
                  <i class="tim-icons icon-simple-add"></i>
                </base-button>
                <base-button type="danger" class="btn-simple" size="md" icon @click="toggleDeleteDivision(row)">
                  <i class="tim-icons icon-simple-remove"></i>
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
    },
};
</script>

<style>

</style>
