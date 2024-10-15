<template>
  <div class="row">
    <div class="col-md-8">
      <edit-profile-form :model="model"> </edit-profile-form>
    </div>
    <div class="col-md-4">
      <user-card :user="user"></user-card>
    </div>
  </div>
</template>
<script>
import axios from '../services/axios'; 
let API_URL = ""

import EditProfileForm from "./Profile/EditProfileForm";
import UserCard from "./Profile/UserCard";
export default {
  components: {
    EditProfileForm,
    UserCard,
  },
  computed: {
    getApiUrl() {
      API_URL =  this.$t("dashboard.apiURL");
    },
  },
  data() {
    return {
      userData: null, // Chứa thông tin người dùng
      modal_test: null,
      model: {
        user_id: null,
        full_name: null,
        phone_number: null,
        day_of_birth: null,
        sex: null,
        nation: null,
        email: null,
        role: null,
        contract_types: null,
        expertise_levels: null,
        subjects: null,
        old_email: null,
        old_phone_number: null,
      },
      user: {
        fullName: "Mike Andrew",
        title: "Ceo/Co-Founder",
        description: `Do not be scared of the truth because we need to restart the human foundation in truth And I love you like Kanye loves Kanye I love Rick Owens’ bed design but the back is...`,
      },
      
    };
  },
  mounted() {
    this.getUserData(); // Gọi API khi trang tải
  },
  methods: {
    getUserData() {
      const token = localStorage.getItem('access_token');
      axios.post(API_URL+'/accounts/detail/', {}, {
        headers: {
          'Authorization': `Bearer ${token}`  // Đính kèm token vào headers
        }
      })
      .then((response) => {
         // Lưu dữ liệu người dùng vào userData
        // this.userData.full_name = response.data.user.full_name;
        // this.userData.sex = response.data.user.sex;
        // this.userData.nation = response.data.user.nation;
        // this.userData.email = response.data.user.email;
        // this.userData.day_of_birth = response.data.user.day_of_birth;
        this.userData = response.data
        this.model_test = response.data

        //fetch data to modal
        this.model.user_id = this.userData.user_id
        this.model.full_name = this.userData.full_name
        this.model.phone_number = this.userData.phone_number
        this.model.old_phone_number = this.userData.phone_number
        this.model.day_of_birth = this.userData.day_of_birth
        this.model.sex = this.userData.sex
        this.model.nation = this.userData.nation
        this.model.email = this.userData.email
        this.model.old_email = this.userData.email
        this.model.contract_types = this.userData.contract_types
        this.model.subjects = this.userData.subjects
        this.model.expertise_levels = this.userData.expertise_levels


        //fetch data to user
        this.user.fullName = this.userData.full_name
        if(this.userData.is_admin) {
          this.user.title = "ADMIN"
          this.model.role = "admins"
        }
        if(this.userData.is_student){
          this.user.title = "HỌC SINH"
          this.model.role = "students"
        }
        if(this.userData.is_parent){
          this.user.title = "PHỤ HUYNH"
          this.model.role = "parents"
        }
        if(this.userData.is_teacher){
          this.user.title = "GIÁO VIÊN"
          this.model.role = "teachers"
        }


        console.log(this.userData)
      })
      .catch(error => {
        console.error("Error fetching user data:", error);
        this.$notify({
          type: 'danger',
          icon: 'tim-icons icon-alert-circle-exc',
          message: "Lấy thông tin tài khoản thất bại. Vui lòng đăng nhập lại",
          timeout: 3000,
          verticalAlign: 'top',
          horizontalAlign: 'center',
        });
        this.$router.push('/login');
      });
    },
  }
};
</script>
<style></style>
