<template>
  <div class="row">
    <div class="col-12">
      <card>
        <!-- GIÁO VIÊN -->
        <div>
          <base-table :data="divisionData" :columns="division_columns">
            <template slot="columns">
              <th>Giáo viên</th>
              <th>Môn dạy</th>
              <th>Lớp dạy</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.teacher }}</td>
              <td>{{ row.subject }}</td>
              <!-- <td>{{ row.room.join(', ') }}</td> -->
              <td>{{ row.room }}</td>
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

        <!-- Thêm phân công Modal -->
        <modal :show.sync="divisionCreateModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm" @close="closeCreateModal">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0"
                  v-if="divisionDetail">
                  
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thêm phân công giáo viên</h4>
                        <h3>{{ divisionDetail.user_id }}</h3>
                        <h4>Môn {{ divisionDetail.subject }}</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                  <div class="col-md-12 pr-md-1 text-center">          
                                        <select class="btn btn-simple btn-lg btn-success" v-model="roomSelected">
                                          <option class="text-info" v-for="(room, index) in roomData" :key="index" :value="room" >{{ room.name }}</option>
                                        </select>
                                  </div>
                                </div>

                                <base-button @click="updateDivision" type="secondary" fill>Thêm</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>

        <!-- xóa phân công Modal -->
        <modal :show.sync="divisionDeleteModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm" @close="closeCreateModal">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0"
                  v-if="divisionDetail">
                  
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Xóa phân công giáo viên</h4>
                        <h3>{{ divisionDetail.user_id }}</h3>
                        <h4>Môn {{ divisionDetail.subject }}</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                  <div class="col-md-12 pr-md-1 text-center">          
                                        <select class="btn btn-simple btn-lg btn-success" v-model="roomSelected">
                                          <option class="text-info" v-for="(room, index) in roomData" :key="index" :value="room" >{{ room.name }}</option>
                                        </select>
                                  </div>
                                </div>

                                <base-button @click="deleteDivision" type="secondary" fill>Xóa</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>
      </card>
    </div>
  </div>

  
</template>

<script>
import Card from "../../components/Cards/Card.vue";
import BaseTable from '../../components/BaseTable.vue';
import axios from "../../services/axios";
import Modal from '../../components/Modal.vue';

let API_URL = "";

export default {
    components: { Card, BaseTable, Modal },
    mounted() {
      this.initializeData();
    },
    data() {
        return {
            divisionCreateModal: false,
            divisionDeleteModal: false,
            divisionDetail: null,
            roomData: [],
            roomSelected: null,

            roomDivisionData: null,

            divisionData: null,
            division_columns: ["user_id", "subject", "room"],
        };
    },
    methods: {
      async initializeData() {
        try {
          await this.getApiUrl();
          await this.getDivisionData();
          await this.getRoomData();
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
      getRoomData() {
        const token = localStorage.getItem("access_token");

        axios
          .get(API_URL + "/rooms/roomset/", {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.roomData = response.data;
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
      getDivisionData() {
        const token = localStorage.getItem("access_token");

        axios
          .get(API_URL + "/adminpanel/assignments/", {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.divisionData = response.data;
            console.log(this.divisionData)
          })
          .catch((error) => {
            console.error("Error getting room data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy danh sách phân công giáo viên thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
      toggleCreateDivision(teacher) {
        this.divisionCreateModal = true;
        this.divisionDetail = teacher;
        this.roomDivisionData = teacher.rooms
      },
      toggleDeleteDivision(teacher){
        this.divisionDeleteModal = true;
        this.divisionDetail = teacher;
        this.roomDivisionData = teacher.rooms
      },
      deleteDivision() {
        const index = this.roomDivisionData.indexOf(this.roomSelected);
        if(index == -1){
          this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Giáo viên "+ this.divisionDetail.user_id+" không được phân công lớp "+this.roomSelected.name,
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
            return
        }
        const tempRooms = [...this.roomDivisionData]
        tempRooms.splice(index, 1);

        const token = localStorage.getItem("access_token");
        const data = {
          rooms: tempRooms
        }

        axios
          .patch(API_URL + "/adminpanel/assignments/"+ this.divisionDetail.user_id+"/",data, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then(() => {
            this.divisionCreateModal = false;
            this.roomDivisionData = tempRooms
            this.$notify({
              type: "success",
              icon: 'tim-icons icon-bell-55',
              message: "Xóa phân công giáo viên thành công",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          })
          .catch((error) => {
            console.error("Error :", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Xóa phân công giáo viên thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
      updateDivision() {
        if(this.roomDivisionData.includes(this.roomSelected.name)){
          this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Giáo viên "+ this.divisionDetail.user_id+" đã được phân công lớp "+this.roomSelected.name,
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
            return
        }
        const tempRooms = [...this.roomDivisionData]
        tempRooms.push(this.roomSelected.name)

        const token = localStorage.getItem("access_token");
        const data = {
          rooms: tempRooms
        }

        axios
          .patch(API_URL + "/adminpanel/assignments/"+ this.divisionDetail.user_id+"/",data, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then(() => {
            this.divisionCreateModal = false;
            this.roomDivisionData = tempRooms
            this.$notify({
              type: "success",
              icon: 'tim-icons icon-bell-55',
              message: "Thêm phân công giáo viên thành công",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          })
          .catch((error) => {
            console.error("Error :", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Phân công giáo viên thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
      closeCreateModal(){
        this.roomSelected = null
      },
    }
}
</script>

<style>

</style>