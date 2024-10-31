<template>
  <!-- <div>
    <md-table v-model="users" :md-sort.sync="currentSort" :md-sort-order.sync="currentSortOrder" :md-sort-fn="customSort" md-card>
      <md-table-toolbar>
        <h1 class="md-title">Users</h1>
      </md-table-toolbar>

      <md-table-row slot="md-table-row" slot-scope="{ item }">
        <md-table-cell md-label="ID" md-numeric>{{ item.id }}</md-table-cell>
        <md-table-cell md-label="Name" md-sort-by="name">{{ item.name }}</md-table-cell>
        <md-table-cell md-label="Email" md-sort-by="email">{{ item.email }}</md-table-cell>
        <md-table-cell md-label="Gender" md-sort-by="gender">{{ item.gender }}</md-table-cell>
        <md-table-cell md-label="Job Title" md-sort-by="title">{{ item.title }}</md-table-cell>
      </md-table-row>
    </md-table>
  </div> -->

  <div>
    
    <!-- Bang hien thi -->
    <div>
      <p id="topDiv">Tuần thứ: </p>
      <table class="table-bordered"  id="tableRef" style="width: 863px">
          <tbody>
              <tr style="height: 62px;">
                  <td style="width: 82px; height: 62px;">Thứ</td>
                  <td style="width: 29px; height: 62px;">Tiết</td>
                  <td style="width: 81px; height: 62px;">Môn học</td>
                  <td style="width: 10px; height: 62px;">Tiết theo PPCT</td>
                  <td style="width: 125px; height: 62px;">Tên học sinh nghỉ</td>
                  <td style="width: 173px; height: 62px;">Tên bài, nội dung công việc</td>
                  <td style="width: 226px; height: 62px;">Nhận xét của giáo viên</td>
                  <td style="width: 53px; height: 62px;">Xếp loại tiết học</td>
                  <td style="width: 58px; height: 62px;">Ký tên</td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 82px; height: 310.333px;" rowspan="6">
                      <p>Thứ Hai</p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                  </td>
                  <td style="width: 29px; height: 62px;">1</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62.3333px;">
                  <td style="width: 29px; height: 62.3333px;">2</td>
                  <td style="width: 81px; height: 62.3333px;"></td>
                  <td style="width: 10px; height: 62.3333px;"></td>
                  <td style="width: 125px; height: 62.3333px;"></td>
                  <td style="width: 173px; height: 62.3333px;"></td>
                  <td style="width: 226px; height: 62.3333px;"></td>
                  <td style="width: 53px; height: 62.3333px;"></td>
                  <td style="width: 58px; height: 62.3333px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">3</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">4</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">5</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">6</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 82px; height: 62px;" rowspan="6">
                      <p>Thứ Ba</p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                  </td>
                  <td style="width: 29px; height: 62px;">1</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">2</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">3</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">4</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">5</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">6</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 82px; height: 62px;" rowspan="6">
                      <p>Thứ Tư</p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                  </td>
                  <td style="width: 29px; height: 62px;">1</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">2</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">3</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">4</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">5</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">6</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 82px; height: 62px;" rowspan="6">
                      <p>Thứ Năm</p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                  </td>
                  <td style="width: 29px; height: 62px;">1</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">2</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">3</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">4</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">5</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">6</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 82px; height: 62px;" rowspan="6">
                      <p>Thứ S&aacute;u</p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                  </td>
                  <td style="width: 29px; height: 62px;">1</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">2</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">3</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">4</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">5</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">6</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 82px; height: 62px;" rowspan="6">
                      <p>Thứ Bảy</p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                  </td>
                  <td style="width: 29px; height: 62px;">1</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">2</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">3</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">4</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">5</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">6</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 82px; height: 62px;" rowspan="6">
                      <p>Chủ Nhật</p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                      <p></p>
                  </td>
                  <td style="width: 29px; height: 62px;">1</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">2</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">3</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">4</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">5</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
              <tr style="height: 62px;">
                  <td style="width: 29px; height: 62px;">6</td>
                  <td style="width: 81px; height: 62px;"></td>
                  <td style="width: 10px; height: 62px;"></td>
                  <td style="width: 125px; height: 62px;"></td>
                  <td style="width: 173px; height: 62px;"></td>
                  <td style="width: 226px; height: 62px;"></td>
                  <td style="width: 53px; height: 62px;"></td>
                  <td style="width: 58px; height: 62px;"></td>
              </tr>
          </tbody>
      </table>
      <div class="row" id="bottomDiv" style="width: 863px">
          <div class="col-md-6">
              <p>Nhận xét của giáo viên chủ nhiệm lớp:</p>
              <p>.....................................................................................................................</p>
              <p>.....................................................................................................................</p>
              <p>.....................................................................................................................</p>
              <p>.....................................................................................................................</p>
          </div>
          <div class="col-md-6">
              <p style="text-align: center;">Giáo viên chủ nhiệm lớp</p>
              <p style="text-align: center; font-style: italic;">(Ký, ghi rõ họ tên)</p>
          </div>
      </div>
    </div>

    <base-button class="mt-5 mb-5" @click="ExportToExcel('xlsx')">Export to pdf</base-button>
  </div>
</template>

<script>
import * as XLSX from 'xlsx';
// export default {
//   methods: {
//     ExportToExcel(type, fn, dl) {
//               var elt = document.getElementById('tableRef');
//               var wb = XLSX.utils.table_to_book(elt, { sheet: "sheet1" });
//               return dl ?
//                   XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }) :
//                   XLSX.writeFile(wb, fn || ('MySheetName.' + (type || 'xlsx')));
//           }
//   }
// };


export default {
  methods: {
    ExportToExcel(type, fn, dl) {
      const wb = XLSX.utils.book_new();
      const ws = XLSX.utils.aoa_to_sheet([]);

      // 1. Capture and add top content
      const topDiv = document.getElementById('topDiv').innerText;
      XLSX.utils.sheet_add_aoa(ws, [[topDiv]], { origin: "A1" });
      ws["!merges"] = [{ s: { r: 0, c: 0 }, e: { r: 0, c: 3 } }]; // Merges A1:D1

      // 2. Capture and add table content right below top content
      const elt = document.getElementById('tableRef');
      if (elt) {
        const wsTable = XLSX.utils.table_to_sheet(elt);
        const tableRows = XLSX.utils.sheet_to_json(wsTable, { header: 1 });
        // Add table content starting at the next row after the top content
        const startRowForTable = topDiv.split('\n').length + 1; // Adjust based on the number of lines in topDiv
        XLSX.utils.sheet_add_aoa(ws, tableRows, { origin: `A${startRowForTable}` }); // Starts table below top content
      }

      // 3. Set the starting row for bottom content permanently to 45
      const bottomStartRow = 45;

      // Part 1: Teacher's report
      XLSX.utils.sheet_add_aoa(ws, [
        ["Nhận xét của giáo viên chủ nhiệm lớp:", "", "", "", ""],
        [".....................................................................................................................", "", "", "", ""],
        [".....................................................................................................................", "", "", "", ""],
        [".....................................................................................................................", "", "", "", ""]
      ], { origin: `A${bottomStartRow}` });

      ws["!merges"].push({
        s: { r: bottomStartRow, c: 0 },
        e: { r: bottomStartRow + 3, c: 4 }  // Merges A(bottomStartRow):E(bottomStartRow + 3)
      });

      // Part 2: Teacher's signature
      XLSX.utils.sheet_add_aoA(ws, [
        ["", "", "", "", "", "Giáo viên chủ nhiệm lớp", "", "", ""],
        ["", "", "", "", "", "(Ký, ghi rõ họ tên)", "", "", ""]
      ], { origin: `F${bottomStartRow}` });

      ws["!merges"].push({
        s: { r: bottomStartRow, c: 5 },
        e: { r: bottomStartRow + 1, c: 8 }  // Adjusting the merge range for signature part
      });

      // 4. Append sheet to workbook and export
      XLSX.utils.book_append_sheet(wb, ws, "Combined Content");

      return dl ?
        XLSX.write(wb, { bookType: type, bookSST: true, type: 'base64' }) :
        XLSX.writeFile(wb, fn || ('MySheetName.' + (type || 'xlsx')));
    }
  }
};
</script>