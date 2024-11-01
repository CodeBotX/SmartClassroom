<template>
  <div class="row">
    <div class="col-12">
      <card>
        <!-- GIÁO VIÊN -->
        <!-- <div>
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
               <td>{{ row.room.join(', ') }}</td> comment
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
        </div> -->
        <div class="card-container">
          <div
            v-for="(room, index) in roomData"
            :key="index"
            class="card-item"
          >
            <card class="text-center" style="width: 10rem;">
              <h4 class="card-title text-info">{{ room.name }}</h4>
              <base-button type="info" size="sm" icon @click="toggleDivisionDetail(room)">
                <i class="tim-icons icon-settings-gear-63"></i>
              </base-button>
            </card>
          </div>
        </div>
        <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.roomSelected">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Chi tiết phân công giáo viên lớp {{roomSelected.name}}</h4>
                        <base-input label="Học kỳ">
                          <select class="btn btn-simple btn-sm btn-success" v-model="semesterSelected" @change="getRoomDivision">
                            <option class="text-info" v-for="(semester, index) in semesters" :key="index" :value="semester.name">{{ semester.name }}</option>
                          </select>
                        </base-input>
                    </div>
                </template>
                <template>
                    <base-table :data="teacherDivisionData" :columns="division_columns">
                      <template slot="columns">
                        <th>Môn</th>
                        <th class="text-center">Giáo viên</th>
                        <th class="text-center">Actions</th>
                      </template>
                      <template slot-scope="{ row }">
                        <td> <div class="text-info"> {{ row.subject }}</div></td>

                        <td class="text-center">{{ row.teacher }}</td>
                        <td class="td-actions text-right">
                          <base-button v-if="!row.teacher" type="success" class="btn-simple" size="md" icon @click="toggleCreateDivision(row)">
                            <i class="tim-icons icon-simple-add"></i>
                          </base-button>
                          <base-button v-else type="info" class="btn-simple" size="md" icon @click="toggleDetailDivision(row)">
                            <i class="tim-icons icon-single-02"></i>
                          </base-button>
                        </td>
                      </template>
                    </base-table>
                </template>
            </card>
  
        <!-- Thêm phân công Modal -->
        <modal :show.sync="divisionCreateModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0"
                  v-if="teacherDivisionDetail" >
                  
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thêm phân công giáo viên môn {{this.teacherDivisionDetail.subject}} lớp {{this.roomSelected.name}}</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                  <div class="col-md-12 pr-md-1 text-center">          
                                        <select class="btn btn-simple btn-lg btn-success" v-model="teacherDivisionDetail.teacher">
                                          <option class="text-info" v-for="(teacher, index) in teachers" :key="index" :value="teacher.user" >{{ teacher.full_name }}</option>
                                        </select>
                                  </div>
                                </div>

                                <base-button @click="createDivision" type="secondary" fill>Thêm</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>

        <!-- Update phân công Modal -->
        <modal :show.sync="divisionUpdateModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0"
                  v-if="teacherDivisionDetail" >
                  
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Cập nhật phân công giáo viên môn {{this.teacherDivisionDetail.subject}} lớp {{this.roomSelected.name}}</h4>
                    </div>
                </template>
                <template>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                  <div class="col-md-12 pr-md-1 text-center">          
                                        <select class="btn btn-simple btn-lg btn-success" v-model="teacherDivisionDetail.teacher">
                                          <option class="text-info" v-for="(teacher, index) in teachers" :key="index" :value="teacher.user" >{{ teacher.full_name }}</option>
                                        </select>
                                  </div>
                                </div>

                                <base-button @click="updateDivision" type="secondary" fill>Thêm</base-button>
                            </div>
                        </div>
                </template>
            </card>
        </modal>
        <!-- <modal :show.sync="divisionDeleteModal">
            <h4 slot="header" class="modal-title" id="modal-title-default">Xác nhận xóa phân công giáo viên này</h4>
            <template slot="footer">
                <base-button type="secondary" @click="deleteDivision">Xác nhận</base-button>
                <base-button type="danger" class="ml-auto" @click="divisionDeleteModal = false">Hủy
                </base-button>
            </template>
        </modal> -->
        <modal :show.sync="teacherDetailModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
          <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thông tin giáo viên</h4>
                    </div>
                </template>
                <template v-if="teacherDetail">
                    <fieldset disabled>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="teacherDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="teacherDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Môn dạy" v-model="teacherDetail.subjects"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Giới tính" v-model="teacherDetail.sex"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày sinh" v-model="teacherDetail.day_of_birth"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Dân tộc" v-model="teacherDetail.nation"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Học vấn" v-model="teacherDetail.expertise_levels"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Chức vụ" v-model="teacherDetail.contract_types"></base-input>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>  
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
            divisionDetailModal: false,
            divisionCreateModal: false,
            divisionUpdateModal: false,
            teacherDetailModal: false,
            teacherDetail: null,
            divisionDetail: null,
            roomData: [],
            roomSelected: null,
            semesterSelected: null,

            teacherNames: {},
            teacherDivisionDetail : null,

            teachers: null,
            semesters: null,
            teacherDivisionData: this.initializeDivisionData(),
            roomDivisionData: null,

            divisionData: null,
            division_columns: ["subject", "teacher"],
        };
    },
    methods: {
      toggleDetailDivision(row){
        this.teacherDetailModal = true;
        this.getTeacherDetail(row.teacher);
      },
      initializeDivisionData() {
        const subjects = ['TOAN', 'VAN', 'ANH', 'KHTN_HOA', 'KHTN_LY', 'KHTN_SINH', 'KHXH_DIA', 'KHXH_SU', 'KHXH_GDCD', 'TD', 'MT', 'AN', 'TH', 'CN', 'HDTN-HN']
        return Array.from({ length: 15 }, (_, index) => ({
          subject: subjects[index],
          teacher: null,
        }));
      },
       getRoomDivision(){
        const token = localStorage.getItem("access_token");
        this.teacherDivisionData = this.initializeDivisionData()

        axios
          .get(API_URL + `/adminpanel/assignments/?room=${this.roomSelected.name}&semester=${this.semesterSelected}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.teacherDivisionData = this.formatDivisionData(response.data);
          })
          .catch((error) => {
            console.error("Error getting score data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy danh sách phân công lớp thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
      closeDivisionDetailModal(){
        this.semesterSelected = null
        this.teacherDivisionData = null
      },
       formatDivisionData(data) {
          const groupedDivisions = {};

          // Khởi tạo với tất cả các môn để đảm bảo mỗi môn đều có một dòng trong bảng
          this.initializeDivisionData().forEach(subjectEntry => {
            groupedDivisions[subjectEntry.subject] = {
              subject: subjectEntry.subject,
              teacher: null,
            };
          });

          // Cập nhật dữ liệu điểm thực tế từ API
          data.forEach(item => {
            if (groupedDivisions[item.subject]) {
              
              groupedDivisions[item.subject].teacher = item.teacher
            }
          });

          // Chuyển đổi đối tượng groupedScores thành mảng để dễ hiển thị trong bảng
          return Object.values(groupedDivisions);
      },
      toggleDivisionDetail(room){
        this.roomSelected = room
        this.divisionDetailModal = true;
        this.semesterSelected = null
        this.teacherDivisionData = null
      },
      async initializeData() {
        try {
          await this.getApiUrl();
          await this.getDivisionData();
          await this.getRoomData();
          await this.getTeacherData();
          await this.getSemesterData();
        } catch (error) {
          console.error('Error initializing data:', error);
        }
      },
       delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
      },
      getTeacherDetail(teacherId) {
        const token = localStorage.getItem("access_token");

        axios
          .get(API_URL + `/accounts/teachers/?user_id=${teacherId}`, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.teacherDetail = response.data[0];
            console.log(this.teacherDetail)
          })
          .catch((error) => {
            console.error("Error getting teacher data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy chi tiết giáo viên thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
    },
      getTeacherData(){
        const token = localStorage.getItem("access_token");

        axios
          .get(API_URL + "/accounts/teachers/", {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then((response) => {
            this.teachers = response.data;
          })
          .catch((error) => {
            console.error("Error getting teacher data:", error);
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Lấy danh sách giáo viên thất bại",
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
        this.teacherDivisionDetail = teacher
      },
      toggleUpdateDivision(teacher){
        this.divisionUpdateModal = true;
        this.teacherDivisionDetail = teacher
      },
      deleteDivision() {
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
      createDivision(){
        const token = localStorage.getItem("access_token");
        const data = {
          "semester": this.semesterSelected,
          "teacher": this.teacherDivisionDetail.teacher,
          "room": this.roomSelected.name,
          "subject": this.teacherDivisionDetail.subject
        }

        axios
          .post(API_URL + "/adminpanel/assignments/",data, {
            headers: {
              Authorization: `Bearer ${token}`,
              "Content-Type": "application/json",
            },
          })
          .then(() => {
            this.divisionCreateModal = false;
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
              message: "Thêm Phân công giáo viên thất bại",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          });
      },
      closeCreateModal(){
        // this.roomSelected = null
      },
    }
}
</script>

<style scoped>
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem; /* Khoảng cách giữa các card */
}

.card-item {
  flex: 1 1 18%; /* Đảm bảo mỗi card chiếm khoảng 18% chiều rộng */
  max-width: 10rem; /* Đặt chiều rộng tối đa cho mỗi card */
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>