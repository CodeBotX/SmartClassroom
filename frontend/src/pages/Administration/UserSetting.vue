<template>
  <div class="row">
    <div class="col-12">
      <card>
        <template slot="header">
          <h3>Quản trị người dùng</h3>
          <div class="col-sm-12">
            <div
              class="btn-group btn-group-toggle float-right"
              data-toggle="buttons"
            >
              <label
                v-for="(option, index) in userSettingOption"
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
        </template>

        <!-- HỌC SINH -->
        <div v-if="bigLineChart.activeIndex === 0">
          <base-table :data="studentData" :columns="student_columns" id="student_table">
            <template slot="columns">
              <th>ID</th>
              <th>Họ và tên</th>
              <th>Giới tính</th>
              <th>Ngày sinh</th>
              <th>Trạng thái</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.user }}</td>
              <td>{{ row.full_name }}</td>
              <td>{{ row.sex }}</td>
              <td>{{ row.day_of_birth }}</td>
              <td>{{ row.active_status }}</td>
              <td class="td-actions text-right">
                <base-button type="info" size="sm" icon @click="toggleDetail(row.user)">
                  <i class="tim-icons icon-single-02"></i>
                </base-button>
                <base-button type="success" size="sm" icon @click="toggleUpdate(row.user)">
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon @click="toggleRemove(row.user)">
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td>
            </template>
          </base-table>
          <b-pagination
            v-model="currentPage"
            :total-rows="studentDataLength"
            :per-page="perPage"
            aria-controls="my-student_table"
          ></b-pagination>
        </div>
        
        <!-- GIÁO VIÊN -->
        <div v-if="bigLineChart.activeIndex === 1">
          <base-table :data="teacherData" :columns="teacher_columns">
            <template slot="columns">
              <th>ID</th>
              <th>Họ và tên</th>
              <th>Giới tính</th>
              <th>Ngày sinh</th>
              <th>Môn dạy</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.user }}</td>
              <td>{{ row.full_name }}</td>
              <td>{{ row.sex }}</td>
              <td>{{ row.day_of_birth }}</td>
              <td>{{ row.subjects }}</td>
              <td class="td-actions text-right">
                <base-button type="info" size="sm" icon @click="toggleDetail(row.user)">
                  <i class="tim-icons icon-single-02"></i>
                </base-button>
                <base-button type="success" size="sm" icon @click="toggleUpdate(row.user)">
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon @click="toggleRemove(row.user)">
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td>
            </template>
          </base-table>
        </div>

        <!-- PHỤ HUYNH -->
        <div v-if="bigLineChart.activeIndex === 2">
          <base-table :data="parentData" :columns="parent_columns">
            <template slot="columns">
              <th>ID</th>
              <th>Họ và tên</th>
              <th>Địa chỉ</th>
              <th class="text-right">Actions</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.user }}</td>
              <td>{{ row.full_name }}</td>
              <td>{{ row.address }}</td>
              <td class="td-actions text-right">
                <base-button type="info" size="sm" icon @click="toggleDetail(row.user)">
                  <i class="tim-icons icon-single-02"></i>
                </base-button>
                <base-button type="success" size="sm" icon @click="toggleUpdate(row.user)">
                  <i class="tim-icons icon-settings"></i>
                </base-button>
                <base-button type="danger" size="sm" icon @click="toggleRemove(row.user)">
                  <i class="tim-icons icon-simple-remove"></i>
                </base-button>
              </td>
            </template>
          </base-table>
        </div>

        <!-- ADMIN -->
        <div v-if="bigLineChart.activeIndex === 3">
          <base-table :data="adminData" :columns="admin_columns">
            <template slot="columns">
              <th>ID</th>
              <th>Họ và tên</th>
              <th>Giới tính</th>
              <th>Ngày sinh</th>
              <th>Chức vụ</th>
            </template>
            <template slot-scope="{ row }">
              <td>{{ row.user }}</td>
              <td>{{ row.full_name }}</td>
              <td>{{ row.sex }}</td>
              <td>{{ row.day_of_birth }}</td>
              <td>{{ row.description }}</td>
            </template>
          </base-table>
        </div>

        <!-- Detail Modal -->
        <modal :show.sync="modals.detailModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
               <!-- Học sinh -->
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thông tin học sinh</h4>
                    </div>
                </template>
                <template v-if="modals.studentDetail">
                    <fieldset disabled>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="modals.studentDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="modals.studentDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Lớp" v-model="modals.studentDetail.room"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Giới tính" v-model="modals.studentDetail.sex"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày sinh" v-model="modals.studentDetail.day_of_birth"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Trạng thái" v-model="modals.studentDetail.active_status"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Phụ huynh" v-model="modals.studentDetail.parent"></base-input>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>  
                </template>
            </card>

            <!-- Giáo viên -->

            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 1">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thông tin giáo viên</h4>
                    </div>
                </template>
                <template v-if="modals.teacherDetail">
                    <fieldset disabled>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="modals.teacherDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="modals.teacherDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Môn dạy" v-model="modals.teacherDetail.subjects"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Giới tính" v-model="modals.teacherDetail.sex"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày sinh" v-model="modals.teacherDetail.day_of_birth"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Dân tộc" v-model="modals.teacherDetail.nation"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Học vấn" v-model="modals.teacherDetail.expertise_levels"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Chức vụ" v-model="modals.teacherDetail.contract_types"></base-input>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>  
                </template>
            </card>

            <!-- Phụ huynh -->

            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 2">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Thông tin phụ huynh</h4>
                    </div>
                </template>
                <template v-if="modals.parentDetail">
                    <fieldset disabled>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="modals.parentDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="modals.parentDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Địa chỉ" v-model="modals.parentDetail.address"></base-input>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </fieldset>  
                </template>
            </card>
        </modal>

        <!-- Update Modal -->
        <modal :show.sync="modals.updateModal"
               body-classes="p-0"
               modal-classes="modal-dialog-centered modal-sm">
            <!-- Học sinh -->
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 0">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Cập nhật học sinh</h4>
                    </div>
                </template>
                <template v-if="modals.studentDetail">
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="modals.studentDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="modals.studentDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Lớp" v-model="modals.studentDetail.room"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Giới tính" v-model="modals.studentDetail.sex"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày sinh" v-model="modals.studentDetail.day_of_birth"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Trạng thái" v-model="modals.studentDetail.active_status"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Phụ huynh" v-model="modals.studentDetail.parent"></base-input>
                                    </div>
                                </div>
                                <base-button @click="updateObject" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                </template>
            </card>

            <!-- Giáo viên -->
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 1">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Cập nhật giáo viên</h4>
                    </div>
                </template>
                <template v-if="modals.teacherDetail">
                    <fieldset>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="modals.teacherDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="modals.teacherDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Môn dạy" v-model="modals.teacherDetail.subjects"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Giới tính" v-model="modals.teacherDetail.sex"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Ngày sinh" v-model="modals.teacherDetail.day_of_birth"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Dân tộc" v-model="modals.teacherDetail.nation"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="Học vấn" v-model="modals.teacherDetail.expertise_levels"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Chức vụ" v-model="modals.teacherDetail.contract_types"></base-input>
                                    </div>
                                </div>
                                <base-button @click="updateObject" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                    </fieldset>  
                </template>
            </card>

            <!-- Phụ huynh -->
            <card type="secondary"
                  header-classes="bg-white pb-5"
                  body-classes="px-lg-5 py-lg-5"
                  class="border-0 mb-0" v-if="this.bigLineChart.activeIndex === 2">
                <template>
                    <div class="text-muted text-center mb-3">
                        <h4 class="text-success">Cập nhật phụ huynh</h4>
                    </div>
                </template>
                <template v-if="modals.parentDetail">
                    <fieldset>
                        <div class="row">
                            <div class="col-12">
                                <div class="row">
                                    <div class="col-md-6 pr-md-1">
                                        <base-input label="ID" v-model="modals.parentDetail.user"></base-input>
                                    </div>
                                    <div class="col-md-6 pl-md-1">
                                        <base-input label="Họ và tên" v-model="modals.parentDetail.full_name"></base-input>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-md-12 pr-md-1">
                                        <base-input label="Địa chỉ" v-model="modals.parentDetail.address"></base-input>
                                    </div>
                                </div>
                                <base-button @click="updateObject" type="secondary" fill>Xác nhận</base-button>
                            </div>
                        </div>
                    </fieldset>  
                </template>
            </card>
        </modal>

        <!-- Remove Modal -->
        <modal :show.sync="modals.removeModal">
            <h4 slot="header" class="modal-title" id="modal-title-default" v-if="this.bigLineChart.activeIndex === 0">Xác nhận xóa học sinh này</h4>
            <h4 slot="header" class="modal-title" id="modal-title-default" v-if="this.bigLineChart.activeIndex === 1">Xác nhận xóa giáo viên này</h4>
            <h4 slot="header" class="modal-title" id="modal-title-default" v-if="this.bigLineChart.activeIndex === 2">Xác nhận xóa phụ huynh này</h4>
            <template slot="footer">
                <base-button type="secondary" @click="removeObject">Xác nhận</base-button>
                <base-button type="danger" class="ml-auto" @click="modals.removeModal = false">Hủy
                </base-button>
            </template>
        </modal>


      </card>
    </div>
  </div>
</template>

<script>
import axios from "../../services/axios";

let API_URL = ""

import config from "@/config";
import Card from "../../components/Cards/Card.vue";
import BaseTable from '../../components/BaseTable.vue';
import Modal from '../../components/Modal.vue';
import BaseInput from '../../components/Inputs/BaseInput.vue';


export default {
  components: { Card, BaseTable, Modal, BaseInput },
  computed: {
    getApiUrl() {
      API_URL =  this.$t("dashboard.apiURL");
    },
  },
  data() {
    return {
    perPage: 3,
    currentPage: 1,
    modals: {
        detailModal: false,
        updateModal: false,
        removeModal: false,
        idRemove: null,

        teacherModal: false,
        parentModal: false,
        studentDetail: null,
        teacherDetail: null,
        parentDetail: null,
    },
    student_columns: ["user", "full_name", "sex", "day_of_birth", "active_status", "actions"],
    teacher_columns: ["user", "full_name", "sex", "day_of_birth", "subjects", "actions"],
    parent_columns: ["user", "full_name", "address"],
    admin_columns: ["user", "full_name", "sex", "day_of_birth", "description"],
      studentData: null,
      teacherData: null,
      parentData: null,
      adminData: null,
      bigLineChart: {
        allData: [
          [100, 70, 90, 70, 85, 60, 75, 60, 90, 80, 110, 100],
          [80, 120, 105, 110, 95, 105, 90, 100, 80, 95, 70, 120],
          [60, 80, 65, 130, 80, 105, 90, 130, 70, 115, 60, 130],
        ],
        activeIndex: null,
        index: "Quản trị",
        chartData: {
          datasets: [{}],
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
        },

        gradientColors: config.colors.primaryGradient,
        gradientStops: [1, 0.4, 0],
        categories: [],
      },
    };
  },
  computed: {
    userSettingOption() {
      return this.$t("dashboard.userSetting");
    },
  },
  methods: {
    studentDataLength() {
      return this.studentData.length
    },
    removeObject(){
        const token = localStorage.getItem("access_token");
        let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
        if (this.bigLineChart.activeIndex === 0) {
          apiUrl = API_URL + "/accounts/students/" + this.modals.idRemove + "/";
        } else if (this.bigLineChart.activeIndex === 1) {
          apiUrl = API_URL + "/accounts/teachers/" + this.modals.idRemove + "/";
        } else if (this.bigLineChart.activeIndex === 2) {
          apiUrl = API_URL + "/accounts/parents/" + this.modals.idRemove + "/";
        }

        axios
        .delete(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          let message = "";

          if (this.bigLineChart.activeIndex === 0) {
            message = "Xóa học sinh thành công"
          } else if (this.bigLineChart.activeIndex === 1) {
            message = "Xóa giáo viên thành công"
          } else if (this.bigLineChart.activeIndex === 2) {
            message = "Xóa phụ huynh thành công"
          }
            this.$notify({
                type: "success",
                icon: 'tim-icons icon-check-2',
                message: message,
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
          this.modals.removeModal = false
          this.initBigChart(this.bigLineChart.activeIndex)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    updateObject(){

        let dataUser = null;

        let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
        if (this.bigLineChart.activeIndex === 0) {
          apiUrl = API_URL + "/accounts/students/" + this.modals.studentDetail.user + "/";
          dataUser = this.modals.studentDetail
        } else if (this.bigLineChart.activeIndex === 1) {
          apiUrl = API_URL + "/accounts/teachers/" + this.modals.teacherDetail.user + "/";
          dataUser = this.modals.teacherDetail
        } else if (this.bigLineChart.activeIndex === 2) {
          apiUrl = API_URL + "/accounts/parents/" + this.modals.parentDetail.user + "/";
          dataUser = this.modals.parentDetail
        }

        const token = localStorage.getItem("access_token");
        axios
        .patch(apiUrl, dataUser, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          let message = "";

          this.modals.studentDetail = response.data
          if (this.bigLineChart.activeIndex === 0) {
          this.modals.studentDetail = response.data
          message = "Cập nhật thông tin học sinh thành công"
        } else if (this.bigLineChart.activeIndex === 1) {
          this.modals.teacherDetail = response.data
           message = "Cập nhật thông tin giáo viên thành công"
        } else if (this.bigLineChart.activeIndex === 2) {
          this.modals.parentDetail = response.data
           message = "Cập nhật thông tin phụ huynh thành công"
        }
        this.$notify({
                type: "success",
                icon: 'tim-icons icon-check-2',
                message: message,
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
          this.modals.updateModal = false
          this.initBigChart(this.bigLineChart.activeIndex)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Dữ liệu không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleDetail(index){
        this.modals.detailModal = true;

        let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
        if (this.bigLineChart.activeIndex === 0) {
          apiUrl = API_URL + "/accounts/students/" + index + "/";
        } else if (this.bigLineChart.activeIndex === 1) {
          apiUrl = API_URL + "/accounts/teachers/" + index + "/";
        } else if (this.bigLineChart.activeIndex === 2) {
          apiUrl = API_URL + "/accounts/parents/" + index + "/";
        }



        const token = localStorage.getItem("access_token");
        axios
        .get(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {

          if (this.bigLineChart.activeIndex === 0) {
            this.modals.studentDetail = response.data
          } else if (this.bigLineChart.activeIndex === 1) {
            this.modals.teacherDetail = response.data
          } else if (this.bigLineChart.activeIndex === 2) {
            this.modals.parentDetail = response.data
          }

          console.log(response.data)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleUpdate(index){
        this.modals.updateModal = true;

        let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
        if (this.bigLineChart.activeIndex === 0) {
          apiUrl = API_URL + "/accounts/students/" + index + "/";
        } else if (this.bigLineChart.activeIndex === 1) {
          apiUrl = API_URL + "/accounts/teachers/" + index + "/";
        } else if (this.bigLineChart.activeIndex === 2) {
          apiUrl = API_URL + "/accounts/parents/" + index + "/";
        }

        const token = localStorage.getItem("access_token");
        axios
        .get(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
           if (this.bigLineChart.activeIndex === 0) {
            this.modals.studentDetail = response.data
          } else if (this.bigLineChart.activeIndex === 1) {
            this.modals.teacherDetail = response.data
          } else if (this.bigLineChart.activeIndex === 2) {
            this.modals.parentDetail = response.data
          }

          console.log(response.data)
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Dữ liệu không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    toggleRemove(index){
        this.modals.removeModal = true;
        this.modals.idRemove = index;
    },
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
            data: this.bigLineChart.allData[index],
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
    
      let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
      if (this.bigLineChart.activeIndex === 0) {
        apiUrl = API_URL + "/accounts/students/";
      } else if (this.bigLineChart.activeIndex === 1) {
        apiUrl = API_URL + "/accounts/teachers/";
      } else if (this.bigLineChart.activeIndex === 2) {
        apiUrl = API_URL + "/accounts/parents/";
      } else if (this.bigLineChart.activeIndex === 3) {
        apiUrl = API_URL + "/accounts/admins/";
      }

      //Get data
      const token = localStorage.getItem("access_token");
      axios
        .get(apiUrl, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          if(this.bigLineChart.activeIndex === 0) this.studentData = response.data
          else if(this.bigLineChart.activeIndex === 1) this.teacherData = response.data
          else if(this.bigLineChart.activeIndex === 2) this.parentData = response.data
          else if(this.bigLineChart.activeIndex === 3) this.adminData = response.data
          
        })
        .catch((error) => {
          console.error("Error get user data :", error);

          this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
        });
    },
    resetPassword() {
      const token = localStorage.getItem("access_token");
      const resetPasswordData = {
        user_id: this.id_user_reset,
      };

      axios
        .post(API_URL + "/accounts/admin-reset-password/", resetPasswordData, {
          headers: {
            Authorization: `Bearer ${token}`, // Đính kèm token vào headers
            "Content-Type": "application/json",
          },
        })
        .then((response) => {
          this.$notify({
            type: "success",
            icon: 'tim-icons icon-check-2',
            message: response.data.detail,
            timeout: 3000,
            verticalAlign: "top",
            horizontalAlign: "right",
          });
          this.isEditingResetPassword = false; // Tắt chế độ chỉnh sửa

          this.user_id_reset = null;
        })
        .catch((error) => {

          if (error.response && error.response.data) {
            if (error.response.status === 401) {
              this.$notify({
                type: "success",
                icon: 'tim-icons icon-alert-circle-exc',
                message: "Bạn không có quyền thực hiện thao tác này.",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
            }
            if (error.response.status === 404) {
              this.$notify({
                type: "warning",
                icon: 'tim-icons icon-bell-55',
                message: "Người dụng không tồn tại. Vui lòng thử lại",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
            }
          } else {
            this.$notify({
              type: "danger",
              icon: 'tim-icons icon-bell-55',
              message: "Reset mật khẩu không thành công. Vui lòng thử lại sau.",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          }
        });
    },
    triggerFileUpload() {
      this.$refs.fileInput.click(); // Trigger file input click event
    },
    handleFileUpload(event) {
      this.selectedFile = event.target.files[0]; // Get selected file
    },
    registerAccounts() {
      if (!this.selectedFile) {
        this.$notify({
          type: "warning",
          icon: 'tim-icons icon-bell-55',
          message: "Vui lòng tải lên tệp Excel",
          timeout: 3000,
          verticalAlign: "top",
          horizontalAlign: "center",
        });
        return;
      }

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      let apiUrl = ""; // API URL sẽ thay đổi dựa trên loại đăng ký
      if (this.registrationType === "student") {
        apiUrl = API_URL + "/accounts/register-student/";
      } else if (this.registrationType === "teacher") {
        apiUrl = API_URL + "/accounts/register-teacher/";
      } else if (this.registrationType === "parent") {
        apiUrl = API_URL + "/accounts/register-parent/";
      }

      const token = localStorage.getItem("access_token");

      axios
        .post(apiUrl, formData, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          this.$notify({
            type: "success",
            icon: 'tim-icons icon-check-2',
            message: response.data.detail,
            timeout: 3000,
            verticalAlign: "top",
            horizontalAlign: "right",
          });
        })
        .catch((error) => {
          console.error("Error registering accounts:", error);
          if (error.response) {
            if (error.response && error.response.data) {
              // Kiểm tra lỗi validate_file từ backend
              if (error.response.data.file) {
                const errorMessage = error.response.data.file[0]; // Lấy thông báo lỗi từ trường file
                this.$notify({
                  type: "danger",
                  icon: 'tim-icons icon-bell-55',
                  message: errorMessage,
                  timeout: 3000,
                  verticalAlign: "top",
                  horizontalAlign: "right",
                });
              } else {
                const errorMessage =
                  "Vui lòng kiểm tra lại cấu trúc file và loại đối tượng đăng ký ";
                this.$notify({
                  type: "danger",
                  icon: 'tim-icons icon-bell-55',
                  message: errorMessage,
                  timeout: 3000,
                  verticalAlign: "top",
                  horizontalAlign: "right",
                });
              }
            } else {
              // Thông báo lỗi nếu không nhận được phản hồi cụ thể từ backend
              this.$notify({
                type: "danger",
                icon: 'tim-icons icon-alert-circle-exc',
                message: "Lỗi không xác định. Vui lòng thử lại.",
                timeout: 3000,
                verticalAlign: "top",
                horizontalAlign: "right",
              });
            }
          } else {
            this.$notify({
              type: "warning",
              icon: 'tim-icons icon-bell-55',
              message: "Có lỗi xảy ra. Vui lòng thử lại sau",
              timeout: 3000,
              verticalAlign: "top",
              horizontalAlign: "right",
            });
          }
        });
    },
  },
};
</script>

<style>
</style>