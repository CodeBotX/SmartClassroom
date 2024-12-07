<template>
<div>
  <nav
    class="navbar navbar-expand-lg navbar-absolute"
    :class="{ 'bg-white': showMenu, 'navbar-transparent': !showMenu }"
  >
    <div class="container-fluid">
      <div class="navbar-wrapper">
        <div
          class="navbar-toggle d-inline"
          :class="{ toggled: $sidebar.showSidebar }"
        >
          <button
            type="button"
            class="navbar-toggler"
            aria-label="Navbar toggle button"
            @click="toggleSidebar"
          >
            <span class="navbar-toggler-bar bar1"></span>
            <span class="navbar-toggler-bar bar2"></span>
            <span class="navbar-toggler-bar bar3"></span>
          </button>
        </div>
        <a class="navbar-brand" style="color: white" href="#pablo">{{ routeName }}</a>
      </div>
      

      <button
        class="navbar-toggler"
        type="button"
        @click="toggleMenu"
        data-toggle="collapse"
        data-target="#navigation"
        aria-controls="navigation-index"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
        <span class="navbar-toggler-bar navbar-kebab"></span>
      </button>

      <collapse-transition>
        <div class="collapse navbar-collapse show" v-show="showMenu">
          <ul class="navbar-nav" :class="$rtl.isRTL ? 'mr-auto' : 'ml-auto'">
            <!-- <div
              class="search-bar input-group"
              @click="searchModalVisible = true"
            >
              <button
                class="btn btn-link"
                id="search-button"
                data-toggle="modal"
                data-target="#searchModal"
              >
                <i class="tim-icons icon-zoom-split"></i>
              </button> -->
              <base-button @click="studyToggle" type="success" simple class="text-center ml-2" v-if="userData.is_teacher">
               <i class="tim-icons icon-atom"></i> Dạy học
              </base-button>
              
              
              <!-- You can choose types of search input -->
            <base-dropdown
              tag="li"
              :menu-on-right="!$rtl.isRTL"
              title-tag="a"
              class="nav-item"
              menu-classes="dropdown-navbar"
            >
              <a
                slot="title"
                href="#"
                class="dropdown-toggle nav-link"
                data-toggle="dropdown"
                aria-expanded="true"
              >
                <div class="photo mr-3">
                  <img src="img/anime3.png" />
                </div>
                <span v-if="userData" :userData="userData" class="mr-5">{{ userData.full_name }}</span>
                <span class="caret d-none d-lg-block d-xl-block"> </span>
                <p v-if="userData" :userData="userData" class="d-lg-none">{{ userData.full_name }}</p>
              </a>
              <li class="nav-link">
                
                <router-link :to="{ path: 'profile'}">
                  <a href="#" class="nav-item dropdown-item">Thông tin tài khoản</a>
                </router-link>
              </li>
              <div class="dropdown-divider"></div>
              <li class="nav-link">
                <a @click="logout" href="#" class="nav-item dropdown-item">Đăng xuất</a>
              </li>
            </base-dropdown>
          </ul>
        </div>
      </collapse-transition>
    </div>
  </nav>
  <Loading :loading="isLoading" />
  </div>
</template>
<script>
import { CollapseTransition } from "vue2-transitions";
import Modal from "@/components/Modal";
import axios from '../../services/axios'; 
import Loading from '../loading/Loading.vue';

import BaseButton from '../../components/BaseButton.vue';
 
let API_URL = ""

const classPeriods = [
  { period: 1, start: { hour: 7, minute: 0 }, end: { hour: 7, minute: 59 } },   // Tiết 1
  { period: 2, start: { hour: 8, minute: 0 }, end: { hour: 8, minute: 59 } },   // Tiết 2
  { period: 3, start: { hour: 9, minute: 0 }, end: { hour: 9, minute: 59 } },  // Tiết 3
  { period: 4, start: { hour: 10, minute: 0 }, end: { hour: 10, minute: 59 } },  // Tiết 4
  { period: 5, start: { hour: 11, minute: 0 }, end: { hour: 11, minute: 59 } },  // Tiết 5
  { period: 6, start: { hour: 12, minute: 0 }, end: { hour: 23, minute: 59 } },  // Tiết 6
];

export default {
  props: {
    userData: {
      type: Object,
      required: true,
      default: "User",
    }
  },
  components: {
    CollapseTransition,
    Modal,
    BaseButton,
    Loading
  },
  computed: {
    getApiUrl() {
      API_URL =  this.$t("dashboard.apiURL");
    },
    routeName() {
      const name = this.$route.matched[1].name;
      return name || "";
    },
    isRTL() {
      return this.$rtl.isRTL;
    },
  },
  data() {
    return {
      activeNotifications: false,
      showMenu: false,
      searchModalVisible: false,
      searchQuery: "",
      isLoading: false,
    };
  },
  methods: {
    getCurrentPeriod() {
      const currentTimeInMinutes = currentHour * 60 + currentMinutes;
      
      for (const period of classPeriods) {
        const startTimeInMinutes = period.start.hour * 60 + period.start.minute;
        const endTimeInMinutes = period.end.hour * 60 + period.end.minute;

        if (currentTimeInMinutes >= startTimeInMinutes && currentTimeInMinutes <= endTimeInMinutes) {
          return period.period; // Trả về số tiết hiện tại
        }
      }

      return null; // Không có tiết học nào hiện tại
    },
    capitalizeFirstLetter(string) {
      return string.charAt(0).toUpperCase() + string.slice(1);
    },
    toggleNotificationDropDown() {
      this.activeNotifications = !this.activeNotifications;
    },
    closeDropDown() {
      this.activeNotifications = false;
    },
    toggleSidebar() {
      this.$sidebar.displaySidebar(!this.$sidebar.showSidebar);
    },
    hideSidebar() {
      this.$sidebar.displaySidebar(false);
    },
    toggleMenu() {
      this.showMenu = !this.showMenu;
    },
    logout() {
      localStorage.removeItem('access_token');  // Xóa token khỏi localStorage
      // localStorage.removeItem('refresh_token');
      localStorage.removeItem('user_data');
      this.$notify({
          type: 'warning',
          icon: 'tim-icons icon-bell-55',
          message: "Bạn đã đăng xuất",
          timeout: 3000,
          verticalAlign: 'top',
          horizontalAlign: 'center',
        });
      this.$router.push('/login');  // Điều hướng về trang đăng nhập
      
    },
    getCurrentFormattedDate(date) {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0'); // Tháng bắt đầu từ 0, nên cần +1
      const day = String(date.getDate()).padStart(2, '0');        // Đảm bảo luôn có 2 chữ số

      return `${year}-${month}-${day}`;
    },
    async studyToggle(){
      if(!this.userData.is_teacher){
        this.$notify({
          type: 'warning',
          icon: 'tim-icons icon-bell-55',
          message: "Bạn không có quyền vào mục này.",
          timeout: 1000,
          verticalAlign: 'top',
          horizontalAlign: 'center',
        });
        return
      }
      //Kiểm tra giáo viên có tiết học nào hiện tại không
      const currentDate = new Date();
      const currentHour = currentDate.getHours();
      const currentMinutes = currentDate.getMinutes();

      let currentPeriod = null
      const currentTimeInMinutes = currentHour * 60 + currentMinutes;
      
      for (const period of classPeriods) {
        const startTimeInMinutes = period.start.hour * 60 + period.start.minute;
        const endTimeInMinutes = period.end.hour * 60 + period.end.minute;

        if (currentTimeInMinutes >= startTimeInMinutes && currentTimeInMinutes <= endTimeInMinutes) {
          currentPeriod = period.period; // Trả về số tiết hiện tại
        }
      }
      // nếu ko thì currentPeriod = null, tức là ko có tiết học nào hiện tại
      if (currentPeriod === null) {
        this.$notify({
          type: 'warning',
          icon: 'tim-icons icon-bell-55',
          message: "Hiện tại không có tiết học nào.",
          timeout: 1000,
          verticalAlign: 'top',
          horizontalAlign: 'center',
        });
        return;
      }

      // this.$notify({
      //     type: 'success',
      //     icon: 'tim-icons icon-bell-55',
      //     message: "Bắt đầu dạy học",
      //     timeout: 1000,
      //     verticalAlign: 'top',
      //     horizontalAlign: 'center',
      //   });
      // this.$router.push('/study');  // Điều hướng về trang dạy học

      // Call API để kiểm tra giáo viên có tiết học không
      this.isLoading = true;
      try {
        const response = await axios.get(API_URL + `/adminpanel/lessons/?teacher=${this.userData.user_id}&day=${this.getCurrentFormattedDate(currentDate)}&period=${currentPeriod}`, {
          
        })
        
          if (response.data.length !== 0) {
            localStorage.setItem('lesson_data', JSON.stringify(response.data[0]));
            this.$notify({
              type: 'success',
              icon: 'tim-icons icon-bell-55',
              message: "Bắt đầu dạy học lớp "+response.data[0].room,
              timeout: 1000,
              verticalAlign: 'top',
              horizontalAlign: 'center',
            });
            this.$router.push('/study');
        } else {
          this.$notify({
            type: 'warning',
            icon: 'tim-icons icon-bell-55',
            message: "Hiện tại bạn không có tiết học.",
            timeout: 1000,
            verticalAlign: 'top',
            horizontalAlign: 'center',
          });
        }
      }
      catch(error) {
        this.$notify({
          type: 'danger',
          icon: 'tim-icons icon-bell-55',
          message: "Lỗi khi kiểm tra tiết học: " + error.message,
          timeout: 1000,
          verticalAlign: 'top',
          horizontalAlign: 'center',
        });
      }
      finally {
        this.isLoading = false;  // Kết thúc loading
      }
    },
  },
};
</script>
<style>
/* .centered-button {
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  top: 50%;
  transform: translate(-50%, -50%);
} */
 .btn-demo {
  padding: 10px 20px;
}

.search-bar .btn-demo {
  margin-left: 10px; /* Khoảng cách giữa icon tìm kiếm và nút Dạy học */
}
</style>
