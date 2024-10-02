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
// const API_URL = 'https://classroom50.online';
const API_URL = 'http://127.0.0.1:8000';

import EditProfileForm from "./Profile/EditProfileForm";
import UserCard from "./Profile/UserCard";
export default {
  components: {
    EditProfileForm,
    UserCard,
  },
  data() {
    return {
      userData: null, // Chứa thông tin người dùng
      model: {
        company: "Creative Code Inc.",
        email: "mike@email.com",
        username: "michael23",
        firstName: "Mike",
        lastName: "Andrew",
        address: "Bld Mihail Kogalniceanu, nr. 8 Bl 1, Sc 1, Ap 09",
        city: "Melbourne",
        country: "Australia",
        about:
          "Lamborghini Mercy, Your chick she so thirsty, I'm in that two seat Lambo.",
        user_id: null,
        full_name: null,
        phone_number: null,
        day_of_birth: null,
        sex: null,
        nation: null,
        email: null,
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
        //fetch data to modal
        this.model.user_id = this.userData.user_id
        this.model.full_name = this.userData.full_name
        this.model.phone_number = this.userData.phone_number
        this.model.day_of_birth = this.userData.day_of_birth
        this.model.sex = this.userData.sex
        this.model.nation = this.userData.nation
        this.model.email = this.userData.email

        //fetch data to user
        this.user.fullName = this.userData.full_name
        if(this.userData.is_admin) this.user.title = "ADMIN"
        if(this.userData.is_student) this.user.title = "HỌC SINH"
        if(this.userData.is_parent) this.user.title = "PHỤ HUYNH"
        if(this.userData.is_teacher) this.user.title = "GIÁO VIÊN"


        console.log(this.userData)
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
  }
};
</script>
<style></style>
