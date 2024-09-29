import { createRouter, createWebHistory } from "vue-router";
 
import dashboard from '../components/pages/master/dashboard'

import home from '../components/pages/home'
import profile from '../components/pages/profile'
import Login from '../components/login/Login.vue'
import UserDetail from '../components/pages/UserDetail.vue'

  const routes = [
    {
      name: 'Dashboard',
      path: '/',
      component: dashboard,
      meta: { requiresAuth: true }, // Đặt thuộc tính requiresAuth cho các route cần bảo vệ
      beforeEnter: (to, from, next) => {
        const token = localStorage.getItem('access_token');
        console.log(token)
        if (token) {
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
        },
        {
          name: 'detail',
          path: '/detail',
          component: UserDetail,
          props: true,
        }
      ]
    },
    { 
      name: 'login',
      path: '/login', 
      component: Login 
    }
       
  ];
  
const router = Router();
export default router;

// Navigation Guard để kiểm tra nếu route yêu cầu đăng nhập
router.beforeEach((to, from, next) => {
  const isAuthenticated = localStorage.getItem('access_token'); // Kiểm tra token đăng nhập
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
  