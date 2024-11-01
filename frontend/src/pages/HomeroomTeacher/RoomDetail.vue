<template>
  <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" >
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Danh sách học sinh lớp {{room.name}}</h4>
                    </div>
                </template>
                <template>
                    <base-table :data="students" :columns="student_columns">
                    <template slot="columns">
                      <th>ID</th>
                      <th>Học sinh</th>
                      <th>Giới tính</th>
                      <th>Ngày sinh</th>
                      <th>Tình trạng</th>
                    </template>
                    <template slot-scope="{ row }">
                      <td>{{ row.user }}</td>
                      <td>{{ row.full_name }}</td>
                      <td>{{ row.sex }}</td>
                      <td>{{ row.day_of_birth }}</td>
                      <td>{{ row.active_status }}</td>
                    </template>
                  </base-table>
                </template>
            </card>
</template>

<script>
import Card from "../../components/Cards/Card.vue";
import BaseTable from '../../components/BaseTable.vue';
import axios from "../../services/axios";
let API_URL ="";

export default {
components: {Card, BaseTable},
props: {
    room: {
      type: Object, 
      required: true,
      default: "room",
    }
  },
  mounted() {
    this.initializeData();
  },
  data(){
    return {
        students: null,
        student_columns: ["user", "full_name", "sex", "day_of_birth", "active_status"],
    }
  },
  methods: {
    async initializeData() {
      try {
        await this.getApiUrl();
        await this.getStudents(this.room.name);
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
  }

}
</script>

<style>

</style>