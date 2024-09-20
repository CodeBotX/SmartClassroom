import { createRouter, createWebHistory } from "vue-router";
 
import dashboard from '../pages/master/dashboard'

import home from '../pages/home'
import profile from '../pages/profile'
import Login from '../login/Login.vue'

  const routes = [
    {
      name: 'Dashboard',
      path: '/',
      component: dashboard,
      meta: { requiresAuth: true }, // Đặt thuộc tính requiresAuth cho các route cần bảo vệ
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('authToken');
        if (token) {
          console.log(token)
          next();  // Cho phép truy cập nếu có token
        } else {
          next('/login');  // Chuyển hướng tới trang đăng nhập nếu không có token
        }
      },
      children: [
         {
          name: 'home',
          path: '/home',
          component:home
        },
        {
          name: 'profile',
          path: '/profile',
          component:profile
        }
      ]
    },
    { 
      path: '/login', 
      component: Login 
    }
       
  ];
  
const router = Router();
export default router;

// Navigation Guard để kiểm tra nếu route yêu cầu đăng nhập
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('authToken'); // Kiểm tra token đăng nhập
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Nếu route yêu cầu đăng nhập mà chưa đăng nhập, chuyển hướng đến trang login
    if (!isAuthenticated) {
      next('/login');
    } else {
      next(); // Cho phép truy cập nếu đã đăng nhập
    }
  } else {
    next(); // Cho phép truy cập các trang không yêu cầu đăng nhập
  }
});

function Router() {
    const router = new createRouter({
        history: createWebHistory(),
        routes,
    });
    return router;
}
  