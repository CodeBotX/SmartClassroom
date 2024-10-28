import axios from 'axios';
import router from '@/router/index.js';
import Notification from '@/components/NotificationPlugin/Notification.vue';

// const API_URL = "http://bkteaching.one/api";
const API_URL = "https://smartclassroom.click/api";
// const API_URL = "http://127.0.0.1:8000/api";

const instance = axios.create({
    baseURL: API_URL,  // URL của API Django
    headers: {
        'Content-Type': 'application/json',
    }
});
// Làm mới token khi nhận mã lỗi 401
async function refreshAccessToken(refreshToken) {
    try {
        const response = await instance.post('/accounts/api/token/refresh/', {
            "refresh_token": refreshToken
        });
        const newAccessToken = response.data.access;
        localStorage.setItem('access_token', newAccessToken);
        return newAccessToken;
    } catch (error) {
        if (error.response && error.response.status === 401) {
            // Kiểm tra xem người dùng có đang ở trang login không trước khi điều hướng
            if (router.currentRoute.name !== 'login') {
                // Notification({
                //     message: 'Refresh token không còn hiệu lực. Vui lòng đăng nhập lại.',
                //     type: 'danger',
                // });
                // Điều hướng đến trang đăng nhập
                router.push('/login');
            }
        } else {
            return
        }
        throw error;
    }
}

// Interceptor kiểm tra lỗi 401 và làm mới token
instance.interceptors.response.use(
    response => response,
    async error => {
        const originalRequest = error.config;
        
        // Nếu nhận mã lỗi 401 và chưa thử làm mới token
        if (error.response && error.response.status === 401 && !originalRequest._retry) {
            originalRequest._retry = true;
            const refreshToken = localStorage.getItem('refresh_token');
            console.log("Refresh Token: ", refreshToken); // Log refresh token

            if (!refreshToken) {
                console.error("Refresh token không tồn tại.");
                if (router.currentRoute.name !== 'login') {
                    router.push({ name: 'login' });
                    return;
                }else {
                    return;
                }
            }
            if (refreshToken) {
                try {
                    const newAccessToken = await refreshAccessToken(refreshToken);
                    instance.defaults.headers.common['Authorization'] = `Bearer ${newAccessToken}`;
                    originalRequest.headers['Authorization'] = `Bearer ${newAccessToken}`;
                    return instance(originalRequest);
                } catch (refreshError) {
                    // Khi không thể làm mới token, điều hướng đến trang đăng nhập
                    console.log("Token refresh failed", refreshError);
                    router.push({ name: 'login' });
                }
            } else {
                // Nếu không có refresh token, điều hướng ra trang đăng nhập
                router.push({ name: 'login' });
            }
        }
        return Promise.reject(error);
    }
);

export default instance;