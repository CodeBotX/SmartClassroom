<template>
  <div v-if="loading" class="loading-overlay">
    <div class="spinner-container">
      <div class="spinner"></div>
      <a href="#" class="loading-icon" aria-hidden="true">
        <img src="@/assets/img/SMALL_CL4.png" alt="Loading Icon" class="loading-icon-img" /> <!-- Thêm icon bằng thẻ img -->
      </a>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    loading: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style scoped>
.loading-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
  display: flex;
  flex-direction: column; 
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.spinner-container {
  position: relative; /* Để spinner và icon có thể chồng lên nhau */
}

.spinner {
  border: 5px solid rgba(255, 255, 255, 0.3);
  border-top: 8px solid #0d9fe8;
  border-radius: 50%;
  width: 100px; /* Đặt kích thước cho spinner */
  height: 100px; /* Đặt kích thước cho spinner */
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.loading-icon {
  position: absolute; /* Đặt icon ở vị trí tuyệt đối bên trong spinner-container */
  top: 50%; /* Giữa theo chiều dọc */
  left: 50%; /* Giữa theo chiều ngang */
  transform: translate(-50%, -50%); /* Giúp icon căn giữa chính xác */
  text-decoration: none; /* Xóa gạch chân dưới thẻ a */
}

.loading-icon-img {
  transform: scale(1.5);
}

p {
  color: white;
  margin-top: 10px;
  font-size: 18px;
}
</style>
