<template>
  <div class="wrapper">
    <side-bar>
      <template slot="links" >
        <sidebar-link v-if="userData && userData.is_admin" 
          to="/administration"
          :name="$t('sidebar.administration')"
          icon="tim-icons icon-bank"
        />
        <sidebar-link  v-if="userData && userData.is_admin"
          to="/education_program"
          :name="$t('sidebar.educationProgram')"
          icon="tim-icons icon-book-bookmark"
        />
        <sidebar-link v-if="userData && userData.is_teacher"
          to="/learning_management"
          :name="$t('sidebar.learningManagement')"
          icon="tim-icons icon-pencil"
        />
        <sidebar-link v-if="userData && userData.is_teacher"
          to="/homeroom_teacher"
          :name="$t('sidebar.homeroomTeacher')"
          icon="tim-icons icon-components"
        />
        <sidebar-link v-if="userData && (userData.is_student || userData.is_parent)"
          to="/learning_outcome"
          :name="$t('sidebar.learningOutcome')"
          icon="tim-icons icon-paper"
        />
         <!-- <sidebar-link 
          to="/competition_result"
          :name="$t('sidebar.competitionResult')"
          icon="tim-icons icon-chart-bar-32"
        /> -->
        <!--
        <sidebar-link
          to="/dashboard"
          :name="$t('sidebar.dashboard')"
          icon="tim-icons icon-chart-pie-36"
        />
        <sidebar-link
          to="/icons"
          :name="$t('sidebar.icons')"
          icon="tim-icons icon-atom"
        />
        <sidebar-link
          to="/maps"
          :name="$t('sidebar.maps')"
          icon="tim-icons icon-pin"
        />
        <sidebar-link
          to="/notifications"
          :name="$t('sidebar.notifications')"
          icon="tim-icons icon-bell-55"
        /> -->
        <!-- <sidebar-link
          to="/profile"
          :name="$t('sidebar.userProfile')"
          icon="tim-icons icon-single-02"
        />
        <sidebar-link
          to="/table-list"
          :name="$t('sidebar.tableList')"
          icon="tim-icons icon-puzzle-10"
        />
        <sidebar-link
          to="/typography"
          :name="$t('sidebar.typography')"
          icon="tim-icons icon-align-center"
        />
        <sidebar-link
          to="/dashboard?enableRTL=true"
          :name="$t('sidebar.rtlSupport')"
          icon="tim-icons icon-world"
        /> -->
      </template>
    </side-bar>
    <div class="main-panel">
      <top-navbar v-if="userData" :userData="userData"></top-navbar>

      <dashboard-content @click.native="toggleSidebar"> </dashboard-content>

      <content-footer></content-footer>
    </div>
  </div>
</template>
<style lang="scss"></style>
<script>
import axios from '../../services/axios'; 

let API_URL = ""


import TopNavbar from "./TopNavbar.vue";
import ContentFooter from "./ContentFooter.vue";
import DashboardContent from "./Content.vue";
// import MobileMenu from "./MobileMenu";
export default {
  data() {
    return {
      userData: null,
    }
  },
  computed: {
    getApiUrl() {
      API_URL =  this.$t("dashboard.apiURL");
    },
  },
  components: {
    TopNavbar,
    ContentFooter,
    DashboardContent,
  },
  methods: {
  toggleSidebar() {
    if (this.$sidebar.showSidebar) {
      this.$sidebar.displaySidebar(false);
    }
  },
  getUserData() {
    let savedUserData = localStorage.getItem('user_data');
    if (savedUserData) {
      // Nếu đã có dữ liệu trong localStorage, sử dụng dữ liệu đó
      this.userData = JSON.parse(savedUserData);
      return;
    }

    // Nếu chưa có dữ liệu, gọi API để lấy thông tin
    const token = localStorage.getItem('access_token');
    axios.post(API_URL + '/accounts/detail/', {}, {
      headers: {
        'Authorization': `Bearer ${token}` // Đính kèm token vào headers
      }
    })
    .then((response) => {
      this.userData = response.data;
      // Lưu dữ liệu userData vào localStorage
      localStorage.setItem('user_data', JSON.stringify(this.userData));
      console.log(this.userData);
    })
    .catch(error => {
      console.error("Error fetching user data:", error);
      this.$notify({
        type: 'danger',
        message: "Lấy thông tin tài khoản thất bại. Vui lòng đăng nhập lại",
        timeout: 3000,
        verticalAlign: 'top',
        horizontalAlign: 'center',
      });
      this.$router.push('/login');
    });
  },
},
  mounted() {
    this.getUserData(); // Gọi API khi trang tải
  },
};
</script>