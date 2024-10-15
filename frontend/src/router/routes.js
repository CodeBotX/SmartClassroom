import DashboardLayout from "@/layout/dashboard/DashboardLayout.vue";
// GeneralViews
import NotFound from "@/pages/NotFoundPage.vue";
import Login from '../components/login/Login.vue'
import StudyLayout from '@/layout/study/StudyLayout.vue'



// Admin pages
const Administration = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/Administration.vue");
const EducationProgram = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/EducationProgram.vue");
const Dashboard = () =>
  import(/* webpackChunkName: "dashboard" */ "@/pages/Dashboard.vue");
const Profile = () =>
  import(/* webpackChunkName: "common" */ "@/pages/Profile.vue");
const Notifications = () =>
  import(/* webpackChunkName: "common" */ "@/pages/Notifications.vue");
const Icons = () =>
  import(/* webpackChunkName: "common" */ "@/pages/Icons.vue");
const Maps = () => import(/* webpackChunkName: "common" */ "@/pages/Maps.vue");
const Typography = () =>
  import(/* webpackChunkName: "common" */ "@/pages/Typography.vue");
const TableList = () =>
  import(/* webpackChunkName: "common" */ "@/pages/TableList.vue");

const routes = [
  {
    name: 'Dashboard',
    path: "/",
    component: DashboardLayout,
    redirect: "/dashboard",
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
        path: "administration",
        name: "administration",
        component: Administration,
      },
      {
        path: "education_program",
        name: "education_program",
        component: EducationProgram,
      },
      {
        path: "dashboard",
        name: "dashboard",
        component: Dashboard,
      },
      {
        path: "profile",
        name: "profile",
        component: Profile,
      },
      {
        path: "notifications",
        name: "notifications",
        component: Notifications,
      },
      {
        path: "icons",
        name: "icons",
        component: Icons,
      },
      {
        path: "maps",
        name: "maps",
        component: Maps,
      },
      {
        path: "typography",
        name: "typography",
        component: Typography,
      },
      {
        path: "table-list",
        name: "table-list",
        component: TableList,
      },

      // import
      // {
      //   name: 'profile',
      //   path: '/profile',
      //   component: profile
      // },
      // {
      //   name: 'detail',
      //   path: '/detail',
      //   component: UserDetail,
      // }
    ],
  },
  { 
    name: 'login',
    path: '/login', 
    component: Login 
  },
  {
    name: 'study',
    path: '/study',
    component: StudyLayout,
    meta: { requiresAuth: true },
    beforeEnter: (to, from, next) => {
      const token = localStorage.getItem('access_token');
      console.log(token)
      if (token) {
        next();  // Cho phép truy cập nếu có token
      } else {
        next('/login');  // Chuyển hướng tới trang đăng nhập nếu không có token
      }
    },
  },
  { path: "*", component: NotFound },
];

/**
 * Asynchronously load view (Webpack Lazy loading compatible)
 * The specified component must be inside the Views folder
 * @param  {string} name  the filename (basename) of the view to load.
function view(name) {
   var res= require('../components/Dashboard/Views/' + name + '.vue');
   return res;
};**/

export default routes;
